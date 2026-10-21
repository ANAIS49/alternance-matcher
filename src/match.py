"""Matching CV <-> offres (étape 3 : IA).

Deux méthodes de similarité sémantique :
- "tfidf"      : léger, marche hors-ligne, parfait pour comprendre le principe.
- "embeddings" : sentence-transformers multilingue, bien meilleur sur le français.

Score final = 60 % similarité du texte + 40 % couverture des compétences demandées.
"""
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .skills import extract_skills

EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"


def _similarity_tfidf(cv: str, texts: list[str]) -> np.ndarray:
    vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
    m = vec.fit_transform([cv] + texts)
    return cosine_similarity(m[0], m[1:]).ravel()


def _similarity_embeddings(cv: str, texts: list[str]) -> np.ndarray:
    from sentence_transformers import SentenceTransformer  # import tardif : optionnel

    model = SentenceTransformer(EMBEDDING_MODEL)
    emb = model.encode([cv] + texts, normalize_embeddings=True)
    return (emb[1:] @ emb[0]).ravel()


def rank_offers(cv_text: str, df: pd.DataFrame, method: str = "tfidf") -> pd.DataFrame:
    my_skills = extract_skills(cv_text)
    texts = df["text"].tolist()

    sim = _similarity_embeddings(cv_text, texts) if method == "embeddings" \
        else _similarity_tfidf(cv_text, texts)
    # Normalise la similarité entre 0 et 1 pour pouvoir la combiner
    sim = (sim - sim.min()) / (sim.max() - sim.min() + 1e-9)

    out = df.copy()
    out["similarity"] = sim
    out["matched"] = out["skills"].apply(lambda s: sorted(s & my_skills))
    out["missing"] = out["skills"].apply(lambda s: sorted(s - my_skills))
    out["coverage"] = out["skills"].apply(
        lambda s: len(s & my_skills) / len(s) if s else 0.0
    )
    out["score"] = (100 * (0.6 * out["similarity"] + 0.4 * out["coverage"])).round(1)
    return out.sort_values("score", ascending=False).reset_index(drop=True)
