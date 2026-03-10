import torch

from typing import List
from src.utils.dataclasses import Sentence, EntityMention
from src.entity_extraction.bilstm_crf_model import BiLSTMCRF


def load_model():

    # These must match training parameters
    vocab_size = 6
    embedding_dim = 50
    hidden_dim = 64
    tagset_size = 5

    model = BiLSTMCRF(vocab_size, embedding_dim, hidden_dim, tagset_size)

    model.load_state_dict(torch.load("ner_model.pt"))

    model.eval()

    return model


model = load_model()


def extract_entities(sentences: List[Sentence], config: dict):

    mentions = []

    # For now we only verify model inference works
    # Full tokenization and tagging will be added next

    for sent in sentences:

        # Placeholder: ML inference integration will be expanded
        pass

    return mentions
