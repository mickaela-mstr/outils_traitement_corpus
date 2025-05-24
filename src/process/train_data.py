import torch
import joblib
import evaluate
import numpy as np
import pandas as pd

from datasets import Dataset
from sklearn.preprocessing import LabelEncoder
from transformers import CamembertTokenizer, CamembertForSequenceClassification, Trainer, TrainingArguments

# Charger les données
df = pd.read_csv("../../data/clean/pokedex_balanced.csv")
df = df.dropna(subset=["description", "type"])

# Encoder les labels
label_encoder = LabelEncoder()
df["label"] = label_encoder.fit_transform(df["type"])
label_list = label_encoder.classes_.tolist()

# Tokenizer
tokenizer = CamembertTokenizer.from_pretrained("camembert-base")

def tokenize(example):
    return tokenizer(example["description"], padding="max_length", truncation=True, max_length=256)

# Dataset HuggingFace
dataset = Dataset.from_pandas(df[["description", "label"]])
dataset = dataset.train_test_split(test_size=0.2, seed=42)
tokenized_dataset = dataset.map(tokenize, batched=True)

# Charger le modèle
model = CamembertForSequenceClassification.from_pretrained("camembert-base", num_labels=len(label_list))

# Définir les métriques
accuracy = evaluate.load("accuracy")
f1 = evaluate.load("f1")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy.compute(predictions=preds, references=labels)["accuracy"],
        "f1": f1.compute(predictions=preds, references=labels, average="weighted")["f1"]
    }

# Arguments d'entraînement
training_args = TrainingArguments(
    output_dir="../../results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model="f1"
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# Lancer l'entraînement
trainer.train()

# Sauvegarder le modèle et le label encoder
model.save_pretrained("../../results/model")
tokenizer.save_pretrained("../../results/model")
joblib.dump(label_encoder, "../../results/label_encoder.pkl")
