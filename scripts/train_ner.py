import torch
import torch.nn as nn
import torch.optim as optim

from src.entity_extraction.bilstm_crf_model import BiLSTMCRF


# Example toy vocabulary and tagset
# This is just to verify the model trains correctly

word_to_ix = {
    "named": 0,
    "entity": 1,
    "recognition": 2,
    "uses": 3,
    "conll": 4,
    "dataset": 5
}

tag_to_ix = {
    "O": 0,
    "B-TASK": 1,
    "I-TASK": 2,
    "B-DATASET": 3,
    "I-DATASET": 4
}


training_data = [
    (
        ["named", "entity", "recognition", "uses", "conll", "dataset"],
        ["B-TASK", "I-TASK", "I-TASK", "O", "B-DATASET", "I-DATASET"]
    )
]


def prepare_sequence(seq, to_ix):
    return torch.tensor([to_ix[w] for w in seq], dtype=torch.long)


EMBEDDING_DIM = 50
HIDDEN_DIM = 64

model = BiLSTMCRF(
    vocab_size=len(word_to_ix),
    embedding_dim=EMBEDDING_DIM,
    hidden_dim=HIDDEN_DIM,
    tagset_size=len(tag_to_ix)
)

loss_function = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)


for epoch in range(5):

    total_loss = 0

    for sentence, tags in training_data:

        model.zero_grad()

        sentence_in = prepare_sequence(sentence, word_to_ix)

        targets = prepare_sequence(tags, tag_to_ix)

        outputs = model(sentence_in.unsqueeze(0))

        outputs = outputs.view(-1, len(tag_to_ix))

        loss = loss_function(outputs, targets)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1} Loss: {total_loss}")


torch.save(model.state_dict(), "ner_model.pt")

print("Model training complete. Model saved as ner_model.pt")
