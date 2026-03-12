from typing import List, Tuple
import random

from src.utils.dataclasses import CanonicalEntity, RelationInstance


def build_edge_set(relations: List[RelationInstance]) -> set:
    """
    Build set of unique edges from relations.
    """
    return set((r.source_entity_id, r.target_entity_id) for r in relations)


def generate_negative_samples(
    entities: List[CanonicalEntity],
    edge_set: set,
    num_samples: int
) -> List[Tuple[str, str]]:
    """
    Generate negative edges not present in graph.
    """

    negatives = []
    entity_ids = [e.entity_id for e in entities]

    while len(negatives) < num_samples:
        source = random.choice(entity_ids)
        target = random.choice(entity_ids)

        if source != target and (source, target) not in edge_set:
            negatives.append((source, target))

    return negatives


def evaluate_link_prediction(
    entities: List[CanonicalEntity],
    relations: List[RelationInstance],
):

    edge_set = build_edge_set(relations)

    positive_edges = list(edge_set)

    negative_edges = generate_negative_samples(
        entities,
        edge_set,
        len(positive_edges)
    )

    # Simple scoring heuristic
    # score = 1 if edge exists else 0

    ranks = []

    for pos in positive_edges:

        candidates = [pos] + negative_edges
        random.shuffle(candidates)

        scores = []

        for edge in candidates:
            if edge in edge_set:
                scores.append((edge, 1))
            else:
                scores.append((edge, 0))

        scores.sort(key=lambda x: x[1], reverse=True)

        rank = [e for e, _ in scores].index(pos) + 1
        ranks.append(rank)

    # Compute metrics
    mrr = sum(1 / r for r in ranks) / len(ranks)

    hits1 = sum(1 for r in ranks if r <= 1) / len(ranks)
    hits3 = sum(1 for r in ranks if r <= 3) / len(ranks)
    hits10 = sum(1 for r in ranks if r <= 10) / len(ranks)

    return {
        "MRR": mrr,
        "Hits@1": hits1,
        "Hits@3": hits3,
        "Hits@10": hits10,
    }
