import requests
from bs4 import BeautifulSoup

poke_url = "https://www.pokepedia.fr/Liste_des_Pok%C3%A9mon_de_la_premi%C3%A8re_g%C3%A9n%C3%A9ration"

# Récupération de la page
response = requests.get(poke_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Chercher tous les liens vers les pages des Pokémon
poke_links = []
table = soup.find('table', {'class': 'tableaustandard'})

for row in table.find_all('tr')[1:]:  # On saute l'en-tête
    cells = row.find_all('td')
    if len(cells) >= 3:  # On vérifie qu'il y a bien au moins 3 colonnes
        cell = cells[2]  # 3ème colonne (Nom)
        link = cell.find('a')
        if link:
            poke_links.append("https://www.pokepedia.fr" + link['href'])

with open('poke_urls/poke_urls.txt', 'w', encoding='utf-8') as f:
    for url in poke_links:
        f.write(url + '\n')