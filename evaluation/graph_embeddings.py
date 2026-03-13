from node2vec import Node2Vec
import networkx as nx


def compute_graph_embeddings(entities, relations):

    G = nx.Graph()

    # Add nodes
    for e in entities:
        G.add_node(e.entity_id)

    # Add edges
    for r in relations:
        G.add_edge(r.source_entity_id, r.target_entity_id)

    node2vec = Node2Vec(
        G,
        dimensions=64,
        walk_length=10,
        num_walks=50,
        workers=1
    )

    model = node2vec.fit(window=5, min_count=1)

    embeddings = {
        node: model.wv[node]
        for node in G.nodes()
    }

    return embeddings
