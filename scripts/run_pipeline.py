import os

from src.utils.config_loader import load_experiment_config
from src.ingestion.loader import load_documents
from src.preprocessing.pdf_preprocessor import preprocess_documents
from src.sentence_representation.sentence_splitter import split_into_sentences
from src.entity_extraction.extractor_factory import get_extractor
from src.normalization.normalizer import normalize_entities
from src.relation_extraction.heuristic_relations import extract_relations
from src.graph_construction.graph_builder import build_graph
from src.graph_construction.neo4j_writer import Neo4jWriter
from src.utils.dataclasses import PipelineResult


def run_pipeline(experiment_config_path: str) -> PipelineResult:

    config = load_experiment_config(experiment_config_path)

    # Stage 1 — Load documents
    documents = load_documents(config)

    # Stage 2 — Preprocess PDFs
    documents = preprocess_documents(documents, config)

    # Stage 3 — Sentence splitting
    sentences = split_into_sentences(documents, config)

    # Stage 4 — Entity extraction
    extractor = get_extractor(config)
    mentions = extractor(sentences, config)

    # Stage 5 — Entity normalization
    entities, entity_links = normalize_entities(mentions, config)

    # Stage 6 — Relation extraction
    relations = extract_relations(sentences, entities, config)

    # Stage 7 — Build graph objects
    nodes, edges = build_graph(entities, relations, config)

    # Stage 8 — Write graph to Neo4j
    writer = Neo4jWriter(
        uri="neo4j://127.0.0.1:7687",
        user="neo4j",
        password=os.getenv("NEO4J_PASSWORD")
    )

    writer.write_graph(entities, relations)
    writer.close()

    result = PipelineResult(
        documents=documents,
        sentences=sentences,
        mentions=mentions,
        entities=entities,
        relations=relations,
    )

    return result


if __name__ == "__main__":

    result = run_pipeline("configs/experiments/dev.yaml")

    print("Pipeline completed.")
    print(f"Documents: {len(result.documents)}")
    print(f"Sentences: {len(result.sentences)}")
    print(f"Entities: {len(result.entities)}")
    print(f"Relations: {len(result.relations)}")
