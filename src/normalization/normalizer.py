from typing import List, Dict
import re

from src.utils.dataclasses import (
    EntityMention,
    CanonicalEntity,
    EntityLink
)


STOP_ENTITIES = {
    "method",
    "approach",
    "system",
    "model",
    "paper",
    "result",
    "experiment",
    "technique",
    "task",
    "dataset"
}


def normalize_entities(
    mentions: List[EntityMention],
    config: dict
):

    entities: Dict[str, CanonicalEntity] = {}
    entity_links: List[EntityLink] = []

    entity_counter = 0

    frequency_counter: Dict[str, int] = {}

    # First pass: count frequencies
    for mention in mentions:

        normalized = re.sub(r"\W+", " ", mention.text.lower()).strip()

        if len(normalized) < 4:
            continue

        if normalized in STOP_ENTITIES:
            continue

        frequency_counter[normalized] = frequency_counter.get(normalized, 0) + 1


    for mention in mentions:

        normalized = re.sub(r"\W+", " ", mention.text.lower()).strip()

        if len(normalized) < 4:
            continue

        if normalized in STOP_ENTITIES:
            continue

        if frequency_counter.get(normalized, 0) < 2:
            continue

        if normalized not in entities:

            entity = CanonicalEntity(
                entity_id=f"ent_{entity_counter}",
                canonical_name=normalized,
                entity_type="CONCEPT",
                aliases=[normalized]
            )

            entities[normalized] = entity
            entity_counter += 1

        link = EntityLink(
            mention_id=mention.mention_id,
            entity_id=entities[normalized].entity_id
        )

        entity_links.append(link)

    return list(entities.values()), entity_links
