# Reproducible Runbook (PBMC 3k scRNA-seq)

This file documents how to reproduce the analysis and rendered HTML.

## Requirements
- CRAN R installed (R 4.5.x recommended)
- Kaggle API token at `~/.kaggle/kaggle.json` with `chmod 600`
- Internet access to download the Kaggle dataset

## One-time setup
1. Install CRAN R (macOS .pkg). Verify:
   ```bash
   /Library/Frameworks/R.framework/Resources/bin/R --version
   ```
2. Set Kaggle token:
   ```bash
   mkdir -p ~/.kaggle
   # kaggle.json should be: {"username":"...","key":"..."}
   chmod 600 ~/.kaggle/kaggle.json
   ```

## Install dependencies (renv + pak)
```bash
/Library/Frameworks/R.framework/Resources/bin/R -e 'if (!requireNamespace("renv", quietly=TRUE)) install.packages("renv", repos="https://cloud.r-project.org"); renv::activate("/Users/stav/Desktop/codex_stuff"); renv::settings$snapshot.type("explicit"); renv::install("pak"); pak::pkg_install(c("Seurat","Matrix","ggplot2","dplyr","SeuratObject","patchwork","cowplot","ggrepel","ggridges","plotly","sctransform","igraph","uwot","reticulate","arrow")); renv::snapshot()'
```

## Download dataset
The notebook can download automatically if `kaggle` is installed in PATH. If not, use:
```bash
~/.virtualenvs/r-reticulate/bin/kaggle datasets download -d mannekuntanagendra/single-cell-rna-seq-analysis-qc-clustering-pbmc-3k -p /Users/stav/Desktop/codex_stuff/data/pbmc3k --unzip
```

## Render the notebook
```bash
/Library/Frameworks/R.framework/Resources/bin/R -e 'library(renv); renv::load("/Users/stav/Desktop/codex_stuff"); rmarkdown::render("notebooks/pbmc3k_arrow_pipeline.Rmd")'
```

## Outputs
- `notebooks/pbmc3k_arrow_pipeline.html`
- `outputs/pbmc3k_seurat.rds`
- `outputs/arrow/qc_metrics.feather`
- `outputs/arrow/cell_clusters.feather`
