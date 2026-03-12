def compute_graph_statistics(entities, relations):

    num_nodes = len(entities)
    num_edges = len(relations)

    # Graph density for directed graph
    if num_nodes <= 1:
        density = 0
    else:
        density = num_edges / (num_nodes * (num_nodes - 1))

    # Average degree
    if num_nodes == 0:
        avg_degree = 0
    else:
        avg_degree = (2 * num_edges) / num_nodes

    stats = {
        "nodes": num_nodes,
        "edges": num_edges,
        "density": density,
        "average_degree": avg_degree
    }

    return stats
