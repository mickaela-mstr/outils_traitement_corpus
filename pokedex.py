import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL de la liste des 151 Pokémon
poke_url_list = "https://www.pokepedia.fr/Liste_des_Pok%C3%A9mon_de_la_premi%C3%A8re_g%C3%A9n%C3%A9ration"

# Récupérer la page
poke_response = requests.get(poke_url_list)
poke_soup = BeautifulSoup(poke_response.content, 'html.parser')

# Chercher la table
poke_table = poke_soup.find('table', {'class': 'tableaustandard'})

# Liste pour URLs, noms, types
poke_entries = []

# Parsing de chaque ligne de la table
for poke_row in poke_table.find_all('tr')[1:]:
    poke_cells = poke_row.find_all('td')
    if len(poke_cells) >= 4:
        # Colonne 3 : nom
        poke_name_cell = poke_cells[2]
        poke_link_tag = poke_name_cell.find('a')
        if poke_link_tag:
            poke_name = poke_link_tag.text.strip()
            poke_url = "https://www.pokepedia.fr" + poke_link_tag['href']

            # Colonne 4 : types
            poke_type_cell = poke_cells[7]
            poke_type_links = poke_type_cell.find_all('a')
            poke_types = [poke_link.text.strip() for poke_link in poke_type_links if poke_link.text.strip()]
            poke_type_text = ', '.join(poke_types)

            poke_entries.append({
                'Nom': poke_name,
                'URL': poke_url,
                'Type': poke_type_text
            })

print(f"✅ Trouvé {len(poke_entries)} Pokémon avec leurs types et URLs.")

# Maintenant : scraper le contenu de chaque fiche
poke_data = []

for poke_entry in poke_entries:
    poke_url = poke_entry['URL']
    poke_name = poke_entry['Nom']
    poke_types_list = poke_entry['Type'].split(', ')

    try:
        poke_response = requests.get(poke_url)
        poke_soup = BeautifulSoup(poke_response.content, 'html.parser')

        # Récupérer le contenu principal
        poke_content_div = poke_soup.find('div', {'id': 'mw-content-text'})
        poke_content_text = poke_content_div.get_text(separator=' ', strip=True)

        # Sauvegarder le texte brut dans les dossiers par type
        for poke_type in poke_types_list:
            poke_type_dir = f"pokedex/{poke_type}"
            os.makedirs(poke_type_dir, exist_ok=True)
            poke_filename = poke_name.replace(' ', '_')
            with open(f"{poke_type_dir}/{poke_filename}.txt", 'w', encoding='utf-8') as poke_f_out:
                poke_f_out.write(poke_content_text)

        # Ajout au CSV global
        poke_data.append({
            'Nom': poke_name,
            'Type': poke_entry['Type'],
            'Description': poke_content_text
        })

        print(f"✅ {poke_name} - Type(s): {poke_entry['Type']}")
        time.sleep(1)

    except Exception as poke_e:
        print(f"❌ Erreur avec {poke_url}: {poke_e}")

# Sauvegarde CSV final
poke_df = pd.DataFrame(poke_data)
os.makedirs('data', exist_ok=True)
poke_df.to_csv('pokedex.csv', index=False, encoding='utf-8')
print(f"🎉 Toutes les fiches avec types corrigés sauvegardées dans data/pokemon_fiches/ et CSV prêt")
