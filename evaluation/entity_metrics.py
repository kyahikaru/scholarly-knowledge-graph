from typing import List, Dict


def precision(tp: int, fp: int) -> float:
    if tp + fp == 0:
        return 0.0
    return tp / (tp + fp)


def recall(tp: int, fn: int) -> float:
    if tp + fn == 0:
        return 0.0
    return tp / (tp + fn)


def f1_score(p: float, r: float) -> float:
    if p + r == 0:
        return 0.0
    return 2 * (p * r) / (p + r)


def evaluate_entities(predicted_entities: List[str], gold_entities: List[str]) -> Dict:

    predicted_set = set(predicted_entities)
    gold_set = set(gold_entities)

    tp = len(predicted_set & gold_set)
    fp = len(predicted_set - gold_set)
    fn = len(gold_set - predicted_set)

    p = precision(tp, fp)
    r = recall(tp, fn)
    f1 = f1_score(p, r)

    return {
        "precision": p,
        "recall": r,
        "f1_score": f1,
        "true_positive": tp,
        "false_positive": fp,
        "false_negative": fn
    }
