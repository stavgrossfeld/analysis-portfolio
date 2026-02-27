# Analysis Portfolio

Portfolio of reproducible bioinformatics analyses with rendered reports on GitHub Pages.

**Live site:** `https://stavgrossfeld.github.io/analysis-portfolio/`

## Projects

- `pbmc3k-scrna/`
  - End-to-end PBMC 3k scRNA-seq pipeline in Seurat
  - QC, normalization, PCA/UMAP, clustering
  - DESeq2-backed marker discovery + marker significance plots
  - Arrow/Feather outputs for downstream handoff

- `breast-cancer-scrna/`
  - Single-cell atlas analysis of 32 breast cancer cell lines
  - QC, clustering, state scoring, DESeq2 marker discovery
  - XGBoost multiclass model to predict `cell_line`
  - XGBoost feature-importance ranking for top differentiating genes

## Live Site

- GitHub Pages: `https://stavgrossfeld.github.io/analysis-portfolio/`

## Repo Structure

- `index.html`: GitHub Pages landing page
- `pbmc3k-scrna/notebooks/`: PBMC reports and notebook sources
- `breast-cancer-scrna/notebooks/`: Breast-cancer reports and notebook sources
