#import packages

import numpy as np
import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt
import OmicsIntegrator as oi
import os

#set working directory

os.chdir('/kuacc/users/adansik22/network_modeling/')

#get patient ids

dirlist=os.listdir("patients/")

#parameter sweep

for i in dirlist :
    #get interactome and prize files
    interactome_file="reference/iref_nohub.tsv"
    prize_file=f"terminals/{i}.tsv"

    interactome = pd.read_csv(interactome_file, delimiter = '\t')
    prize = pd.read_csv(prize_file, delimiter = "\t")

    #build network
    params = {
        "noise": 0.1, 
        "dummy_mode": "terminals", 
        "exclude_terminals": False, 
        "seed": 1
    }

    graph = oi.Graph(interactome_file, params)
    graph.prepare_prizes(prize_file)


    #set parameters and do grid search
    Ws = list(np.arange(2,6,1))
    Bs = list(np.arange(2,6,1))
    Gs = list(np.arange(2,6,1))


    results = graph.grid_search(prize_file, Ws, Bs, Gs)
    membership_df = oi.summarize_grid_search(results, "membership")
    node_attributes_df = graph.node_attributes

    #add coverage info
    initial_nodes = list(prize.name)
    results_with_terminals = membership_df[membership_df.index.isin(initial_nodes)]
    initial_node_covers = results_with_terminals.sum().sort_values(ascending=False).to_frame(name="Covering_nodes")
    out = set(initial_node_covers[initial_node_covers["Covering_nodes"]==max(initial_node_covers["Covering_nodes"])].index)
    initial_node_covers.sort_index(axis=0, inplace=True)
    membership_df.sort_index(axis=1, inplace=True)
    total_node = membership_df.sum().to_frame(name="Total_nodes")
    membership_df.loc['Covering_nodes']=(initial_node_covers['Covering_nodes'])
    membership_df.loc['Total_nodes']=(total_node['Total_nodes'])

    #add component info
    components={}

    for key, d in results.items():
        num_components = len(list(nx.connected_components(d["augmented_forest"])))
        name=str(key)
        components[name]=num_components

    component_df=pd.DataFrame.from_dict(components, orient="index", columns=["Component_number"])
    t_component_df=component_df.transpose()

    membership_df=pd.concat([membership_df,t_component_df])


    node_attributes_df.to_csv(f'patients/{i}/{i}_node_attributes.csv')
    membership_df.to_csv(f'patients/{i}/{i}_membership_df.csv')

