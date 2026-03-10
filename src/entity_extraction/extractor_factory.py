from src.entity_extraction.rule_based_extractor import extract_entities


def get_extractor(config):
    backend = config["ner"]["backend"]

    if backend == "rule_based":
        return extract_entities

    raise ValueError(f"Unknown NER backend: {backend}")
