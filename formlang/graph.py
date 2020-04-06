import networkx as nx


def read_graph_from_file(file_obj):
    graph = nx.DiGraph()
    for line in filter(bool, map(str.strip, file_obj)):
        u, symbol, v = line.split()
        graph.add_edge(int(u), int(v), symbol=symbol)
    return graph
