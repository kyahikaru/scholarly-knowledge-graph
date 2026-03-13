import yaml
import logging
import time
import os

from src.utils.logging_config import setup_logging
from src.utils.config_loader import load_experiment_config
from src.ingestion.loader import load_documents
from evaluation.graph_statistics import compute_graph_statistics
from evaluation.link_prediction import evaluate_link_prediction
from evaluation.graph_embeddings import compute_graph_embeddings
from src.preprocessing.pdf_preprocessor import preprocess_documents
from src.sentence_representation.sentence_splitter import split_into_sentences
from src.entity_extraction.extractor_factory import get_extractor
from src.normalization.normalizer import normalize_entities
from src.relation_extraction.relation_factory import get_relation_extractor
from src.graph_construction.graph_builder import build_graph
from src.graph_construction.neo4j_writer import Neo4jWriter
from src.utils.dataclasses import PipelineResult
from src.utils.cache import cache_exists, load_cache, save_cache

logger = logging.getLogger(__name__)


def timed_stage(stage_name, func, *args):
    start = time.perf_counter()
    result = func(*args)
    duration = time.perf_counter() - start
    logger.info(f"{stage_name} completed in {duration:.3f} seconds")
    return result


def run_pipeline(experiment_config_path: str, pipeline_config: dict) -> PipelineResult:

    config = load_experiment_config(experiment_config_path)

    cache_cfg = pipeline_config.get("cache", {})
    ner_cache_path = cache_cfg.get("ner_mentions")

    logger.info("Stage 1 — Loading documents")
    documents = timed_stage(
        "Stage 1 — Loading documents",
        load_documents,
        config
    )

    logger.info("Stage 2 — Preprocessing PDFs")
    documents = timed_stage(
        "Stage 2 — Preprocessing PDFs",
        preprocess_documents,
        documents,
        config
    )

    logger.info("Stage 3 — Sentence splitting")
    sentences = timed_stage(
        "Stage 3 — Sentence splitting",
        split_into_sentences,
        documents,
        config
    )

    logger.info("Stage 4 — Entity extraction")

    if ner_cache_path and cache_exists(ner_cache_path):

        mentions = load_cache(ner_cache_path)
        logger.info(f"Loaded cached NER mentions from {ner_cache_path}")

    else:

        extractor = get_extractor(config)

        mentions = timed_stage(
            "Stage 4 — Entity extraction",
            extractor,
            sentences,
            config
        )

        if ner_cache_path:
            save_cache(mentions, ner_cache_path)

    logger.info("Stage 5 — Entity normalization")
    entities, entity_links = timed_stage(
        "Stage 5 — Entity normalization",
        normalize_entities,
        mentions,
        config
    )

    logger.info("Stage 6 — Relation extraction")

    relation_extractor = get_relation_extractor(config)

    relations = timed_stage(
        "Stage 6 — Relation extraction",
        relation_extractor,
        sentences,
        entities,
        config
    )

    logger.info("Stage 7 — Building graph objects")
    nodes, edges = timed_stage(
        "Stage 7 — Graph construction",
        build_graph,
        entities,
        relations,
        config
    )

    logger.info("Stage 8 — Graph embeddings")

    embeddings = timed_stage(
        "Stage 8 — Graph embeddings",
        compute_graph_embeddings,
        entities,
        relations
    )

    logger.info("Stage 9 — Writing graph to Neo4j")

    neo4j_cfg = pipeline_config["neo4j"]

    password = os.getenv("NEO4J_PASSWORD")

    if password is None:
        raise RuntimeError(
            "NEO4J_PASSWORD environment variable not set. Run: export NEO4J_PASSWORD='your_password'"
        )

    writer = Neo4jWriter(
        uri=neo4j_cfg["uri"],
        user=neo4j_cfg["user"],
        password=password
    )

    start = time.perf_counter()
    writer.write_graph(entities, relations)
    writer.close()

    logger.info(
        f"Stage 9 — Neo4j write completed in {time.perf_counter() - start:.3f} seconds"
    )

    logger.info("Stage 10 — Computing graph statistics")

    stats = timed_stage(
        "Stage 10 — Graph statistics",
        compute_graph_statistics,
        entities,
        relations
    )

    logger.info("Graph Statistics")
    logger.info(f"Nodes: {stats['nodes']}")
    logger.info(f"Edges: {stats['edges']}")
    logger.info(f"Density: {stats['density']:.4f}")
    logger.info(f"Average Degree: {stats['average_degree']:.2f}")

    logger.info("Stage 11 — Link prediction evaluation")

    link_metrics = timed_stage(
        "Stage 11 — Link prediction",
        evaluate_link_prediction,
        entities,
        relations
    )

    logger.info("Link Prediction Metrics")
    logger.info(f"MRR: {link_metrics['MRR']:.4f}")
    logger.info(f"Hits@1: {link_metrics['Hits@1']:.4f}")
    logger.info(f"Hits@3: {link_metrics['Hits@3']:.4f}")
    logger.info(f"Hits@10: {link_metrics['Hits@10']:.4f}")

    result = PipelineResult(
        documents=documents,
        sentences=sentences,
        mentions=mentions,
        entities=entities,
        relations=relations,
    )

    return result


if __name__ == "__main__":

    setup_logging("INFO")

    logger.info("Starting pipeline")

    with open("configs/pipeline.yaml", "r") as f:
        pipeline_config = yaml.safe_load(f)

    experiment_config_path = pipeline_config.get(
        "experiment_config",
        "configs/experiments/dev.yaml"
    )

    start_pipeline = time.perf_counter()

    result = run_pipeline(experiment_config_path, pipeline_config)

    logger.info(
        f"Pipeline completed in {time.perf_counter() - start_pipeline:.3f} seconds"
    )

    logger.info(f"Documents: {len(result.documents)}")
    logger.info(f"Sentences: {len(result.sentences)}")
    logger.info(f"Entities: {len(result.entities)}")
    logger.info(f"Relations: {len(result.relations)}")
