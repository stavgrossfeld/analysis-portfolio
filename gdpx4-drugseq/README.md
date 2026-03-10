# GDPx4 DRUG-seq Streaming Analysis (HEK293)

This folder contains a streaming parquet analysis workflow for the Hugging Face dataset:

- Dataset: `ginkgo-datapoints/GDPx4`
- File: `differential_expression.parquet`

## What It Does

The script streams rows (no full local parquet download) and writes:

- `outputs/gdpx4_streaming_summary.json`
- `outputs/gdpx4_compound_summary.csv`
- `outputs/gdpx4_top_gene_hits.csv`

## Setup

```bash
python3 -m venv .venv-gdpx4
source .venv-gdpx4/bin/activate
pip install datasets polars pyarrow pandas seaborn matplotlib
```

## Authentication

`GDPx4` is currently gated on the Hugging Face Hub, so authenticate first:

```bash
source .venv-gdpx4/bin/activate
hf auth login
```

Or export a token directly:

```bash
export HF_TOKEN=hf_xxx
```

The script also auto-loads `HF_TOKEN` from a local `.env` file.

## Run

```bash
source .venv-gdpx4/bin/activate
python gdpx4-drugseq/scripts/analyze_gdpx4_streaming.py --max-rows 500000
```

Optional:

```bash
python gdpx4-drugseq/scripts/analyze_gdpx4_streaming.py \
  --repo ginkgo-datapoints/GDPx4 \
  --data-file differential_expression.parquet \
  --max-rows 2000000 \
  --top-n 100
```

## R Markdown Plots

You can stream GDPx4 inside an `.Rmd` using `reticulate` + Python `datasets`, then plot in R:

```bash
R -e 'rmarkdown::render("gdpx4-drugseq/notebooks/gdpx4_streaming_analysis.Rmd", params=list(max_rows=300000, top_n=30))'
```

Outputs include:

- `gdpx4-drugseq/outputs/figures/gdpx4_significant_genes_by_compound.png`
- `gdpx4-drugseq/outputs/figures/gdpx4_significant_rate_by_compound.png`
- `gdpx4-drugseq/outputs/figures/gdpx4_top_abs_log2fc_hits.png`
