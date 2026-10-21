"""Explication du score (étape 4).

- Sans clé API : explication à base de règles (compétences en commun / manquantes).
- Avec ANTHROPIC_API_KEY : un LLM rédige une explication personnalisée en français.
"""
import os


def explain_rules(row) -> str:
    matched = ", ".join(row["matched"]) or "aucune compétence listée en commun"
    missing = ", ".join(row["missing"]) or "rien de bloquant"
    return (
        f"**Ce qui colle :** {matched}.\n\n"
        f"**À renforcer :** {missing}."
    )


def explain_llm(row, cv_text: str) -> str:
    import anthropic  # pip install anthropic

    client = anthropic.Anthropic()
    prompt = f"""Tu aides une étudiante à choisir ses candidatures d'alternance.
Voici son CV :
{cv_text}

Voici l'offre : {row['title']} chez {row['company']} ({row['city']})
{row['description']}

Compétences en commun détectées : {row['matched']}
Compétences à renforcer : {row['missing']}

En 5 lignes maximum, en français : (1) pourquoi cette offre lui correspond, (2) ce qui lui manque,
(3) un conseil concret pour la lettre de motivation. Sois honnête, ne surestime pas son niveau."""
    msg = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5"),
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def explain(row, cv_text: str) -> str:
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            return explain_llm(row, cv_text)
        except Exception as e:  # on retombe sur les règles si l'API échoue
            return explain_rules(row) + f"\n\n_(LLM indisponible : {e})_"
    return explain_rules(row)
