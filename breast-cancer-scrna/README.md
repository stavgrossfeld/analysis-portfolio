# Breast Cancer Cell Lines scRNA-seq

Single-cell analysis of 32 human breast cancer cell lines (GSE173634). The notebook walks through QC, clustering, DESeq2-backed marker discovery (including per-cluster marker significance plots), XGBoost-based cell-line classification with gene-importance ranking, and state scoring (epithelial, mesenchymal, proliferative, stress), with gene-level boxplots to anchor the interpretation.

## Project artifacts

- Rendered report (HTML): `notebooks/breast_cancer_cell_lines.html`
- Source notebook: `notebooks/breast_cancer_cell_lines.Rmd`
- Repro steps: `AGENTS.md`

## View the report

GitHub Pages:  
`https://stavgrossfeld.github.io/analysis-portfolio/breast-cancer-scrna/notebooks/breast_cancer_cell_lines.html`

GitHub source:  
`https://github.com/stavgrossfeld/analysis-portfolio/tree/main/breast-cancer-scrna`

## Data source

Downloaded from Kaggle: `alexandervc/scrnaseq-breast-cancer-cell-lines-atlas` (Matrix Market files).

## Notes

This is a cell-line dataset. State labels in the report are descriptive and meant for interpretation, not clinical annotation.
