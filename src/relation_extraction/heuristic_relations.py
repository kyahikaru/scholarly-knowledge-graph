from typing import List, Dict

from src.utils.dataclasses import (
    Sentence,
    CanonicalEntity,
    RelationInstance,
)


def extract_relations(
    sentences: List[Sentence],
    entities: List[CanonicalEntity],
    config: dict,
) -> List[RelationInstance]:
    """
    Heuristic relation extraction for MWP.
    Creates USED_ON relations when TASK and DATASET co-occur in a sentence.
    """

    relations: List[RelationInstance] = []
    relation_counter = 0

    entity_index: Dict[str, CanonicalEntity] = {
        e.canonical_name.lower(): e for e in entities
    }

    for sent in sentences:

        sent_text = sent.text.lower()

        tasks = [
            e for e in entity_index.values()
            if e.entity_type == "TASK" and e.canonical_name in sent_text
        ]

        datasets = [
            e for e in entity_index.values()
            if e.entity_type == "DATASET" and e.canonical_name in sent_text
        ]

        for task in tasks:
            for dataset in datasets:

                relation = RelationInstance(
                    relation_id=f"rel_{relation_counter}",
                    source_entity_id=task.entity_id,
                    target_entity_id=dataset.entity_id,
                    relation_type="USED_ON",
                    sentence_id=sent.sentence_id,
                )

                relations.append(relation)
                relation_counter += 1

    return relations
