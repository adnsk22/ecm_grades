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

#get parameter list

param_path="g34_parameter_list.csv"
parameters=pd.read_csv(param_path, delimiter = ',' )

#construct networks

forests={}

for index, row in parameters.iterrows():
    tosplit = row['patients']
    split_string = tosplit.split("_")
    patient = split_string[0]
    g_no = split_string[1]
    w = row['w']
    b = row['b']
    g = row['g']
    
    #selected
    interactome_file="reference/iref_nohub.tsv"
    prize_file=f"terminals/{patient}.tsv"

    graph = oi.Graph(interactome_file, {'w':w, 'b':b, 'g':g,})
    graph.prepare_prizes(prize_file)

    vertex_indices, edge_indices = graph.pcsf()
    forest, augmented_forest = graph.output_forest_as_networkx(vertex_indices, edge_indices)

    # removing self loops
    augmented_forest.remove_edges_from(nx.selfloop_edges(augmented_forest))
    forest.remove_edges_from(nx.selfloop_edges(forest))
    
    forests[tosplit]=augmented_forest

#combine networks

combined_graphs={}

for id in dirlist:
    g3=forests[f"{id}_3"]
    g4=forests[f"{id}_4"]
    
    combined_graph=nx.compose(g3,g4)
    
    #save
    oi.get_networkx_graph_as_dataframe_of_edges(combined_graph).to_csv(f'patients/{id}/{id}_edges.csv', sep=',', header=True, index=False)
    oi.get_networkx_graph_as_dataframe_of_nodes(combined_graph).to_csv(f'patients/{id}/{id}_nodes.csv', sep=',', header=True, index=True)
    oi.output_networkx_graph_as_interactive_html(combined_graph, output_dir=f'patients/{id}/', filename=f'{id}_network.html')
    nx.write_graphml(combined_graph, f'patients/{id}/{id}.graphml')
    
    nx.draw(combined_graph)
    plt.savefig(f'patients/{id}/{id}_mygraph.png')
    
    combined_graphs[id]=combined_graph
