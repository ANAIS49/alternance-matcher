"""Interface Streamlit : lance avec  `streamlit run app.py`"""
from pathlib import Path

import pandas as pd
import streamlit as st

from src.analyze import offers_by, skill_frequency, skill_gap
from src.clean import clean_offers, load_offers
from src.explain import explain
from src.match import rank_offers
from src.skills import extract_skills

DATA = Path(__file__).parent / "data"

st.set_page_config(page_title="Alternance Matcher", layout="wide")
st.title("🎯 Alternance Matcher")
st.caption("Analyse des offres + matching CV/offre par IA")

with st.sidebar:
    st.header("Paramètres")
    uploaded = st.file_uploader("Tes offres (CSV : title, company, city, description)", type="csv")
    method = st.radio("Méthode de similarité", ["tfidf", "embeddings"],
                      help="'embeddings' nécessite sentence-transformers")
    top_n = st.slider("Nombre d'offres affichées", 3, 20, 8)

cv_text = st.text_area("Ton CV (texte)", (DATA / "cv.txt").read_text(encoding="utf-8"), height=180)
df = clean_offers(pd.read_csv(uploaded)) if uploaded else load_offers(DATA / "offers_sample.csv")
if not uploaded:
    st.info("Données d'exemple (fictives). Importe tes vraies offres dans la barre latérale.")

tab1, tab2, tab3 = st.tabs(["🏆 Classement", "📊 Marché", "🧭 Feuille de route"])

with tab1:
    ranked = rank_offers(cv_text, df, method)
    for i, row in ranked.head(top_n).iterrows():
        with st.expander(f"#{i+1} — {row['title']} · {row['company']} ({row['city']}) — {row['score']}/100"):
            st.write(row["description"])
            st.markdown(explain(row, cv_text))

with tab2:
    freq = skill_frequency(df)
    c1, c2 = st.columns(2)
    c1.subheader("Compétences les plus demandées")
    c1.bar_chart(freq.set_index("skill")["pct_offers"])
    c2.subheader("Offres par ville")
    c2.bar_chart(offers_by(df, "city"))

with tab3:
    gap = skill_gap(df, extract_skills(cv_text))
    st.subheader("Ce que le marché demande vs ce que tu as")
    st.dataframe(gap, width="stretch")
    st.markdown("**À apprendre en priorité :** " +
                ", ".join(gap[~gap["tu_l_as"]].head(5)["skill"]))
