import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
from datetime import datetime

# === 1. Chargement et nettoyage des données ===
@st.cache_data
def load_data():
    path = "recettes_fusionnees.csv"
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower().str.capitalize()
    col_map = {
        "Réalisation": "Realisation",
        "Prévision": "Prevision",
        "Régie": "Regie",
        "Catégorie": "Categorie",
        "Rubriques": "Rubrique",
        "Ecart": "Ecart",
        "Taux": "Taux",
    }
    df = df.rename(columns=col_map)
    if "Taux" not in df.columns and "Realisation" in df.columns and "Prevision" in df.columns:
        df["Taux"] = df["Realisation"] / df["Prevision"].replace(0, pd.NA)
    if "Ecart" not in df.columns and "Realisation" in df.columns and "Prevision" in df.columns:
        df["Ecart"] = df["Realisation"] - df["Prevision"]
    return df

# === 2. Configuration ===
st.set_page_config(layout="wide")
st.title("📊 Dashboard Enrichi des Recettes Publiques")
df = load_data()

# === 3. Filtres ===
st.sidebar.header("🔍 Filtres dynamiques")
annees = sorted(df["Annee"].dropna().unique())
categories = df["Categorie"].dropna().unique()
rubriques = df["Rubrique"].dropna().unique()

selected_year = st.sidebar.selectbox("Année", annees, index=len(annees)-1)
selected_categorie = st.sidebar.selectbox("Catégorie", ["Toutes"] + list(categories))
selected_rubrique = st.sidebar.selectbox("Rubrique", ["Toutes"] + list(rubriques))

filtered_df = df[df["Annee"] == selected_year]
if selected_categorie != "Toutes":
    filtered_df = filtered_df[filtered_df["Categorie"] == selected_categorie]
if selected_rubrique != "Toutes":
    filtered_df = filtered_df[filtered_df["Rubrique"] == selected_rubrique]

# === 4. Indicateurs Clés ===
st.markdown("## 📌 Indicateurs Clés")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Total Réalisé", f"{filtered_df['Realisation'].sum():,.0f} GNF")
with c2:
    st.metric("Total Prévu", f"{filtered_df['Prevision'].sum():,.0f} GNF")
with c3:
    taux = filtered_df['Taux'].mean()
    st.metric("Taux de Réalisation Moyen", f"{taux:.2%}")

st.markdown("---")

# === 5. Comparaison interannuelle ===
st.subheader("📅 Comparaison interannuelle")
if "Date" in df.columns:
    fig_line = px.line(
        df.groupby(["Date", "Annee"])["Realisation"].sum().reset_index(),
        x="Date", y="Realisation", color="Annee",
        title="Évolution des réalisations par année",
        markers=True
    )
    st.plotly_chart(fig_line, use_container_width=True)

# === 6. Croissance cumulée ===
st.subheader("📈 Croissance cumulée des recettes")
cumul_df = filtered_df.sort_values("Date").copy()
cumul_df["Cumul_Real"] = cumul_df["Realisation"].cumsum()
cumul_df["Cumul_Prev"] = cumul_df["Prevision"].cumsum()
fig_cumul = px.area(
    cumul_df, x="Date", y=["Cumul_Real", "Cumul_Prev"],
    title="Cumul des réalisations et prévisions dans l'année"
)
st.plotly_chart(fig_cumul, use_container_width=True)

# === 7. Analyse interactive par régie ===
st.subheader("🏛️ Analyse des régies")
if "Regie" in filtered_df.columns:
    fig_regie = px.bar(
        filtered_df.groupby("Regie")["Realisation"].sum().reset_index().sort_values("Realisation"),
        x="Realisation", y="Regie", orientation="h",
        title="Recettes réalisées par régie", color="Realisation"
    )
    st.plotly_chart(fig_regie, use_container_width=True)

# === 8. Carte géographique (optionnelle) ===
if os.path.exists("data_clean/geo_data.csv"):
    st.subheader("🗺️ Carte des recettes par région")
    geo_df = pd.read_csv("data_clean/geo_data.csv")
    fig_map = px.choropleth(
        geo_df,
        geojson="https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson",
        locations="region", featureidkey="properties.name",
        color="realisation",
        projection="mercator",
        title="Répartition géographique des recettes"
    )
    fig_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_map, use_container_width=True)

# === 9. Date de mise à jour ===
st.caption(f"🔁 Données actualisées automatiquement — {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

