import kagglehub
import shutil
import os

print("Téléchargement du dataset...")

path = kagglehub.dataset_download("yassinesadiki/housing-data-in-morocco")
print("Dataset téléchargé ici :", path)

# Copier les fichiers CSV dans ton dossier data/raw/
for fichier in os.listdir(path):
    if fichier.endswith('.csv'):
        shutil.copy(
            os.path.join(path, fichier),
            os.path.join('data/raw/', fichier)
        )
        print(f"Copié : {fichier} → data/raw/{fichier}")

print("Terminé !")