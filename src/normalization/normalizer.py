from typing import List, Dict
import re

from src.utils.dataclasses import EntityMention, CanonicalEntity, EntityLink


def normalize_entities(
    mentions: List[EntityMention],
    config: dict
) -> tuple[List[CanonicalEntity], List[EntityLink]]:
    """
    Basic normalization and deduplication for MWP.
    Improves canonicalization while preventing excessive merging.
    """

    canonical_entities: Dict[str, CanonicalEntity] = {}
    links: List[EntityLink] = []

    for mention in mentions:

        # Clean text but keep meaningful structure
        normalized_text = re.sub(r"\W+", " ", mention.text.lower()).strip()

        # Prevent extremely short tokens from collapsing entities
        if len(normalized_text) < 4:
            normalized_text = mention.text.lower().strip()

        key = f"{mention.entity_type}:{normalized_text}"

        if key not in canonical_entities:

            entity_id = f"entity_{len(canonical_entities)}"

            canonical_entities[key] = CanonicalEntity(
                entity_id=entity_id,
                canonical_name=normalized_text,
                entity_type=mention.entity_type,
                aliases=[mention.text],
            )

        else:
            # Avoid duplicate aliases
            if mention.text not in canonical_entities[key].aliases:
                canonical_entities[key].aliases.append(mention.text)

        link = EntityLink(
            mention_id=mention.mention_id,
            entity_id=canonical_entities[key].entity_id,
        )

        links.append(link)

    return list(canonical_entities.values()), links
