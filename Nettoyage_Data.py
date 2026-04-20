import pandas as pd

df = pd.read_csv("data/raw/housing_data.csv", encoding="utf-8-sig")

print("Nombre de lignes :", len(df))
print("\nColonnes disponibles :")
print(df.columns.tolist())
print("\nAperçu des 5 premières lignes :")
print(df.head())
print("\nInfos générales :")
print(df.info())


print("\nValeurs manquantes par colonne :")
print(df.isnull().sum())


colonnes_texte = ["desc", "address", "ascenseur", 
                  "terrasse", "parking", "Type", 
                  "City", "Nighberd"]
df[colonnes_texte] = df[colonnes_texte].fillna("Non précisé")


colonnes_nombres = ["new_price", "chambres", 
                    "salles de bains", "surface", 
                    "floor"]
for col in colonnes_nombres:
    moyenne = df[col].mean().round(0)
    df[col] = df[col].fillna(moyenne)
    print(f"Colonne '{col}' : valeurs nulles remplacées par {moyenne}")


print("\nValeurs manquantes après correction :")
print(df.isnull().sum())



df.to_csv("data/clean/housing_clean.csv", index=False, encoding="utf-8-sig")
print("\nFichier sauvegardé dans data/clean/housing_clean.csv ✓")