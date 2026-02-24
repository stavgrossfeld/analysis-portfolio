# Repro guide — Breast cancer cell lines scRNA-seq

This runbook reproduces the analysis and HTML report.

## 1) Data download

Use Kaggle CLI:

```
~/.virtualenvs/r-reticulate/bin/kaggle datasets download \
  -d alexandervc/scrnaseq-breast-cancer-cell-lines-atlas \
  -p /Users/stav/repos/analysis-portfolio/breast-cancer-scrna/data \
  --unzip
```

Expected files:

- `breast-cancer-scrna/data/MTX_FMT_GSE173634/matrix.mtx`
- `breast-cancer-scrna/data/MTX_FMT_GSE173634/features.tsv`
- `breast-cancer-scrna/data/MTX_FMT_GSE173634/barcodes.tsv`

## 2) R environment (shared)

Use the shared repo-level `renv`:

```
/Library/Frameworks/R.framework/Resources/bin/R -q -e "renv::init(bare=TRUE)"
/Library/Frameworks/R.framework/Resources/bin/R -q -e "install.packages('pak', repos='https://cloud.r-project.org')"
/Library/Frameworks/R.framework/Resources/bin/R -q -e "pak::pkg_install(c('Seurat','dplyr','ggplot2','patchwork','tidyr','stringr','viridis','biomaRt','DESeq2'))"
/Library/Frameworks/R.framework/Resources/bin/R -q -e "renv::snapshot()"
```

## 3) Render the report

```
/Library/Frameworks/R.framework/Resources/bin/R -q -e "rmarkdown::render('notebooks/breast_cancer_cell_lines.Rmd')" \
  --args /Users/stav/repos/analysis-portfolio/breast-cancer-scrna
```

Output:

- `breast-cancer-scrna/notebooks/breast_cancer_cell_lines.html`
