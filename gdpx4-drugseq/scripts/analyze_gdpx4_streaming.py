#!/usr/bin/env python3
"""Stream and analyze the GDPx4 DRUG-seq dataset from Hugging Face parquet."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from datasets import load_dataset


DEFAULT_REPO = "ginkgo-datapoints/GDPx4"
DEFAULT_PARQUET = "differential_expression.parquet"


@dataclass
class CompoundStats:
    rows: int = 0
    lfc_sum: float = 0.0
    significant_rows: int = 0

    def update(self, lfc: float | None, is_significant: bool) -> None:
        self.rows += 1
        if lfc is not None and math.isfinite(lfc):
            self.lfc_sum += lfc
        if is_significant:
            self.significant_rows += 1

    @property
    def mean_lfc(self) -> float | None:
        if self.rows == 0:
            return None
        return self.lfc_sum / self.rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=DEFAULT_REPO, help="HF dataset repo id")
    parser.add_argument("--data-file", default=DEFAULT_PARQUET, help="Parquet file in dataset repo")
    parser.add_argument(
        "--token",
        default=os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_HUB_TOKEN"),
        help="HF token (or set HF_TOKEN / HUGGING_FACE_HUB_TOKEN)",
    )
    parser.add_argument("--max-rows", type=int, default=500_000, help="Rows to stream for analysis")
    parser.add_argument("--top-n", type=int, default=50, help="Top genes to keep by abs(log2 fold change)")
    parser.add_argument(
        "--out-dir",
        default="gdpx4-drugseq/outputs",
        help="Output directory for CSV/JSON artifacts",
    )
    return parser.parse_args()


def load_token_from_dotenv(dotenv_path: Path = Path(".env")) -> str | None:
    if not dotenv_path.exists():
        return None
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key not in {"HF_TOKEN", "HUGGING_FACE_HUB_TOKEN"}:
            continue
        token = value.strip().strip("'\"")
        return token or None
    return None


def pick_column(columns: list[str], candidates: list[str]) -> str | None:
    lower_map = {c.lower(): c for c in columns}
    for cand in candidates:
        if cand.lower() in lower_map:
            return lower_map[cand.lower()]
    return None


def to_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        out = float(value)
        if not math.isfinite(out):
            return None
        return out
    except (TypeError, ValueError):
        return None


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    token = args.token or load_token_from_dotenv()
    if not token:
        raise SystemExit(
            "Missing Hugging Face auth token. Set HF_TOKEN or pass --token. "
            "GDPx4 is currently gated on the Hub. "
            "A local .env file with HF_TOKEN is also supported."
        )

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ds = load_dataset(
        args.repo,
        data_files=args.data_file,
        split="train",
        token=token,
        streaming=True,
    )

    iterator = iter(ds)
    first_row = next(iterator)
    columns = list(first_row.keys())

    compound_col = pick_column(columns, ["compound", "perturbation", "drug"])
    cell_line_col = pick_column(columns, ["cell_line", "cellline", "cell_type"])
    gene_col = pick_column(columns, ["gene", "gene_symbol", "feature"])
    lfc_col = pick_column(columns, ["log2FoldChange", "log2_fold_change", "log2fc", "lfc"])
    padj_col = pick_column(columns, ["padj", "adj_pvalue", "q_value", "qvalue", "fdr"])

    if compound_col is None or gene_col is None:
        raise SystemExit(f"Required columns not found. Available columns: {columns}")

    compounds: set[str] = set()
    cell_lines: set[str] = set()
    genes: set[str] = set()
    compound_stats: dict[str, CompoundStats] = defaultdict(CompoundStats)
    top_gene_hits: list[dict[str, Any]] = []

    def process_row(row: dict[str, Any], rank_idx: int) -> None:
        compound = str(row.get(compound_col, ""))
        gene = str(row.get(gene_col, ""))
        cell_line = str(row.get(cell_line_col, "")) if cell_line_col else ""
        lfc = to_float(row.get(lfc_col)) if lfc_col else None
        padj = to_float(row.get(padj_col)) if padj_col else None

        compounds.add(compound)
        genes.add(gene)
        if cell_line_col and cell_line:
            cell_lines.add(cell_line)

        is_significant = bool(
            lfc is not None and abs(lfc) >= 1.0 and padj is not None and padj < 0.05
        )
        compound_stats[compound].update(lfc, is_significant)

        if lfc is not None:
            top_gene_hits.append(
                {
                    "gene": gene,
                    "compound": compound,
                    "cell_line": cell_line,
                    "lfc": lfc,
                    "abs_lfc": abs(lfc),
                    "padj": padj,
                    "rank_idx": rank_idx,
                }
            )

    process_row(first_row, rank_idx=1)

    rows_processed = 1
    for row in iterator:
        rows_processed += 1
        process_row(row, rank_idx=rows_processed)
        if args.max_rows and rows_processed >= args.max_rows:
            break

    compound_rows: list[dict[str, Any]] = []
    for compound, st in compound_stats.items():
        compound_rows.append(
            {
                "compound": compound,
                "rows": st.rows,
                "mean_log2fc": st.mean_lfc,
                "significant_rows": st.significant_rows,
                "significant_rate": (st.significant_rows / st.rows) if st.rows else None,
            }
        )
    compound_rows.sort(key=lambda x: x["rows"], reverse=True)

    top_gene_hits.sort(key=lambda x: x["abs_lfc"], reverse=True)
    top_gene_hits = top_gene_hits[: args.top_n]

    summary = {
        "dataset_repo": args.repo,
        "data_file": args.data_file,
        "streaming": True,
        "sample_rows_processed": rows_processed,
        "analysis_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "columns": columns,
        "detected_columns": {
            "compound": compound_col,
            "cell_line": cell_line_col,
            "gene": gene_col,
            "lfc": lfc_col,
            "padj": padj_col,
        },
        "unique_compounds_in_sample": len(compounds),
        "unique_cell_lines_in_sample": len(cell_lines),
        "unique_genes_in_sample": len(genes),
        "notes": "Streaming sample analysis. Increase --max-rows for deeper coverage.",
    }

    summary_path = out_dir / "gdpx4_streaming_summary.json"
    compounds_path = out_dir / "gdpx4_compound_summary.csv"
    genes_path = out_dir / "gdpx4_top_gene_hits.csv"

    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_csv(
        compounds_path,
        ["compound", "rows", "mean_log2fc", "significant_rows", "significant_rate"],
        compound_rows,
    )
    write_csv(
        genes_path,
        ["gene", "compound", "cell_line", "lfc", "abs_lfc", "padj", "rank_idx"],
        top_gene_hits,
    )

    print(f"Wrote: {summary_path}")
    print(f"Wrote: {compounds_path}")
    print(f"Wrote: {genes_path}")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
