import pandas as pd
from sklearn.utils import resample

# Charger les données augmentées
df = pd.read_csv("../../data/clean/pokedex_aug_backtranslate.csv")
df = df.dropna(subset=["description", "type"])

# Compter les exemples par classe
class_counts = df["type"].value_counts()
max_count = class_counts.max()

# Rééchantillonnage par duplication
df_balanced = pd.concat([
    resample(df[df["type"] == t], 
             replace=True, 
             n_samples=max_count, 
             random_state=42)
    for t in class_counts.index
])

# Mélanger les données
df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

# Sauvegarder
df_balanced.to_csv("../../data/clean/pokedex_balanced.csv", index=False)
