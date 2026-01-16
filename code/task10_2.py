from typing import List, Dict, Tuple
import networkx as nx

def solve_graph_cycle_removal_and_max_distance(file_content: str) -> Tuple[Dict, Dict]:
    lines = file_content.strip().split('\n')
    N = int(lines[0])
    nodes = lines[1:N+1]
    edges = []
    for line in lines[N+1:]:
        id_1, id_2, weight = line.split()
        edges.append((id_1, id_2, int(weight)))

    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_weighted_edges_from(edges)

    # Identify all Minimum Feedback Edge Sets (FES) candidates
    fes_candidates = []
    for cycle in nx.simple_cycles(G):
        cycle_edges = [(cycle[i], cycle[i+1]) for i in range(len(cycle)-1)] + [(cycle[-1], cycle[0])]
        fes_candidates.append(set(cycle_edges))

    # Select the FES candidate with the maximum total weight
    if fes_candidates:
        max_weight_fes = max(fes_candidates, key=lambda x: sum(G[id_1][id_2]['weight'] for id_1, id_2 in x))
        G.remove_edges_from(max_weight_fes)

    # Transform the remaining graph into a Directed Acyclic Graph (DAG)
    dag = G.copy()

    # Calculate the maximum distances (longest paths) from every source node to all other reachable nodes in the DAG
    max_distances = {}
    for node in nodes:
        longest_paths = nx.dag_longest_path_length(dag, source=node)
        max_distances[node] = longest_paths

    return dag.adjacency(), max_distances

from typing import List, Dict, Tuple
import networkx as nx

def solve_graph_cycle_removal_and_max_distance(file_content: str) -> Tuple[Dict, Dict]:
    lines = file_content.strip().split('\n')
    N = int(lines[0])
    nodes = lines[1:N+1]
    edges = []
    for line in lines[N+1:]:
        id_1, id_2, weight = line.split()
        edges.append((id_1, id_2, int(weight)))

    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_weighted_edges_from(edges)