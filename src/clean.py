"""Chargement et nettoyage des offres (étape 1 : Data)."""
from pathlib import Path

import pandas as pd

from .skills import extract_skills

REQUIRED = ["title", "company", "city", "description"]


def load_offers(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes dans le CSV : {missing}")
    return clean_offers(df)


def clean_offers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in REQUIRED:
        df[col] = df[col].fillna("").astype(str).str.strip()
    # Supprime les offres vides et les doublons (même titre + entreprise)
    df = df[df["description"].str.len() > 20]
    df = df.drop_duplicates(subset=["title", "company"]).reset_index(drop=True)
    df["text"] = df["title"] + ". " + df["description"]
    df["skills"] = df["text"].apply(extract_skills)
    return df
