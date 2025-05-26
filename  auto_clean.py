# auto_clean.py

import os
import pandas as pd
from datetime import datetime

# === 1. Détection des fichiers bruts ===
folder_raw = "data_raw"
folder_clean = "data_clean"
os.makedirs(folder_clean, exist_ok=True)

# Liste les fichiers Excel ou CSV
data_files = [f for f in os.listdir(folder_raw) if f.endswith(('.xlsx', '.xls', '.csv'))]

# === 2. Fonction de nettoyage automatique ===
def clean_dataframe(df):
    # Harmonisation des noms de colonnes
    df.columns = df.columns.str.strip().str.replace('\n', '').str.replace('"', '').str.replace('\\xa0', '')
    df.columns = df.columns.str.replace('é', 'e', regex=False).str.replace('É', 'E', regex=False)
    df.columns = df.columns.str.replace('PRÉVISION', 'Prevision', regex=False)

    rename_dict = {
        "ANNÉE": "Annee", "Année": "Annee",
        "MOIS": "Mois",
        "RÉGIE": "Regie", "Régie": "Regie",
        "RUBRIQUE": "Rubrique",
        "PREVISION": "Prevision", "Prévision": "Prevision",
        "REALISATION": "Realisation", "Réalisation": "Realisation",
        "ECART": "Ecart", "ÉCART": "Ecart",
        "TAUX": "Taux"
    }
    df = df.rename(columns=rename_dict)

    # Conversion des valeurs numériques
    numeric_cols = ["Prevision", "Realisation", "Ecart", "Taux"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Création colonne Date si Mois + Annee
    mois_map = {
        "JANV": "01", "FÉVR": "02", "MARS": "03", "AVRIL": "04", "MAI": "05", "JUIN": "06",
        "JUIL": "07", "AOÛT": "08", "SEPT": "09", "OCT": "10", "NOV": "11", "DÉC": "12",
        "DEC": "12", "AOUT": "08"
    }
    if "Mois" in df.columns and "Annee" in df.columns:
        df["Mois"] = df["Mois"].astype(str).str.upper().str[:4]
        df["Mois_num"] = df["Mois"].map(mois_map)
        df["Date"] = pd.to_datetime(df["Annee"].astype(str) + "-" + df["Mois_num"], errors="coerce")

    return df

# === 3. Nettoyage de chaque fichier ===
for file in data_files:
    file_path = os.path.join(folder_raw, file)
    print(f"Traitement de : {file}")

    # Chargement en fonction du format
    if file.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # Nettoyage
    df_clean = clean_dataframe(df)

    # Sauvegarde
    name_clean = file.split('.')[0] + "_clean.csv"
    clean_path = os.path.join(folder_clean, name_clean)
    df_clean.to_csv(clean_path, index=False)
    print(f"Nettoyé et sauvegardé : {clean_path}")

print("\n✅ Tous les fichiers ont été nettoyés et enregistrés dans data_clean/")
