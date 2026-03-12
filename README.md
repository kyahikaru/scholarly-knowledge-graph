# Scholarly Knowledge Graph Construction

This project implements an end-to-end pipeline for constructing a knowledge graph from NLP research papers. The system processes scholarly PDF documents, extracts important entities such as tasks and datasets, identifies relationships between them, and stores the results in a Neo4j graph database. The resulting graph can be queried, visualized, and analyzed using standard graph statistics and link prediction metrics. The objective of this project is to demonstrate a complete research engineering workflow that integrates natural language processing, graph construction, and evaluation into a reproducible system.

## Example Knowledge Graph

![Knowledge Graph](docs./knowledge_graph_example.png)

Figure 1: Example knowledge graph generated from the processed research paper corpus. The graph captures relationships between entities extracted from scholarly papers. In this prototype, task and dataset entities are connected using heuristic relations derived from sentence co-occurrence.

## System Architecture

![Pipeline Architecture](docs./pipeline_architecture.png)

Figure 2: End-to-end pipeline for scholarly knowledge graph construction. The pipeline consists of the following stages. Document ingestion loads research papers from PDF format. Preprocessing cleans the raw documents and converts them into structured text. Sentence segmentation splits the text into individual sentences for downstream processing. Entity extraction uses a BiLSTM-CRF model to identify entities such as tasks and datasets. Entity normalization consolidates extracted mentions into canonical entities. Relation extraction applies heuristic rules to detect relationships between entities based on sentence co-occurrence. Graph construction transforms entities and relations into graph nodes and edges. Graph storage saves the resulting graph in a Neo4j database. Finally, evaluation computes graph statistics and link prediction metrics to analyze the structure of the generated knowledge graph.

## Evaluation Results

![Evaluation Metrics](docs./evaluation_results.png)

Figure 3: Summary of graph statistics and link prediction evaluation metrics produced by the system.

Graph Statistics  
Documents processed: 8  
Sentences extracted: 5356  
Entities discovered: 4  
Relation instances: 62  
Unique graph edges: 4  
Graph density: 0.333  
Average degree: 2.0  

Link Prediction Metrics  
Mean Reciprocal Rank (MRR): 1.0  
Hits@1: 1.0  
Hits@3: 1.0  
Hits@10: 1.0  

These metrics provide a simple evaluation of the structural properties of the generated knowledge graph.

## Project Structure

scholarly-knowledge-graph  
configs  
data  
└── raw_pdfs  
docs  
└── images  
    ├── pipeline_architecture.png  
    ├── knowledge_graph_example.png  
    └── evaluation_results.png  
evaluation  
├── graph_statistics.py  
└── link_prediction.py  
scripts  
└── run_pipeline.py  
src  
├── entity_extraction  
├── relation_extraction  
├── normalization  
├── graph_construction  
└── utils  
README.md  

## How to Run the Pipeline

Clone the repository  
git clone https://github.com/<username>/scholarly-knowledge-graph.git  
cd scholarly-knowledge-graph  

Install dependencies  
pip install -r requirements.txt  

Place research paper PDFs in the directory  
data/raw_pdfs/

Run the pipeline  
PYTHONPATH=. python scripts/run_pipeline.py  

The pipeline will process the documents, extract entities and relations, construct the knowledge graph, store it in Neo4j, and compute evaluation metrics.

## Technologies Used

Python  
PyTorch  
Neo4j  
BiLSTM-CRF for entity recognition  
Heuristic relation extraction  
Graph analytics and evaluation

## Limitations

This project uses heuristic relation extraction based on entity co-occurrence within sentences. While effective for small experimental datasets, this approach does not capture deeper semantic relationships that require contextual reasoning. Future improvements could incorporate transformer-based relation extraction models and larger scholarly corpora.

## Future Work

Possible extensions include expanding the entity types beyond tasks and datasets, incorporating transformer-based NER models, scaling the pipeline to larger research corpora, and applying graph embedding methods for improved link prediction.

## License

This project is provided for research and educational purposes.
