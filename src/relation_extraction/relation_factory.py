from src.relation_extraction.heuristic_relations import extract_relations
from src.relation_extraction.transformer_relations import TransformerRelationExtractor


def get_relation_extractor(config):

    backend = config.get("pipeline", {}).get("relation_extraction", "heuristic")

    if backend == "heuristic":
        return extract_relations

    if backend == "transformer":

        model_name = config.get("models", {}).get("relation_extraction", {}).get(
            "transformer_model",
            "facebook/bart-large-mnli"
        )

        return TransformerRelationExtractor(model_name)

    raise ValueError(f"Unknown relation extraction backend: {backend}")
