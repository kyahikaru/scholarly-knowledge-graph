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
    Heuristic relation extractor with relation limiting.

    Creates CO_OCCURS_WITH relations for entities appearing
    in the same sentence but caps the number of relations
    per sentence to prevent graph explosion.
    """

    relations: List[RelationInstance] = []
    relation_counter = 0

    entity_index: Dict[str, CanonicalEntity] = {
        e.canonical_name.lower(): e for e in entities
    }

    MAX_ENTITIES_PER_SENTENCE = 3

    for sent in sentences:

        sent_text = sent.text.lower()

        entities_in_sentence = [
            e for e in entity_index.values()
            if e.canonical_name.lower() in sent_text
        ]

        # Limit entities per sentence
        entities_in_sentence = entities_in_sentence[:MAX_ENTITIES_PER_SENTENCE]

        for i in range(len(entities_in_sentence)):
            for j in range(i + 1, len(entities_in_sentence)):

                source = entities_in_sentence[i]
                target = entities_in_sentence[j]

                relation = RelationInstance(
                    relation_id=f"rel_{relation_counter}",
                    source_entity_id=source.entity_id,
                    target_entity_id=target.entity_id,
                    relation_type="CO_OCCURS_WITH",
                    sentence_id=sent.sentence_id,
                )

                relations.append(relation)
                relation_counter += 1

    return relations
