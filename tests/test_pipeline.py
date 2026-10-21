from pathlib import Path

from src.clean import load_offers
from src.match import rank_offers

D = Path(__file__).parent.parent / "data"


def test_pipeline_runs_and_ranks():
    df = load_offers(D / "offers_sample.csv")
    assert len(df) == 11  # le doublon a été supprimé
    ranked = rank_offers((D / "cv.txt").read_text(encoding="utf-8"), df)
    assert ranked["score"].is_monotonic_decreasing
    assert ranked["score"].between(0, 100).all()
