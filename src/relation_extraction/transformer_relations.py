import logging
from typing import List

from transformers import pipeline

logger = logging.getLogger(__name__)


class TransformerRelationExtractor:

    def __init__(self, model_name="facebook/bart-large-mnli"):

        logger.info(f"Loading relation model {model_name}")

        self.classifier = pipeline(
            "zero-shot-classification",
            model=model_name
        )

        self.relation_labels = [
            "task uses dataset",
            "task evaluated on dataset",
            "task compared with task",
            "no relation"
        ]

    def __call__(self, sentences, entities, config):

        relations = []

        for sentence in sentences:

            for e1 in entities:
                for e2 in entities:

                    if e1 == e2:
                        continue

                    hypothesis = f"{e1.text} {e2.text}"

                    result = self.classifier(
                        sentence,
                        self.relation_labels
                    )

                    label = result["labels"][0]

                    if label != "no relation":

                        relations.append({
                            "source": e1.text,
                            "target": e2.text,
                            "type": label
                        })

        logger.info(f"Transformer relations extracted: {len(relations)}")

        return relations
