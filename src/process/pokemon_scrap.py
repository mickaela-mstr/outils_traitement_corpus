from bs4 import BeautifulSoup
import requests
import pandas as pd
from collections import defaultdict

""" Utilise ce script pour créer un csv qui contient le nom du pokemon, sa desription et son type"""

def get_home_page():
 
    url = "https://www.pokepedia.fr/Liste_des_Pok%C3%A9mon_de_la_premi%C3%A8re_g%C3%A9n%C3%A9ration"
    response = requests.get(url)
    base_url = response.url
    return response.text, base_url

def extract_pokemon_data(row, base_url):
    
    pokedex = {}

    info = row.find_all("a", {"title": True})
    if len(info) > 0:
        page = info[0]["href"]
        page = base_url + page
        description = retrieve_description(page)
        name = info[1]
        type = info[6]
        pokedex["name"] = name["title"]
        pokedex["type"] = type["title"]
        pokedex["description"] = description
        
        return pokedex
    
def retrieve_description(page):

    response = requests.get(page)
    soup = BeautifulSoup(response.text, "html.parser")
    description = soup.find("div", {"id": "mw-content-text"})
    paragraphs = description.find_all("p")
    if len(paragraphs) > 0:
        paragraphs = paragraphs[1:]
    
    description = ""
    for paragraph in paragraphs:
        description += paragraph.get_text()
    return description
    

if __name__ == "__main__":


    home_page, base_url = get_home_page()
    base_url = base_url.split("/Liste")[0]
    soup = BeautifulSoup(home_page, "html.parser")
    main_table = soup.find("table", {"class": ["tableaustandard", "sortable", "entetefixe"]})
    rows = main_table.find_all("tr")

    pokedex = defaultdict(list)

    for i, row in enumerate(rows[1:]):
        print(f"Traitement du pokemon {i}")
        try:
            pokedex_solo = extract_pokemon_data(row, base_url)
            if pokedex_solo:
                pokedex["name"].append(pokedex_solo["name"])
                pokedex["type"].append(pokedex_solo["type"])
                pokedex["description"].append(pokedex_solo["description"])
        except Exception as e:
            print(f"Erreur avec le pokemon {i}: {e}")

            
    df = pd.DataFrame(pokedex)
    df.to_csv("pokedex.csv", index=False)