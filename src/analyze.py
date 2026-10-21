"""Analyse du marché : quelles compétences reviennent le plus ? (étape 2)"""
from collections import Counter

import pandas as pd


def skill_frequency(df: pd.DataFrame) -> pd.DataFrame:
    counts = Counter(s for skills in df["skills"] for s in skills)
    out = pd.DataFrame(counts.items(), columns=["skill", "n_offers"])
    out["pct_offers"] = (100 * out["n_offers"] / len(df)).round(1)
    return out.sort_values("n_offers", ascending=False).reset_index(drop=True)


def offers_by(df: pd.DataFrame, column: str) -> pd.Series:
    return df[column].value_counts()


def skill_gap(df: pd.DataFrame, my_skills: set[str]) -> pd.DataFrame:
    """Compétences demandées par le marché que tu n'as pas encore : ta feuille de route."""
    freq = skill_frequency(df)
    freq["tu_l_as"] = freq["skill"].isin(my_skills)
    return freq
