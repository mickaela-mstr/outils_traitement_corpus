import pandas as pd
from deep_translator import GoogleTranslator
from tqdm import tqdm

# Charger le dataset d'origine
df = pd.read_csv("../../data/raw/pokedex.csv")
df = df.dropna(subset=["description", "type"])

def truncate_text(text, max_len=4900):
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]
    last_period = truncated.rfind(".")
    if last_period != -1:
        return truncated[:last_period + 1]
    return truncated

def back_translate(text):
    text = truncate_text(text)
    try:
        en = GoogleTranslator(source='fr', target='en').translate(text)
        fr = GoogleTranslator(source='en', target='fr').translate(en)
        return fr
    except Exception as e:
        print("Erreur lors de la traduction :", e)
        return None
    
augmented = []
for _, row in tqdm(df.iterrows(), total=len(df)):
    original = row["description"]
    label = row["type"]
    bt = back_translate(original)
    if bt:
        augmented.append({"description": bt, "type": label})

aug_df = pd.DataFrame(augmented)

full_df = pd.concat([df[["description", "type"]], aug_df], ignore_index=True)

full_df.to_csv("../../data/raw/pokedex_aug_backtranslate.csv", index=False)
