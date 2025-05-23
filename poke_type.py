# j'arrivais pas à récupérer les types depuis poképédia donc j'ai trouvé un site qui listait les pokémons et leur types en texte simple. 
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.relictcg.com/blogs/guides/quels-sont-les-151-premiers-pokemon"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

poke_lines = []

# On prend tous les éléments de texte dans le corps principal
for tag in soup.find_all(['p', 'li']):
    text = tag.get_text().strip()
    if re.match(r'^\d{3} ', text):  # commence par "001 ", "034 ", etc.
        poke_lines.append(text)

poke_data = []

for line in poke_lines:
    try:
        # Ex: "001 Bulbizarre : type Plante Poison"
        match = re.match(r'^\d+\s+([^\:]+)\s*:\s*type\s+(.+)', line, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            types = match.group(2).strip()
            poke_data.append({'Nom': name, 'Type': types})
    except Exception as e:
        print(f"❌ Problème avec : {line} → {e}")

df = pd.DataFrame(poke_data)
df.to_csv("pokedex/pokemon_types.csv", index=False, encoding="utf-8")
print("✅ Fichier data/pokemon_types.csv créé avec succès !")
