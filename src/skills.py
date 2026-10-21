"""Vocabulaire de compétences recherchées dans les offres et dans le CV.

Chaque compétence a un nom canonique et une liste de variantes (minuscules).
Tu peux enrichir ce dictionnaire : c'est la base de l'analyse ET du matching.
"""

import re

SKILLS = {
    "Python": [r"python"],
    "SQL": [r"sql", r"postgresql", r"mysql"],
    "C": [r"langage c\b"],  # + cas particulier du "C" majuscule ci-dessous
    "Pandas": [r"pandas"],
    "Scikit-learn": [r"scikit-learn", r"sklearn"],
    "Machine Learning": [r"machine learning", r"apprentissage automatique", r"\bml\b"],
    "Deep Learning": [r"deep learning", r"pytorch", r"tensorflow", r"réseaux de neurones"],
    "NLP / LLM": [r"\bnlp\b", r"\bllm", r"langage naturel", r"ia générative", r"\brag\b", r"prompt"],
    "Data Visualisation": [r"power bi", r"tableau\b(?! de bord)", r"dataviz", r"visualisation", r"matplotlib"],
    "Statistiques": [r"statistique", r"probabilité"],
    "Git / GitHub": [r"\bgit\b", r"github", r"gitlab"],
    "Cloud": [r"\baws\b", r"azure", r"\bgcp\b", r"cloud"],
    "Docker": [r"docker", r"conteneur"],
    "ETL / Data Engineering": [r"\betl\b", r"pipeline", r"airflow", r"data engineering", r"spark"],
    "Excel": [r"excel"],
    "Cybersécurité": [r"cybersécurité", r"sécurité informatique", r"\bsoc\b"],
    "Anglais": [r"anglais", r"english"],
    "Travail en équipe": [r"équipe", r"collaboratif"],
    "Autonomie": [r"autonomie", r"autonome"],
}

# "C" doit rester sensible à la casse (sinon "c'est" serait pris pour le langage C)
_C_PATTERN = re.compile(r"(?<![\w+#])C(?![\w+#'’])")
_COMPILED = {n: [re.compile(p, re.IGNORECASE) for p in ps] for n, ps in SKILLS.items()}


def extract_skills(text: str) -> set[str]:
    """Retourne l'ensemble des compétences canoniques détectées dans un texte."""
    found = {n for n, pats in _COMPILED.items() if any(p.search(text) for p in pats)}
    if _C_PATTERN.search(text):
        found.add("C")
    return found
