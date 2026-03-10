import torch
from typing import List

from src.utils.dataclasses import Sentence, EntityMention
from src.entity_extraction.bilstm_crf_model import BiLSTMCRF


# toy vocabulary used during training
word_to_ix = {
    "named": 0,
    "entity": 1,
    "recognition": 2,
    "uses": 3,
    "conll": 4,
    "dataset": 5
}

ix_to_tag = {
    0: "O",
    1: "B-TASK",
    2: "I-TASK",
    3: "B-DATASET",
    4: "I-DATASET"
}


def load_model():

    vocab_size = 6
    embedding_dim = 50
    hidden_dim = 64
    tagset_size = 5

    model = BiLSTMCRF(
        vocab_size=vocab_size,
        embedding_dim=embedding_dim,
        hidden_dim=hidden_dim,
        tagset_size=tagset_size
    )

    model.load_state_dict(torch.load("ner_model.pt"))
    model.eval()

    return model


model = load_model()


def tokenize(text: str):
    return text.lower().split()


def extract_entities(sentences: List[Sentence], config: dict):

    mentions = []
    mention_counter = 0

    for sent in sentences:

        tokens = tokenize(sent.text)

        token_ids = []
        valid_tokens = []

        for token in tokens:
            if token in word_to_ix:
                token_ids.append(word_to_ix[token])
                valid_tokens.append(token)

        if len(token_ids) == 0:
            continue

        tensor = torch.tensor(token_ids).unsqueeze(0)

        outputs = model(tensor)

        predictions = torch.argmax(outputs, dim=2).squeeze().tolist()

        if not isinstance(predictions, list):
            predictions = [predictions]

        for token, tag_id in zip(valid_tokens, predictions):

            tag = ix_to_tag.get(tag_id, "O")

            if tag.startswith("B-"):

                entity_type = tag.split("-")[1]

                mention = EntityMention(
                    mention_id=mention_counter,
                    text=token,
                    entity_type=entity_type,
                    sentence_id=0,
                    doc_id=0,
                    start_char=0,
                    end_char=0
                )

                mentions.append(mention)
                mention_counter += 1

    return mentions
