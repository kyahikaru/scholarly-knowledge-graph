from src.entity_extraction.rule_based_extractor import extract_entities as rule_based
from src.entity_extraction.bilstm_crf_extractor import extract_entities as bilstm_crf


def get_extractor(config):

    backend = config["ner"]["backend"]

    if backend == "rule_based":
        return rule_based

    if backend == "bilstm_crf":
        return bilstm_crf

    raise ValueError(f"Unknown NER backend: {backend}")
