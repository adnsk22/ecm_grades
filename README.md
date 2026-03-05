#**ECM GRADES**

<img src="https://github.com/user-attachments/assets/ff81c86d-8abf-411f-8771-07d47dbd5b61" alt="Workflow diagram" width="600">

## Overview



This repository contains data processing, patient ECM barcoding and stratification, patient-specific network construction, ECM-specific consensus network construction and network proximity analyses as well as downstream analyses such as ECM grade-specific highly variable gene identification, Pathway/TF enrichment, cellular deconvolution cancer-associated pathway score calculations, clinical investigation of ECM grades and mutation profiling. All of the data generated in the study are provided as well as the input data used in the analyses.



## Repository structure



```

ecm_grades/

├── data/ (Raw and/or preprocessed input data.)

│   └── DRUGBANK_14_03_2024/ (Drug data used for network proximity analysis including FDA approved drugs, drug target proteins and relevant annotations.)

│   └── cbioportal/luad_cptac_2020/ (Omic and clinical data processed by CBioPortal.)

│   └── clinical-cptac-3.2023-10-02/ (Survival and recurrence data of patients retrieved from CPTAC.)

│   └── lists/ (List of genes and drugs used in the study including Matrisome genes, cancer-associated pathway genes and oncotreat drug list.)

│   └── raw_data/ (Raw omic data retrieved directly from the supplementary data from Gillette et al. (2020).)

│   └── reference_interactome/ (Raw and processed reference PPI interactome used in network analyses.)

├── network_modeling/ (Scripts and notebooks for building ECM guided patient-specific networks)

│   └── patients/ (Contains directories for each patient which include patient-specific networks, OmicsIntegrator2 solutions for every parameter combination.)

│   └── reference/ (Processed reference PPI interactome.)

│   └── scripts/ (Includes the auxilary scripts for generating OI2 solutions(get_memberships.py), selecting the most optimal parameter combinations(get_parameterlist.R) and reconstructing the final network from the most optimal parameter combinations(get_networks.py))

│   └── terminals/ (Contains prize files for each patient.)

│   └── final_parameter_list.csv (Generated csv file containing the optimal parameter combinations for each patient.)

│   └── ecm_grades.sh (Bash script that runs the auxilary scripts as a pipeline.)

│   └── ecm_momix.yml (Conda environment necessary to run the process.)

├── network_proximity/ (Inputs and codes for the network proximity analysis)

│   └── input_data/ (Contains processed reference PPI interactome, ECM consensus networks, processed drug-target data.)

│   └── network_proximity_pool.py (Python script for running the network proximity analysis.)

│   └── proximity_results_insol.csv (CSV file containing relative proximity values between ECM consensus networks and drug targets.)
│   └── proximity.yml (Conda environment necessary to run the process.)

├── out_data/ (Generated outputs (networks, tables, figures))

│   └── TRRUST/ (TF enrichment results for each patient obtained from TRRUST)

│   └── enrichments/ (Patient pathway enrichment analysis results for KEGG, REACTOME and HALLMARK pathways and GO Biological Processes) 

│   └── lists/ (Contains outputs of omic data analysis such as foldchange values and normalized expression data. Also contains both multi-omic and single-omic patient-specific ECM barcodes.)

│   └── network_data/ (Contains outputs of network data analysis such as average cost, edge, node and terminal counts.)

│   └── pptx_data/ (Contains differentially phosphorylated ECM proteins for each patient later included in terminal list along with TFs.)

│   └── terminals/ (Contains terminals for each patient.)

│   └── trx_data/ (Contains differentially expressed ECM genes for each patient used for TF enrichment analysis.)

├── patients_all/ (graphml files of ECM guided patient-specific networks.)

├── consensus_networks.py (Python script to construct consensus networks)

└──  main.rmd (Main analysis workflow (R Markdown))

```



## Requirements



### R

R (>= 4.1)
rmarkdown
tidyverse
readxl
ggstatsplot
ggpubr
M3C
vegan
survival
survminer
immunedeconv
enrichR
ComplexHeatmap
patchwork
circlize
reshape2
ggforestplot
ggvenn
gridExtra

### Python

Python (>=2.7)
OmicsIntegrator
numpy
pandas
networkx
sys
pandas
networkx


> Exact package versions used in the analysis are provided in the supplementary tables associated with the manuscript and the conda environments are provided as .yml .



## How to run



### Network modeling



Set network_modeling as working directory and activate the ecm_momix environment provided as ecm_momix.yml. Place prize files for each patient in `terminals/` and the reference interactome to `reference/` and run the bash script



```bash

bash ecm_grades.sh

```

Outputs will be written to `patients/`.



### Building consensus networks



Set ecm_grades as working directory. Patient-specific networks should be under `patients_all/` in .graphml format, ECM grade annotations are provided under `out_data/lists/`. Run consensus_networks.py



```bash

python consensus_networks.py

```

Outputs will be written to `out_data/network_data/`.



### Network proximity



Set network_proximity as working directory and activate the proximity environment provided as proximity.yml. Place reference PPI interactome, consensus networks and drug-target data in `input_data/` and run python script.



```bash

python network_proximity_pool.py

```

Outputs will be written to the working directory..



## Downstream analyses.



main.rmd contains the codes for the 



\* processing of some of the input data for the network modeling, and proximity analyses such as terminal preparation, PPI reference interactome and drug filtering, 

\* analysis of the multi-omic data, 

\* generation of ECM barcoding, and ECM based clustering of the patients, 

\* pathway enrichment analyses, 

\* clinical data analyses, 

\* cellular deconvolution analyses and 

\* generation of all of the figures in the article



You can run main.rmd using RStudio.

All generated files from this script are saved under `out_data/` with self-descriptive filenames.



\## Contact



For questions or issues, please open an issue or contact the repository maintainer.



