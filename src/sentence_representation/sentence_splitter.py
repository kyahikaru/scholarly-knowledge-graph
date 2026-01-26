from typing import List

import re

from src.utils.dataclasses import Document, Sentence


def split_into_sentences(documents: List[Document], config: dict) -> List[Sentence]:
    """
    Split document sections into sentences and create Sentence objects.
    """
    sentences: List[Sentence] = []
    sentence_counter = 0

    for doc in documents:
        for section_name, text in doc.sections.items():
            # Very simple sentence splitting (MWP-level)
            raw_sentences = re.split(r'(?<=[.!?])\s+', text)

            for raw_sentence in raw_sentences:
                cleaned = raw_sentence.strip()
                if not cleaned:
                    continue

                sent = Sentence(
                    sentence_id=f"sent_{sentence_counter}",
                    doc_id=doc.doc_id,
                    section=section_name,
                    text=cleaned
                )
                sentences.append(sent)
                sentence_counter += 1

    return sentences
