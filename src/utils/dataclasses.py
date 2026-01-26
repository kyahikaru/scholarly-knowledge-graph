from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional


@dataclass
class Document:
    doc_id: str
    source_path: str
    title: Optional[str]
    sections: Dict[str, str]


@dataclass
class Sentence:
    sentence_id: str
    doc_id: str
    section: str
    text: str


@dataclass
class TokenizedSentence:
    sentence_id: str
    tokens: List[str]
    char_offsets: List[Tuple[int, int]]


@dataclass
class EntityMention:
    mention_id: str
    sentence_id: str
    doc_id: str
    text: str
    entity_type: str
    start_char: int
    end_char: int


@dataclass
class CanonicalEntity:
    entity_id: str
    canonical_name: str
    entity_type: str
    aliases: List[str]


@dataclass
class EntityLink:
    mention_id: str
    entity_id: str


@dataclass
class RelationInstance:
    relation_id: str
    source_entity_id: str
    target_entity_id: str
    relation_type: str
    sentence_id: str


@dataclass
class GraphNode:
    node_id: str
    label: str
    properties: Dict


@dataclass
class GraphEdge:
    source_id: str
    target_id: str
    relation_type: str
    properties: Dict


@dataclass
class PipelineResult:
    documents: List[Document]
    sentences: List[Sentence]
    mentions: List[EntityMention]
    entities: List[CanonicalEntity]
    relations: List[RelationInstance]
