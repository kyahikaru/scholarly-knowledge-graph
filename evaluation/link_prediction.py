from typing import List


def hits_at_k(ranks: List[int], k: int) -> float:
    """
    Compute Hits@K metric.
    ranks: list of ranks for the correct entity
    k: threshold
    """
    hits = sum(1 for r in ranks if r <= k)
    return hits / len(ranks)


def mean_reciprocal_rank(ranks: List[int]) -> float:
    """
    Compute Mean Reciprocal Rank (MRR).
    ranks: list of ranks for the correct entity
    """
    reciprocal_sum = sum(1 / r for r in ranks)
    return reciprocal_sum / len(ranks)


def evaluate_link_prediction(ranks: List[int]):

    metrics = {
        "MRR": mean_reciprocal_rank(ranks),
        "Hits@1": hits_at_k(ranks, 1),
        "Hits@3": hits_at_k(ranks, 3),
        "Hits@10": hits_at_k(ranks, 10)
    }

    return metrics
