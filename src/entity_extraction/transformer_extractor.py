import logging
from typing import List, Dict, Any
import uuid

import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

from src.utils.dataclasses import EntityMention

logger = logging.getLogger(__name__)


class TransformerNERExtractor:
    """
    Transformer-based NER extractor using HuggingFace models
    with noise filtering.
    """

    def __init__(self, model_name: str):

        logger.info(f"Loading transformer NER model: {model_name}")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)

        self.device = 0 if torch.cuda.is_available() else -1

        self.pipeline = pipeline(
            "ner",
            model=self.model,
            tokenizer=self.tokenizer,
            aggregation_strategy="simple",
            device=self.device
        )

        # filtering parameters
        self.min_score = 0.60
        self.min_length = 3

        self.stopwords = {
            "the", "this", "that", "these", "those",
            "method", "model", "approach", "paper",
            "result", "results", "use", "using"
        }

        logger.info("Transformer NER model loaded successfully")

    def __call__(self, sentences: List[Any], config: Dict[str, Any]) -> List[EntityMention]:

        mentions: List[EntityMention] = []

        for sentence_obj in sentences:

            sentence_text = getattr(sentence_obj, "text", "")

            if not sentence_text or not sentence_text.strip():
                continue

            inputs = self.tokenizer(
                sentence_text,
                truncation=True,
                max_length=512,
                return_tensors="pt"
            )

            truncated_text = self.tokenizer.decode(
                inputs["input_ids"][0],
                skip_special_tokens=True
            )

            entities = self.pipeline(truncated_text)

            for ent in entities:

                word = ent["word"].strip().lower()
                score = ent.get("score", 0)

                # FILTER 1 — confidence
                if score < self.min_score:
                    continue

                # FILTER 2 — short tokens
                if len(word) < self.min_length:
                    continue

                # FILTER 3 — stopwords
                if word in self.stopwords:
                    continue

                mention = EntityMention(
                    mention_id=str(uuid.uuid4()),
                    sentence_id=sentence_obj.sentence_id,
                    doc_id=sentence_obj.doc_id,
                    text=word,
                    entity_type=ent["entity_group"],
                    start_char=ent["start"],
                    end_char=ent["end"]
                )

                mentions.append(mention)

        logger.info(f"Transformer NER extracted {len(mentions)} mentions")

        return mentions
