from typing import List
import re

from src.utils.dataclasses import Sentence, EntityMention


TASK_PATTERNS = [
    r"named entity recognition",
    r"part-of-speech tagging",
    r"machine translation",
    r"sentiment analysis",
]

DATASET_PATTERNS = [
    r"conll[- ]?2003",
    r"ontonotes",
    r"imdb",
    r"squad",
]


def extract_entities(sentences: List[Sentence], config: dict) -> List[EntityMention]:
    """
    Rule-based entity extraction for MWP.
    """
    mentions: List[EntityMention] = []
    mention_counter = 0

    for sent in sentences:
        text_lower = sent.text.lower()

        # TASK entities
        for pattern in TASK_PATTERNS:
            for match in re.finditer(pattern, text_lower):
                mention = EntityMention(
                    mention_id=f"mention_{mention_counter}",
                    sentence_id=sent.sentence_id,
                    doc_id=sent.doc_id,
                    text=sent.text[match.start():match.end()],
                    entity_type="TASK",
                    start_char=match.start(),
                    end_char=match.end(),
                )
                mentions.append(mention)
                mention_counter += 1

        # DATASET entities
        for pattern in DATASET_PATTERNS:
            for match in re.finditer(pattern, text_lower):
                mention = EntityMention(
                    mention_id=f"mention_{mention_counter}",
                    sentence_id=sent.sentence_id,
                    doc_id=sent.doc_id,
                    text=sent.text[match.start():match.end()],
                    entity_type="DATASET",
                    start_char=match.start(),
                    end_char=match.end(),
                )
                mentions.append(mention)
                mention_counter += 1

    return mentions
