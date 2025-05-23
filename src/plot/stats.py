import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import os
import seaborn as sns

# Chargement des données
df = pd.read_csv("pokedex.csv")

# Création du dossier résultats
os.makedirs("résultats", exist_ok=True)

# Stopwords personnalisés adaptés aux descriptions Pokémon
custom_stopwords = { 
    'le', 'la', 'les', 'de', 'des', 'du', 'un', 'une', 'et', 'en', 'dans', 'par', 'pour',
    'avec', 'sur', 'est', 'à', 'au', 'aux', 'se', 'ce', 'cet', 'cette', 'il', 'elle', 'ils',
    'elles', 'qui', 'que', 'dont', 'où', 'ne', 'pas', 'plus', 'moins', 'comme', 'son', 'sa',
    'ses', 'leurs', 'leur', 'a', 'ont', 'été', 'être', 'fait', 'faites', 'à'
    "très", "cette", "celui", "celle", "dont", "lorsqu", "ainsi", "alors", "fait",
    "comme", "leurs", "leurs.", "ses", "dans", "avec", "par", "est", "qui", "une", "des",
    "les", "plus", "sur", "du", "au", "pour", "d", "s", "ne", "pas", "être", "il", "elle", "ce"
}

# Nettoyage du texte
def clean_text(text):
    words = text.lower().split()
    words = [word.strip(".,;!?()[]'\"") for word in words]
    return [word for word in words if word.isalpha() and word not in custom_stopwords]

# Application du nettoyage
df["clean_words"] = df["description"].astype(str).apply(clean_text)

# Wordcloud global
all_words = [word for words in df["clean_words"] for word in words]
word_freq = Counter(all_words)
wc = WordCloud(width=800, height=400, background_color='white', max_words=100).generate_from_frequencies(word_freq)
plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.title("Nuage de mots - Tous les Pokémon")
plt.tight_layout()
plt.savefig("résultats/wordcloud_all.png")
plt.close()

# Wordcloud par type
types = df["type"].dropna().unique()
for t in types:
    type_words = [word for words in df[df["type"] == t]["clean_words"] for word in words]
    word_freq = Counter(type_words)
    if word_freq:
        wc = WordCloud(width=800, height=400, background_color='white', max_words=100).generate_from_frequencies(word_freq)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.title(f"Nuage de mots - Type {t}")
        plt.tight_layout()
        plt.savefig(f"résultats/wordcloud_{t}.png")
        plt.close()

# Barplot global
common_words = Counter(all_words).most_common(20)
words, counts = zip(*common_words)
plt.figure(figsize=(10, 5))
sns.barplot(x=list(words), y=list(counts))
plt.title("Top 20 des mots les plus fréquents - Tous les Pokémon")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("résultats/barplot_all.png")
plt.close()

# Barplot par type
for t in types:
    type_words = [word for words in df[df["type"] == t]["clean_words"] for word in words]
    word_freq = Counter(type_words).most_common(10)
    if word_freq:
        words, counts = zip(*word_freq)
        plt.figure(figsize=(8, 4))
        sns.barplot(x=list(words), y=list(counts))
        plt.title(f"Top 10 - Type {t}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"résultats/barplot_{t}.png")
        plt.close()
