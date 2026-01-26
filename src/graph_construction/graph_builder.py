from typing import List

from src.utils.dataclasses import (
    CanonicalEntity,
    RelationInstance,
    GraphNode,
    GraphEdge,
)


def build_graph(
    entities: List[CanonicalEntity],
    relations: List[RelationInstance],
    config: dict,
) -> tuple[List[GraphNode], List[GraphEdge]]:
    """
    Convert entities and relations into graph nodes and edges.
    """
    nodes: List[GraphNode] = []
    edges: List[GraphEdge] = []

    for entity in entities:
        node = GraphNode(
            node_id=entity.entity_id,
            label=entity.entity_type,
            properties={
                "name": entity.canonical_name,
                "aliases": entity.aliases,
            },
        )
        nodes.append(node)

    for relation in relations:
        edge = GraphEdge(
            source_id=relation.source_entity_id,
            target_id=relation.target_entity_id,
            relation_type=relation.relation_type,
            properties={
                "sentence_id": relation.sentence_id,
            },
        )
        edges.append(edge)

    return nodes, edges
