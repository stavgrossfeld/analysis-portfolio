# PBMC 3k scRNA-seq Arrow Pipeline

Portfolio-ready single-cell RNA-seq analysis pipeline using a Kaggle dataset and Apache Arrow.

## What This Does
- Loads PBMC 3k scRNA-seq data from Kaggle
- Runs QC, normalization, PCA, UMAP, clustering, marker genes
- Writes Arrow artifacts for fast, portable intermediate storage

## Dataset
Kaggle: `mannekuntanagendra/single-cell-rna-seq-analysis-qc-clustering-pbmc-3k`

## R Pipeline (Recommended)
Notebook: `notebooks/pbmc3k_arrow_pipeline.Rmd`  
Rendered HTML: `notebooks/pbmc3k_arrow_pipeline.html`

### View the Report
GitHub Pages (recommended):  
`https://stavgrossfeld.github.io/analysis-portfolio/pbmc3k-scrna/notebooks/pbmc3k_arrow_pipeline.html`

GitHub source (Markdown/HTML in repo):  
`https://github.com/stavgrossfeld/analysis-portfolio/tree/main/pbmc3k-scrna`

### R Setup (pak)
The notebook installs deps with `pak` automatically. If you want to install manually:
```r
if (!requireNamespace("pak", quietly = TRUE)) install.packages("pak")
pak::pkg_install(c("Seurat", "Matrix", "ggplot2", "dplyr", "arrow"))
```

### Run
```r
# From RStudio or R console
rmarkdown::render("notebooks/pbmc3k_arrow_pipeline.Rmd")
```

If you want to render without executing (for a static portfolio artifact):  
```bash
SKIP_PAK_INSTALL=1 SKIP_R_RUN=1 R -e 'rmarkdown::render("notebooks/pbmc3k_arrow_pipeline.Rmd")'
```

### Outputs
- `outputs/pbmc3k_seurat.rds`
- `outputs/arrow/qc_metrics.feather`
- `outputs/arrow/cell_clusters.feather`

## Python Pipeline (Optional)
Notebook: `notebooks/pbmc3k_arrow_pipeline.ipynb`

### Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run
```bash
jupyter notebook notebooks/pbmc3k_arrow_pipeline.ipynb
```

### Outputs
- `outputs/pbmc3k_processed.h5ad`
- `outputs/arrow/qc_metrics.feather`
- `outputs/arrow/expression_matrix.feather`

## Data Access
Option A: Kaggle CLI (recommended)
- Put your token at `~/.kaggle/kaggle.json`
- Run the notebook; it will download automatically

Option B: Manual download
- Download the dataset from Kaggle
- Unzip into `data/pbmc3k/`
