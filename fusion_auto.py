import os
import pandas as pd

# === 1. Définir le dossier des fichiers nettoyés ===
folder_clean = "data_clean"

# === 2. Lister les fichiers qui se terminent par "_clean.csv" ===
files_to_merge = [f for f in os.listdir(folder_clean) if f.endswith("_clean.csv")]

# === 3. Charger chaque fichier et ajouter une colonne source ===
dfs = []
for file in files_to_merge:
    path = os.path.join(folder_clean, file)
    df = pd.read_csv(path)
    df["Source"] = file.replace("_clean.csv", "")
    dfs.append(df)

# === 4. Fusionner les fichiers ===
df_fusion = pd.concat(dfs, ignore_index=True)

# === 5. Supprimer les doublons ===
df_fusion.drop_duplicates(inplace=True)

# === 6. Sauvegarder dans le dossier clean ===
fusion_path = os.path.join(folder_clean, "recettes_fusionnees.csv")
df_fusion.to_csv(fusion_path, index=False)

print("✅ Fichier fusionné sauvegardé dans :", fusion_path)
