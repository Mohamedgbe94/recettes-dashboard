# main.py
# === Automatiser la mise à jour quotidienne du pipeline ===

import subprocess
import datetime
import os

# === 1. Début du processus ===
print("\n=== Début de l'automatisation ===")
print("Date et heure :", datetime.datetime.now())

# === 2. Chemin absolu du dossier ===
base_path = "/Users/sylla/Documents/PROJETREC/env"  # Le bon répertoire où se trouvent tes scripts Python

# === 3. Lancement du script auto_clean.py ===
try:
    print("\n🧼 Exécution de : auto_clean.py...")
    subprocess.run(["python3", os.path.join(base_path, "auto_clean.py")], check=True)
except Exception as e:
    print("Erreur dans auto_clean.py :", e)

# === 4. Lancement du script fusion_auto.py ===
try:
    print("\n🧹 Exécution de : fusion_auto.py...")
    subprocess.run(["python3", os.path.join(base_path, "fusion_auto.py")], check=True)
except Exception as e:
    print("Erreur dans fusion_auto.py :", e)

# === 5. Lancement du script analyse_auto.py ===
try:
    print("\n📊 Exécution de : analyse_auto.py...")
    subprocess.run(["python3", os.path.join(base_path, "analyse_auto.py")], check=True)
except Exception as e:
    print("Erreur dans analyse_auto.py :", e)

# === 6. (Facultatif) Lancer le dashboard Streamlit automatiquement ===
# try:
#     print("\n🚀 Lancement du Dashboard Streamlit...")
#     subprocess.run(["streamlit", "run", os.path.join(base_path, "dashboard_streamlit.py")], check=True)
# except Exception as e:
#     print("Erreur dans dashboard_streamlit.py :", e)

print("\n🗓️ Pipeline exécuté avec succès le", datetime.datetime.now())
