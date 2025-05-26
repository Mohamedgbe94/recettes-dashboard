import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === 1. Charger les données fusionnées ===
df = pd.read_csv("data_clean/recettes_fusionnees.csv")

# === 2. Nettoyer les colonnes ===
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace("\n", "").str.replace("\u00e9", "e").str.replace("\u00c9", "E")

# Harmoniser les noms de colonnes
rename_map = {
    "ANNEE": "Annee", "Année": "Annee",
    "MOIS": "Mois", "REGIE": "Regie", "Régie": "Regie",
    "PREVISION": "Prevision", "Prévision": "Prevision",
    "REALISATION": "Realisation", "Réalisation": "Realisation",
    "ECART": "Ecart", "Taux": "Taux"
}
df = df.rename(columns=rename_map)

# === 3. Créer un dossier de sortie ===
output_dir = "data_clean/graphes"
os.makedirs(output_dir, exist_ok=True)

# === 4. Evolution mensuelle des recettes ===
df_mensuel = df.groupby("Date")[["Realisation", "Prevision"]].sum()
plt.figure(figsize=(10, 5))
plt.plot(df_mensuel.index, df_mensuel["Realisation"], label="Réalisé", marker='o')
plt.plot(df_mensuel.index, df_mensuel["Prevision"], label="Prévu", marker='x', linestyle='--')
plt.title("Evolution mensuelle des recettes")
plt.xlabel("Date")
plt.ylabel("Montants (GNF)")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "evolution_mensuelle_auto.png"), dpi=300)
plt.close()

# === 5. Taux moyen de réalisation par régie ===
df_taux_moyen = df.groupby("Regie")["Taux"].mean()
plt.figure(figsize=(8, 6))
sns.barplot(x=df_taux_moyen.index, y=df_taux_moyen.values, color="purple")
plt.title("Taux de réalisation moyen par régie")
plt.xlabel("Régie")
plt.ylabel("Taux (%)")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "taux_moyen_regie_auto.png"), dpi=300)
plt.close()

# === 6. Ecart moyen par régie ===
df_ecarts = df.groupby("Regie")["Ecart"].mean().sort_values()
plt.figure(figsize=(8, 6))
sns.barplot(x=df_ecarts.index, y=df_ecarts.values, palette="Reds")
plt.title("Ecart moyen entre prévision et réalisation par régie")
plt.xlabel("Régie")
plt.ylabel("Ecart moyen (GNF)")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "ecart_moyen_regie_auto.png"), dpi=300)
plt.close()

print("\U00002705 Tous les graphiques d'analyse automatique ont été générés dans :", output_dir)
