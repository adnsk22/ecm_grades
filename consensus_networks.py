# -*- coding: utf-8 -*-
"""
Created on Tue May 28 15:01:45 2024

@author: MONSTER
"""

import os
import pandas as pd
import networkx as nx
from collections import Counter

os.chdir("C:/Users/MONSTER/OneDrive - Koc Universitesi/THESIS/ecm_grades_codes")

clusters=pd.read_csv("out_data/lists/momix_clusters.csv")

poorest=clusters.loc[clusters["ecm_type"]=="poorest","patients"].tolist()
poor=clusters.loc[clusters["ecm_type"]=="poor","patients"].tolist()
rich=clusters.loc[clusters["ecm_type"]=="rich","patients"].tolist()
richest=clusters.loc[clusters["ecm_type"]=="richest","patients"].tolist()

poorest_ntwx=dict()
for i in poorest: 
    n1=nx.read_graphml(f"../patients/{i}/{i}.graphml")
    edges_to_remove1 = [(u, v) for u, v, attr in n1.edges(data=True) if not attr.get('in_solution', False)]
    n1.remove_edges_from(edges_to_remove1)
    poorest_ntwx[f"{i}"]=n1

poor_ntwx=dict()
for i in poor: 
    n1=nx.read_graphml(f"../patients/{i}/{i}.graphml")
    edges_to_remove1 = [(u, v) for u, v, attr in n1.edges(data=True) if not attr.get('in_solution', False)]
    n1.remove_edges_from(edges_to_remove1)
    poor_ntwx[f"{i}"]=n1
    
rich_ntwx=dict()    
for i in rich: 
    n1=nx.read_graphml(f"../patients/{i}/{i}.graphml")
    edges_to_remove1 = [(u, v) for u, v, attr in n1.edges(data=True) if not attr.get('in_solution', False)]
    n1.remove_edges_from(edges_to_remove1)
    rich_ntwx[f"{i}"]=n1

richest_ntwx=dict()
for i in richest: 
    n1=nx.read_graphml(f"../patients/{i}/{i}.graphml")
    edges_to_remove1 = [(u, v) for u, v, attr in n1.edges(data=True) if not attr.get('in_solution', False)]
    n1.remove_edges_from(edges_to_remove1)
    richest_ntwx[f"{i}"]=n1

ntwrks = {"poorest":poorest_ntwx, "poor":poor_ntwx, "rich":rich_ntwx, "richest":richest_ntwx}


final_data_on_consensus = []

for ecm_type_name, clus_dict in ntwrks.items() : 
    
    for k in range(0,len(clus_dict.keys())) : 
        
        edge_frequency = Counter()
        
        for graph_name, graph in clus_dict.items() :
            for edge in graph.edges() :
                normalized_edge = tuple(sorted(edge))
                edge_frequency[normalized_edge] += 1
                
        edges_to_remove = {edge for edge, count in edge_frequency.items() if count <= k}
                
        updated_graphs = {}
        
        for graph_name, graph in clus_dict.items() :
            updated_graph=graph.copy()
            for edge in list(updated_graph.edges()) :
                normalized_edge = tuple(sorted(edge))
                if normalized_edge in edges_to_remove :
                    updated_graph.remove_edge(*edge)
            updated_graphs[graph_name] = updated_graph
                
        component_data = {}
        
        for graph_name, graph in updated_graphs.items() :
            connected_components = list(nx.connected_components(graph))
            data = []
            for i in range(len(connected_components)) :
                nodes = connected_components[i] 
                size = len(connected_components[i])
                total = len(graph.nodes())
                data.append({"size":size, "nodes":nodes, "total_nodes":total})           
            component_data[graph_name] = pd.DataFrame(data)
            
        final_data = []
        
        for patient, df in component_data.items() :
            total_nodes = df["total_nodes"].max()
            highest_size = df["size"].max()
            first = df[df["size"] == highest_size].nodes.tolist()
            second_highest_size = df[df["size"] < highest_size]["size"].max()
            second = df[df["size"] == second_highest_size].nodes.tolist()
            singleton_count = df[df["size"]==1].shape[0]
            component_count = df.shape[0]
            final_data.append({"patient":patient,
                                       "total_nodes":total_nodes, 
                                       "components":component_count, 
                                       "singletons":singleton_count, 
                                       "largest_component":highest_size, 
                                       "largest_nodes":first,
                                       "second_largest_component":second_highest_size,
                                       "second_largest_nodes":second})
            
        final_dataframe = pd.DataFrame(final_data)
        
        consensus = nx.Graph()
        
        for graph_name, graph in updated_graphs.items() :
            consensus = nx.compose(consensus, graph)
            
        connected_components = list(nx.connected_components(consensus))
        
        data = []
        
        for i in range(len(connected_components)) : 
            nodes = connected_components[i] 
            size = len(connected_components[i])
            data.append({"size":size, "nodes":nodes}) 
            
        data_on_consensus = pd.DataFrame(data)
        
        consensus_type = f"below_{k}"  
        total_nodes = len(consensus.nodes())
        component_count = data_on_consensus.shape[0]
        singleton_count = data_on_consensus[data_on_consensus["size"]==1].shape[0]
        highest_size = data_on_consensus["size"].max()
        first = data_on_consensus[data_on_consensus["size"] == highest_size].nodes.tolist()
        second_highest_size = data_on_consensus[data_on_consensus["size"] < highest_size]["size"].max()
        second = data_on_consensus[data_on_consensus["size"] == second_highest_size].nodes.tolist()
    
    
        final_data_on_consensus.append({"ecm_type":ecm_type_name,
                                   "consensus_type":consensus_type,
                                   "total_nodes":total_nodes, 
                                   "components":component_count, 
                                   "singletons":singleton_count, 
                                   "largest_component":highest_size, 
                                   "largest_nodes":first,
                                   "second_largest_component":second_highest_size,
                                   "second_largest_nodes":second})

df = pd.DataFrame(final_data_on_consensus)

def clean_largest_nodes(value):
    if isinstance(value, list) and len(value) > 0:
        node_set = value[0]
        if isinstance(node_set, set):
            return ";".join(node_set)
    return ""

# Apply the function to the 'largest_nodes' column
df['largest_nodes'] = df['largest_nodes'].apply(clean_largest_nodes)
        
#df.to_csv('out_data/network_data/consensus_insol/consensus_metrics_insol.csv', index=False)

    
""" Get consensus graph for poorest """
    
edge_frequency = Counter()
    
for graph_name, graph in poorest_ntwx.items() :
    for edge in graph.edges() :
        normalized_edge = tuple(sorted(edge)) 
        edge_frequency[normalized_edge] += 1
            
edges_to_remove = {edge for edge, count in edge_frequency.items() if count <= 6}
            
updated_graphs = {}
    
for graph_name, graph in poorest_ntwx.items() :
    updated_graph=graph.copy()
    for edge in list(updated_graph.edges()) :
        normalized_edge = tuple(sorted(edge))
        if normalized_edge in edges_to_remove :
            updated_graph.remove_edge(*edge)
    updated_graphs[graph_name] = updated_graph

consensus = nx.Graph()

for graph_name, graph in updated_graphs.items() :
    consensus = nx.compose(consensus, graph)       
     
# Get connected components
connected_components = list(nx.connected_components(consensus))

# Check if everything is right
data = []

for i in range(len(connected_components)) : 
    nodes = connected_components[i]
    size = len(connected_components[i])
    data.append({"size":size, "nodes":nodes})        
    
    data_on_consensus = pd.DataFrame(data)
    
    total_nodes = len(consensus.nodes())
    component_count = data_on_consensus.shape[0]
    singleton_count = data_on_consensus[data_on_consensus["size"]==1].shape[0]
    highest_size = data_on_consensus["size"].max()
    first = data_on_consensus[data_on_consensus["size"] == highest_size].nodes.tolist()
    second_highest_size = data_on_consensus[data_on_consensus["size"] < highest_size]["size"].max()
    second = data_on_consensus[data_on_consensus["size"] == second_highest_size].nodes.tolist()

print(total_nodes, component_count, singleton_count, highest_size, second_highest_size, second )
        
# Find the largest connected component
largest_cc = max(connected_components, key=len)

# Extract the subgraph corresponding to the largest connected component
largest_cc_subgraph = consensus.subgraph(largest_cc).copy()        
       
for edge, freq in edge_frequency.items():
    if largest_cc_subgraph.has_edge(*edge):
        largest_cc_subgraph[edge[0]][edge[1]]['frequency'] = freq
    else:
        print(f"Edge {edge} not found in the graph.")  

for u, v, attrs in largest_cc_subgraph.edges(data=True):
    print((u, v), attrs)
    
for u, attrs in largest_cc_subgraph.nodes(data=True):
    print(u, attrs)

nx.write_graphml(largest_cc_subgraph, "out_data/network_data/consensus_insol/consensus_poorest.graphml")


""" Get consensus graph for poor """
    
edge_frequency = Counter()
    
for graph_name, graph in poor_ntwx.items() :
    for edge in graph.edges() :
        normalized_edge = tuple(sorted(edge)) 
        edge_frequency[normalized_edge] += 1
            
edges_to_remove = {edge for edge, count in edge_frequency.items() if count <= 11}
            
updated_graphs = {}
    
for graph_name, graph in poor_ntwx.items() :
    updated_graph=graph.copy()
    for edge in list(updated_graph.edges()) :
        normalized_edge = tuple(sorted(edge))
        if normalized_edge in edges_to_remove :
            updated_graph.remove_edge(*edge)
    updated_graphs[graph_name] = updated_graph

consensus = nx.Graph()

for graph_name, graph in updated_graphs.items() :
    consensus = nx.compose(consensus, graph)       
     
# Get connected components
connected_components = list(nx.connected_components(consensus))

# Check if everything is right
data = []

for i in range(len(connected_components)) : 
    nodes = connected_components[i]
    size = len(connected_components[i])
    data.append({"size":size, "nodes":nodes})        
    
    data_on_consensus = pd.DataFrame(data)
    
    total_nodes = len(consensus.nodes())
    component_count = data_on_consensus.shape[0]
    singleton_count = data_on_consensus[data_on_consensus["size"]==1].shape[0]
    highest_size = data_on_consensus["size"].max()
    first = data_on_consensus[data_on_consensus["size"] == highest_size].nodes.tolist()
    second_highest_size = data_on_consensus[data_on_consensus["size"] < highest_size]["size"].max()
    second = data_on_consensus[data_on_consensus["size"] == second_highest_size].nodes.tolist()

print(total_nodes, component_count, singleton_count, highest_size, second_highest_size, second )
        
# Find the largest connected component
largest_cc = max(connected_components, key=len)

# Extract the subgraph corresponding to the largest connected component
largest_cc_subgraph = consensus.subgraph(largest_cc).copy()        
       
for edge, freq in edge_frequency.items():
    if largest_cc_subgraph.has_edge(*edge):
        largest_cc_subgraph[edge[0]][edge[1]]['frequency'] = freq
    else:
        print(f"Edge {edge} not found in the graph.")  

for u, v, attrs in largest_cc_subgraph.edges(data=True):
    print((u, v), attrs)
    
for u, attrs in largest_cc_subgraph.nodes(data=True):
    print(u, attrs)

nx.write_graphml(largest_cc_subgraph, "out_data/network_data/consensus_insol/consensus_poor.graphml")


""" Get consensus graph for rich """
    
edge_frequency = Counter()
    
for graph_name, graph in rich_ntwx.items() :
    for edge in graph.edges() :
        normalized_edge = tuple(sorted(edge)) 
        edge_frequency[normalized_edge] += 1
            
edges_to_remove = {edge for edge, count in edge_frequency.items() if count <= 10}
            
updated_graphs = {}
    
for graph_name, graph in rich_ntwx.items() :
    updated_graph=graph.copy()
    for edge in list(updated_graph.edges()) :
        normalized_edge = tuple(sorted(edge))
        if normalized_edge in edges_to_remove :
            updated_graph.remove_edge(*edge)
    updated_graphs[graph_name] = updated_graph

consensus = nx.Graph()

for graph_name, graph in updated_graphs.items() :
    consensus = nx.compose(consensus, graph)       
     
# Get connected components
connected_components = list(nx.connected_components(consensus))

# Check if everything is right
data = []

for i in range(len(connected_components)) : 
    nodes = connected_components[i]
    size = len(connected_components[i])
    data.append({"size":size, "nodes":nodes})        
    
    data_on_consensus = pd.DataFrame(data)
    
    total_nodes = len(consensus.nodes())
    component_count = data_on_consensus.shape[0]
    singleton_count = data_on_consensus[data_on_consensus["size"]==1].shape[0]
    highest_size = data_on_consensus["size"].max()
    first = data_on_consensus[data_on_consensus["size"] == highest_size].nodes.tolist()
    second_highest_size = data_on_consensus[data_on_consensus["size"] < highest_size]["size"].max()
    second = data_on_consensus[data_on_consensus["size"] == second_highest_size].nodes.tolist()

print(total_nodes, component_count, singleton_count, highest_size, second_highest_size, second )
        
# Find the largest connected component
largest_cc = max(connected_components, key=len)

# Extract the subgraph corresponding to the largest connected component
largest_cc_subgraph = consensus.subgraph(largest_cc).copy()        
       
for edge, freq in edge_frequency.items():
    if largest_cc_subgraph.has_edge(*edge):
        largest_cc_subgraph[edge[0]][edge[1]]['frequency'] = freq
    else:
        print(f"Edge {edge} not found in the graph.")  

for u, v, attrs in largest_cc_subgraph.edges(data=True):
    print((u, v), attrs)
    
for u, attrs in largest_cc_subgraph.nodes(data=True):
    print(u, attrs)

nx.write_graphml(largest_cc_subgraph, "out_data/network_data/consensus_insol/consensus_rich.graphml")


""" Get consensus graph for richest """
    
edge_frequency = Counter()
    
for graph_name, graph in richest_ntwx.items() :
    for edge in graph.edges() :
        normalized_edge = tuple(sorted(edge)) 
        edge_frequency[normalized_edge] += 1
            
edges_to_remove = {edge for edge, count in edge_frequency.items() if count <= 4}
            
updated_graphs = {}
    
for graph_name, graph in richest_ntwx.items() :
    updated_graph=graph.copy()
    for edge in list(updated_graph.edges()) :
        normalized_edge = tuple(sorted(edge))
        if normalized_edge in edges_to_remove :
            updated_graph.remove_edge(*edge)
    updated_graphs[graph_name] = updated_graph

consensus = nx.Graph()

for graph_name, graph in updated_graphs.items() :
    consensus = nx.compose(consensus, graph)       
     
# Get connected components
connected_components = list(nx.connected_components(consensus))

# Check if everything is right
data = []

for i in range(len(connected_components)) : 
    nodes = connected_components[i]
    size = len(connected_components[i])
    data.append({"size":size, "nodes":nodes})        
    
    data_on_consensus = pd.DataFrame(data)
    
    total_nodes = len(consensus.nodes())
    component_count = data_on_consensus.shape[0]
    singleton_count = data_on_consensus[data_on_consensus["size"]==1].shape[0]
    highest_size = data_on_consensus["size"].max()
    first = data_on_consensus[data_on_consensus["size"] == highest_size].nodes.tolist()
    second_highest_size = data_on_consensus[data_on_consensus["size"] < highest_size]["size"].max()
    second = data_on_consensus[data_on_consensus["size"] == second_highest_size].nodes.tolist()

print(total_nodes, component_count, singleton_count, highest_size, second_highest_size, second )
        
# Find the largest connected component
largest_cc = max(connected_components, key=len)

# Extract the subgraph corresponding to the largest connected component
largest_cc_subgraph = consensus.subgraph(largest_cc).copy()        
       
for edge, freq in edge_frequency.items():
    if largest_cc_subgraph.has_edge(*edge):
        largest_cc_subgraph[edge[0]][edge[1]]['frequency'] = freq
    else:
        print(f"Edge {edge} not found in the graph.")  

for u, v, attrs in largest_cc_subgraph.edges(data=True):
    print((u, v), attrs)
    
for u, attrs in largest_cc_subgraph.nodes(data=True):
    print(u, attrs)

nx.write_graphml(largest_cc_subgraph, "out_data/network_data/consensus_insol/consensus_richest.graphml")



        
        

