"""NPS calculation utilities."""

from __future__ import annotations

import pandas as pd


def classify_nps(score: int) -> str:
    if score >= 9:
        return "Promoter"
    if score >= 7:
        return "Passive"
    return "Detractor"


def calculate_nps(df: pd.DataFrame) -> float:
    if df.empty or "nps_score" not in df.columns:
        return 0.0

    total = len(df)
    promoters = (df["nps_score"] >= 9).sum()
    detractors = (df["nps_score"] <= 6).sum()
    return round(((promoters / total) - (detractors / total)) * 100, 1)


def nps_breakdown(df: pd.DataFrame) -> dict[str, int]:
    if df.empty:
        return {"Promoter": 0, "Passive": 0, "Detractor": 0}
    counts = df["nps_category"].value_counts().to_dict()
    return {
        "Promoter": int(counts.get("Promoter", 0)),
        "Passive": int(counts.get("Passive", 0)),
        "Detractor": int(counts.get("Detractor", 0)),
    }
