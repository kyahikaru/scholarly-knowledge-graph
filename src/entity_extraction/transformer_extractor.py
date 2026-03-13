import logging
from typing import List, Dict, Any

import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

logger = logging.getLogger(__name__)


class TransformerNERExtractor:

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

        logger.info("Transformer NER model loaded successfully")

    def __call__(self, sentences: List[str], config: Dict[str, Any]):

        mentions = []

        for sentence in sentences:

            entities = self.pipeline(sentence)

            for ent in entities:

                mention = {
                    "text": ent["word"],
                    "label": ent["entity_group"],
                    "score": float(ent["score"]),
                    "start": ent["start"],
                    "end": ent["end"],
                    "sentence": sentence
                }

                mentions.append(mention)

        logger.info(f"Transformer NER extracted {len(mentions)} mentions")

        return mentions
