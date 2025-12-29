import sys
import os
import pandas as pd
from multiprocessing import Pool

os.chdir("/home/adansik22/tools/network_proximity/")
sys.path.append(os.getcwd())

from toolbox import wrappers

Convert reference interactome to sif format
iref = pd.read_csv("input_data/iref_nohub.tsv", sep='\t')
iref = iref[["protein1", "protein2"]]
iref['interaction_type'] = 'pp'

sif_df = iref[['protein1', 'interaction_type', 'protein2']]
sif_content = sif_df.apply(lambda x: ' '.join(x), axis=1)
sif_content.to_csv('input_data/network_for_prox.sif', index=False, header=False)

# Get reference
network = wrappers.get_network('input_data/network_for_prox.sif', only_lcc=True)

# Get drug targets
drug_proteins_df = pd.read_csv("input_data/drug_proteins.csv")

# Create drug dictionary
drug_proteins = drug_proteins_df.drop(columns="Number_of_Genes")
drug_nodes = {}
for index, row in drug_proteins.iterrows():
    prots = row["Drug_Proteins"]
    if isinstance(prots, str):
        drug_nodes[row["ID"]] = row["Drug_Proteins"].split(";")
    else:
        drug_nodes[row["ID"]] = [prots]

# Get consensus ECM networks
ecm_proteins = pd.read_csv("input_data/consensus_30pcnt.csv")

# Create cluster dictionary
ecm_nodes = {col: ecm_proteins[col].dropna().tolist() for col in ecm_proteins.columns}

def calculate_proximity(drug_cluster_pair):
    drug_name, nodes_from, cluster_name, nodes_to = drug_cluster_pair
    try:
        dc_pair = drug_name + "_" + cluster_name
        d, z, (mean, sd) = wrappers.calculate_proximity(network, nodes_from, nodes_to, min_bin_size=100, seed=452456)
        return {"dc_pair": dc_pair, "d": d, "z": z, "mean": mean, "sd": sd}
    except TypeError:
        return None

if __name__ == "__main__":
    drug_cluster_pairs = [(drug_name, nodes_from, cluster_name, nodes_to) 
                          for drug_name, nodes_from in drug_nodes.items()
                          for cluster_name, nodes_to in ecm_nodes.items()]

    pool = Pool()
    try:
        results = pool.map(calculate_proximity, drug_cluster_pairs)
    finally:
        pool.close()
        pool.join()

    # Filter out any None results due to exceptions
    proximity_results = [result for result in results if result is not None]

    df = pd.DataFrame(proximity_results, columns=["dc_pair", "d", "z", "mean", "sd"])

    # Write DataFrame to CSV file
    df.to_csv('proximity_results_insol.csv', index=False)

