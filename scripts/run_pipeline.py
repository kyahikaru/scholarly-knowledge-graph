from src.utils.config_loader import load_experiment_config
from src.ingestion.loader import load_documents
from src.preprocessing.pdf_preprocessor import preprocess_documents
from src.sentence_representation.sentence_splitter import split_into_sentences
from src.entity_extraction.rule_based_extractor import extract_entities
from src.normalization.normalizer import normalize_entities
from src.relation_extraction.heuristic_relations import extract_relations
from src.graph_construction.graph_builder import build_graph
from src.utils.dataclasses import PipelineResult


def run_pipeline(experiment_config_path: str) -> PipelineResult:
    # Load merged configuration
    config = load_experiment_config(experiment_config_path)

    # Stage 1: Ingestion
    documents = load_documents(config)

    # Stage 2: Preprocessing
    documents = preprocess_documents(documents, config)

    # Stage 3: Sentence representation
    sentences = split_into_sentences(documents, config)

    # Stage 4: Entity extraction
    mentions = extract_entities(sentences, config)

    # Stage 5: Normalization
    entities, entity_links = normalize_entities(mentions, config)

    # Stage 6: Relation extraction
    relations = extract_relations(sentences, entities, config)

    # Stage 7: Graph preparation
    nodes, edges = build_graph(entities, relations, config)

    # Final assembled result
    result = PipelineResult(
        documents=documents,
        sentences=sentences,
        mentions=mentions,
        entities=entities,
        relations=relations,
    )

    return result


if __name__ == "__main__":
    # Example run (path can be changed later)
    result = run_pipeline("configs/experiments/dev.yaml")

    print("Pipeline completed.")
    print(f"Documents: {len(result.documents)}")
    print(f"Sentences: {len(result.sentences)}")
    print(f"Entities: {len(result.entities)}")
    print(f"Relations: {len(result.relations)}")
