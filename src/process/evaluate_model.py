import torch
import joblib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from datasets import Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from transformers import CamembertTokenizer, CamembertForSequenceClassification

# Chemins
MODEL_DIR = "../../results/model"
LABEL_ENCODER_PATH = "../../results/label_encoder.pkl"
DATA_PATH = "../../data/clean/pokedex_aug_backtranslate.csv"

# Charger les éléments
model = CamembertForSequenceClassification.from_pretrained(MODEL_DIR)
tokenizer = CamembertTokenizer.from_pretrained(MODEL_DIR)
label_encoder = joblib.load(LABEL_ENCODER_PATH)

# Préparer les données
df = pd.read_csv(DATA_PATH)
df = df.dropna(subset=["description", "type"])
df["label"] = label_encoder.transform(df["type"])
df["type"].value_counts(normalize=True)

# Séparer un jeu de test (même seed que TP5 pour cohérence)
_, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Tokenisation
def tokenize(examples):
    return tokenizer(examples["description"], padding="max_length", truncation=True, max_length=256)

dataset = Dataset.from_pandas(test_df[["description", "label"]])
dataset = dataset.map(tokenize)
dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

# Prédictions
model.eval()
predictions = []
true_labels = []

with torch.no_grad():
    for batch in torch.utils.data.DataLoader(dataset, batch_size=8):
        inputs = {k: v for k, v in batch.items() if k in ["input_ids", "attention_mask"]}
        outputs = model(**inputs)
        preds = torch.argmax(outputs.logits, dim=-1).cpu().numpy()
        labels = batch["label"].cpu().numpy()
        predictions.extend(preds)
        true_labels.extend(labels)

# Rapport de classification
labels = list(range(len(label_encoder.classes_)))
report = classification_report(true_labels, predictions, labels=labels, target_names=label_encoder.classes_, digits=3, zero_division=0)
print(report)

# Matrice de confusion
cm = confusion_matrix(true_labels, predictions)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt="d", xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_, cmap="Blues")
plt.xlabel("Prédit")
plt.ylabel("Réel")
plt.title("Matrice de confusion")
plt.tight_layout()
plt.savefig("../../figures/confusion_matrix.png")
plt.close()
