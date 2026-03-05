# ECM GRADES

<img src="https://github.com/user-attachments/assets/ff81c86d-8abf-411f-8771-07d47dbd5b61" alt="Workflow diagram" width="600">

## Overview

ECM GRADES is a multi-omic analysis pipeline for ECM-based patient stratification and network-driven drug prioritization in lung adenocarcinoma (LUAD). Using proteogenomic data from the CPTAC cohort, the pipeline constructs ECM-guided patient-specific networks, derives ECM barcodes for patient clustering, and performs network proximity analysis to identify candidate therapeutic targets.

The repository includes all input data, intermediate outputs, and analysis code needed to reproduce the results reported in the associated manuscript.

---

## Repository Structure

```
ecm_grades/
├── data/
│   ├── DRUGBANK_14_03_2024/
│   ├── cbioportal/luad_cptac_2020/
│   ├── clinical-cptac-3.2023-10-02/
│   ├── lists/
│   ├── raw_data/
│   └── reference_interactome/
├── network_modeling/
│   ├── patients/
│   ├── reference/
│   ├── scripts/
│   ├── terminals/
│   ├── final_parameter_list.csv
│   ├── ecm_grades.sh
│   └── ecm_momix.yml
├── network_proximity/
│   ├── input_data/
│   ├── network_proximity_pool.py
│   ├── proximity_results_insol.csv
│   └── proximity.yml
├── out_data/
│   ├── TRRUST/
│   ├── enrichments/
│   ├── lists/
│   ├── network_data/
│   ├── pptx_data/
│   ├── terminals/
│   └── trx_data/
├── patients_all/
├── consensus_networks.py
└── main.rmd
```

| Directory / File | Description |
|---|---|
| `data/` | Raw and preprocessed input data |
| `data/DRUGBANK_14_03_2024/` | FDA-approved drug data, drug targets, and annotations for network proximity analysis |
| `data/cbioportal/luad_cptac_2020/` | Omic and clinical data from CBioPortal |
| `data/clinical-cptac-3.2023-10-02/` | Patient survival and recurrence data from CPTAC |
| `data/lists/` | Gene and drug lists — Matrisome genes, cancer-associated pathway genes, OncoTreat drug list |
| `data/raw_data/` | Raw omic data from Gillette et al. (2020) supplementary materials |
| `data/reference_interactome/` | Raw and processed reference PPI interactome for network analyses |
| `network_modeling/` | Scripts for building ECM-guided patient-specific networks |
| `network_modeling/patients/` | Per-patient directories with OmicsIntegrator2 solutions across all parameter combinations |
| `network_modeling/scripts/` | Auxiliary scripts: `get_memberships.py`, `get_parameterlist.R`, `get_networks.py` |
| `network_modeling/terminals/` | Prize files for each patient |
| `network_modeling/ecm_grades.sh` | Bash pipeline script orchestrating the auxiliary scripts |
| `network_modeling/ecm_momix.yml` | Conda environment for network modeling |
| `network_proximity/` | Network proximity analysis inputs and code |
| `network_proximity/input_data/` | Reference interactome, consensus networks, and drug-target data |
| `network_proximity/network_proximity_pool.py` | Runs the network proximity analysis |
| `network_proximity/proximity_results_insol.csv` | Relative proximity values between ECM consensus networks and drug targets |
| `network_proximity/proximity.yml` | Conda environment for network proximity analysis |
| `out_data/` | All generated outputs — networks, tables, and figures |
| `out_data/TRRUST/` | TF enrichment results per patient from TRRUST |
| `out_data/enrichments/` | Pathway enrichment results (KEGG, REACTOME, HALLMARK, GO Biological Processes) |
| `out_data/lists/` | Fold-change values, normalized expression data, and ECM barcodes (multi-omic and single-omic) |
| `out_data/network_data/` | Network statistics — average cost, edge/node/terminal counts |
| `out_data/pptx_data/` | Differentially phosphorylated ECM proteins per patient (used as terminals alongside TFs) |
| `out_data/terminals/` | Final terminal lists per patient |
| `out_data/trx_data/` | Differentially expressed ECM genes per patient for TF enrichment |
| `patients_all/` | GraphML files of ECM-guided patient-specific networks |
| `consensus_networks.py` | Constructs ECM consensus networks from patient-specific networks |
| `main.rmd` | Main analysis workflow (R Markdown) |

---

## Requirements

### R (>= 4.1)

| Package | Package | Package |
|---|---|---|
| `rmarkdown` | `tidyverse` | `readxl` |
| `ggstatsplot` | `ggpubr` | `M3C` |
| `vegan` | `survival` | `survminer` |
| `immunedeconv` | `enrichR` | `ComplexHeatmap` |
| `patchwork` | `circlize` | `reshape2` |
| `ggforestplot` | `ggvenn` | `gridExtra` |

### Python (>= 2.7)

| Package | Package |
|---|---|
| `OmicsIntegrator` | `numpy` |
| `pandas` | `networkx` |

> Exact package versions are provided in the supplementary tables of the associated manuscript. Conda environments for each pipeline stage are included as `.yml` files.

---

## How to Run

### 1. Network Modeling

Activate the conda environment and set `network_modeling/` as the working directory. Place patient prize files in `terminals/` and the reference interactome in `reference/`, then run:

```bash
conda activate ecm_momix  # from ecm_momix.yml
bash ecm_grades.sh
```

Outputs are written to `patients/`.

---

### 2. Building Consensus Networks

From the root `ecm_grades/` directory, ensure patient-specific networks are in `patients_all/` as `.graphml` files and ECM grade annotations are under `out_data/lists/`. Then run:

```bash
python consensus_networks.py
```

Outputs are written to `out_data/network_data/`.

---

### 3. Network Proximity

Activate the conda environment and set `network_proximity/` as the working directory. Place the reference PPI interactome, consensus networks, and drug-target data in `input_data/`, then run:

```bash
conda activate proximity  # from proximity.yml
python network_proximity_pool.py
```

Outputs are written to the working directory.

---

### 4. Downstream Analyses

Open `main.rmd` in RStudio. This script handles:

- Input data preparation for network modeling and proximity analyses (terminal preparation, PPI filtering, drug filtering)
- Multi-omic data analysis
- ECM barcoding and patient clustering
- Pathway and TF enrichment analyses
- Clinical and survival analyses
- Cellular deconvolution
- Generation of all manuscript figures

All outputs are saved to `out_data/` with self-descriptive filenames.

---

## Contact

For questions or issues, please [open an issue](../../issues) or contact the repository maintainers via email (adansik22@ku.edu.tr or ntuncbag@ku.edu.tr).

## Citation

Dansık, A., Sarıca, S., Öztürk, E., & Tuncbag, N. (2025). Extracellular matrix-guided tumor stratification and network models reveal clinical molecular grades. bioRxiv. https://doi.org/10.1101/2025.08.29.672994


