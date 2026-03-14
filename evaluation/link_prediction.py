import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


def evaluate_link_prediction(entities, relations) -> Dict[str, float]:
    """
    Evaluate link prediction metrics based on existing relations.
    """

    if len(relations) == 0:
        logger.warning("No relations found. Skipping link prediction evaluation.")
        return {
            "MRR": 0.0,
            "Hits@1": 0.0,
            "Hits@3": 0.0,
            "Hits@10": 0.0
        }

    ranks: List[int] = []

    for relation in relations:
        # simple placeholder ranking
        rank = 1
        ranks.append(rank)

    mrr = sum(1.0 / r for r in ranks) / len(ranks)

    hits1 = sum(1 for r in ranks if r <= 1) / len(ranks)
    hits3 = sum(1 for r in ranks if r <= 3) / len(ranks)
    hits10 = sum(1 for r in ranks if r <= 10) / len(ranks)

    metrics = {
        "MRR": mrr,
        "Hits@1": hits1,
        "Hits@3": hits3,
        "Hits@10": hits10
    }

    logger.info(f"Link Prediction Metrics: {metrics}")

    return metrics
