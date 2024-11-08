import backboning
import projection
import networkx as nx
import pandas as pd
from networkx.algorithms import resource_allocation_index

projections ={
    "simple":projection.simple,
    "hyperbolic":projection.hyperbolic,
    "pearson":projection.pearson,
    'resource_allocation': resource_allocation_index,
}
backbonings={
    "noise_corrected":backboning.noise_corrected,
    "high_salience_skeleton":backboning.high_salience_skeleton,
    "doubly_stochastic":backboning.doubly_stochastic,
    "disparity_filter":backboning.disparity_filter
}

projection_methods = {
    'simple': {'function': projection.simple,
               'backbonings': {'noise_corrected':backboning.noise_corrected, 'doubly_stochastic': backboning.doubly_stochastic, 'disparity_filter': backboning.disparity_filter}},
    'hyperbolic': {'function': projection.hyperbolic,
                   'backbonings': {'high_salience_skeleton': backboning.high_salience_skeleton}},
    'resource_allocation': {'function': resource_allocation_index,
                            'backbonings': {'doubly_stochastic':backboning.doubly_stochastic}},
    'pearson': {'function': projection.pearson,
                'backbonings': {'noise_corrected':backboning.noise_corrected}}
}
#convex network reduction missing

G=nx.read_edgelist("data/edges.csv",delimiter=",",nodetype=int)
#get sets of nodes (animal, parasite)
nodes = pd.read_csv("data/nodes.csv",delimiter=",")
animal_nodes = list(set(nodes[nodes[" is_host"]==1]["# index"]))
parasite_nodes = list(set(nodes[nodes[" is_host"]==0]["# index"]))


# function is needed to convert graph to df for backboning (with predefined function)
def graph_to_dataframe(graph):
    edges = nx.to_pandas_edgelist(graph)
    edges.rename(columns={'source': 'src', 'target': 'trg', 'weight': 'nij'}, inplace=True)
    return edges


for key,method in projection_methods.items():
    projected_network = method['function'](G,animal_nodes)
    edges_df = graph_to_dataframe(projected_network)
    for label, backboning in method['backbonings'].items():
        result = backboning(edges_df)
        result.to_csv(f"projections_with_backbonings/{key}_{label}.csv")

