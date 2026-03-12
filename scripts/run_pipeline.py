from src.utils.config_loader import load_experiment_config
from src.ingestion.loader import load_documents
from evaluation.graph_statistics import compute_graph_statistics
from evaluation.link_prediction import evaluate_link_prediction
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
        password="NEO4J_PASSWORD"
    )

    writer.write_graph(entities, relations)
    writer.close()

    # Stage 9 — Graph statistics
    stats = compute_graph_statistics(entities, relations)

    print("\nGraph Statistics")
    print("----------------")
    print(f"Nodes: {stats['nodes']}")
    print(f"Edges: {stats['edges']}")
    print(f"Density: {stats['density']:.4f}")
    print(f"Average Degree: {stats['average_degree']:.2f}")

    # Stage 10 — Link prediction evaluation
    link_metrics = evaluate_link_prediction(entities, relations)

    print("\nLink Prediction Metrics")
    print("----------------------")
    print(f"MRR: {link_metrics['MRR']:.4f}")
    print(f"Hits@1: {link_metrics['Hits@1']:.4f}")
    print(f"Hits@3: {link_metrics['Hits@3']:.4f}")
    print(f"Hits@10: {link_metrics['Hits@10']:.4f}")

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

    print("\nPipeline completed.")
    print(f"Documents: {len(result.documents)}")
    print(f"Sentences: {len(result.sentences)}")
    print(f"Entities: {len(result.entities)}")
    print(f"Relations: {len(result.relations)}")
