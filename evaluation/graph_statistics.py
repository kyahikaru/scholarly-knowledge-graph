from typing import List
from src.utils.dataclasses import CanonicalEntity, RelationInstance


def compute_graph_statistics(
    entities: List[CanonicalEntity],
    relations: List[RelationInstance],
):
    """
    Compute structural statistics for the knowledge graph.
    """

    nodes = len(entities)

    # Count unique edges (same logic as Neo4j MERGE)
    unique_edges = set(
        (r.source_entity_id, r.target_entity_id) for r in relations
    )

    edges = len(unique_edges)

    # Density for directed graph
    if nodes > 1:
        density = edges / (nodes * (nodes - 1))
    else:
        density = 0

    # Average degree
    if nodes > 0:
        avg_degree = (2 * edges) / nodes
    else:
        avg_degree = 0

    stats = {
        "nodes": nodes,
        "edges": edges,
        "density": density,
        "average_degree": avg_degree,
    }

    return stats
