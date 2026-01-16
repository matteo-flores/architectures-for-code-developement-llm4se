from typing import List, Dict, Tuple
import networkx as nx

def solve_graph_cycle_removal_and_max_distance(file_content: str) -> Tuple[Dict, Dict]:
    lines = file_content.strip().split('\n')
    N = int(lines[0])
    nodes = lines[1:N+1]
    edges = [line.split() for line in lines[N+1:]]

    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_weighted_edges_from(edges)

    cycles = list(nx.simple_cycles(G))
    if not cycles:
        return {node: [(neighbor, weight) for neighbor, weight in G[node].items()] for node in G}, {}

    fes_candidates = []
    for cycle in cycles:
        cycle_edges = [(cycle[i], cycle[i+1]) for i in range(len(cycle)-1)] + [(cycle[-1], cycle[0])]
        fes = set()
        for u, v in cycle_edges:
            fes.add((u, v))
        fes_candidates.append((fes, sum(G[u][v]['weight'] for u, v in fes)))

    fes_candidates.sort(key=lambda x: (-x[1], len(x[0])))
    selected_fes = fes_candidates[0][0]

    G.remove_edges_from(selected_fes)

    dag_adj_list = {node: [(neighbor, weight) for neighbor, weight in G[node].items()] for node in G}
    max_distances = {}

    for node in G.nodes():
        try:
            longest_paths = dict(nx.single_source_dijkstra_path_length(G, node, weight='weight'))
            max_distances[node] = longest_paths
        except nx.NetworkXNoPath:
            max_distances[node] = {}

    return dag_adj_list, max_distances