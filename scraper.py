import pandas as pd
from bs4 import BeautifulSoup
import time
import requests
import random

print("=" * 60)
print("SCRAPER IMMOBILIER MAROC")
print("=" * 60)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows 10 x64)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
    "Accept-Language": "*",
}

villes = ['casablanca', 'rabat', 'marrakech', 'tanger', 'fes']

Data = []

for ville in villes:
    print(f"\nScraping de {ville.upper()}...")
    
    url = f"https://www.avito.ma/fr/maroc/appartements_a_vendre?ville={ville}"
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            annonces = soup.find_all('div', class_='listing-item')
            
            if not annonces:
                annonces = soup.find_all("article")
            
            print(f"{len(annonces)} elements trouves")
            
            for i, annonce in enumerate(annonces[:10]):
                try:
                    prix = "Prix non trouve"
                    for selecteur in ["span.price", "div.price"]:
                        elem = annonce.select_one(selecteur)
                        if elem:
                            prix = elem.text.strip()
                            break
                    
                    titre = "Titre non trouve"
                    for selecteur in ["h2.title", "span.title"]:
                        elem = annonce.select_one(selecteur)
                        if elem:
                            titre = elem.text.strip()
                            break
                    
                    Data.append({
                        "ville": ville,
                        "titre": titre,
                        "prix": prix,
                        "date_scraping": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    print(f"   Annonce {i+1}: {prix[:50]}")
                    
                except Exception as e:
                    print(f"   Erreur sur une annonce: {e}")
        
        else:
            print(f"   Erreur HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   Erreur de connexion: {e}")
    
    time.sleep(random.uniform(2, 4))

print("\n" + "=" * 60)
print(f"RESULTATS: {len(Data)} annonces collectees")
print("=" * 60)

if Data:
    df = pd.DataFrame(Data)
    df.to_csv('data/raw/annonces_brutes.csv', index=False, encoding='utf-8-sig')
    print(f"Sauvegarde dans data/raw/annonces_brutes.csv")
    print("\nApercu:")
    print(df.head())
else:
    print("Aucune donnee collectee")