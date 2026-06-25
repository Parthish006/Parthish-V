"""AI-driven insights generation from survey data."""

from __future__ import annotations

from collections import Counter

import pandas as pd

from config import ACCESSIBILITY_OPTIONS, EXPERIENCE_METRICS, SECURITY_METRICS


def _lowest_metrics(df: pd.DataFrame, columns: list[str], n: int = 3) -> list[tuple[str, float]]:
    if df.empty:
        return []
    means = {col: df[col].mean() for col in columns if col in df.columns}
    sorted_items = sorted(means.items(), key=lambda x: x[1])
    return sorted_items[:n]


def _top_themes(df: pd.DataFrame, sentiment: str, n: int = 5) -> list[str]:
    if df.empty or "open_feedback" not in df.columns:
        return []
    texts = df[df["sentiment"] == sentiment]["open_feedback"].dropna().astype(str)
    keywords = []
    for text in texts:
        for word in text.lower().split():
            cleaned = word.strip(".,!?;:'\"()[]")
            if len(cleaned) > 4:
                keywords.append(cleaned)
    return [w for w, _ in Counter(keywords).most_common(n)]


def generate_insights(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "key_concerns": ["Insufficient data — collect more survey responses."],
            "positive_themes": ["No positive themes identified yet."],
            "accessibility_recommendations": ["Deploy baseline accessibility audits at polling stations."],
            "security_suggestions": ["Maintain current security protocols and monitor continuously."],
            "operational_improvements": ["Increase voter outreach to gather representative feedback."],
            "summary": "Awaiting voter feedback data to generate AI insights.",
        }

    concerns = []
    low_exp = _lowest_metrics(df, EXPERIENCE_METRICS)
    for metric, score in low_exp:
        label = metric.replace("_", " ").title()
        if score < 7:
            concerns.append(f"Low {label} rating ({score:.1f}/10) — requires attention.")

    detractor_pct = (df["nps_category"] == "Detractor").mean() * 100 if "nps_category" in df.columns else 0
    if detractor_pct > 20:
        concerns.append(f"High detractor rate ({detractor_pct:.0f}%) — investigate root causes.")

    negative_df = df[df["sentiment"] == "Negative"]
    if not negative_df.empty:
        concerns.append(f"{len(negative_df)} responses flagged with negative sentiment in open feedback.")

    if not concerns:
        concerns = ["No critical concerns detected — maintain monitoring cadence."]

    positive = _top_themes(df, "Positive")
    if not positive:
        positive = ["Helpful staff", "Secure process", "Clean facilities"]

    accessibility_counts = Counter()
    for items in df.get("accessibility_feedback", []):
        if isinstance(items, list):
            accessibility_counts.update(items)

    missing = [opt for opt in ACCESSIBILITY_OPTIONS if accessibility_counts.get(opt, 0) < len(df) * 0.3]
    accessibility_recs = []
    for item in missing[:4]:
        accessibility_recs.append(f"Expand {item.lower()} coverage across underserved polling locations.")
    if not accessibility_recs:
        accessibility_recs = ["Sustain accessibility investments and publish compliance reports."]

    security_low = _lowest_metrics(df, SECURITY_METRICS, 2)
    security_suggestions = []
    for metric, score in security_low:
        if score < 7.5:
            security_suggestions.append(
                f"Strengthen {metric.replace('_', ' ')} — current average {score:.1f}/10."
            )
    if not security_suggestions:
        security_suggestions = ["Security metrics are strong — continue transparent communication."]

    operational = []
    if "waiting_time_satisfaction" in df.columns and df["waiting_time_satisfaction"].mean() < 7:
        operational.append("Deploy queue management and additional staff during peak hours.")
    if "signage" in " ".join(concerns).lower() or "Signage Visibility" in missing:
        operational.append("Upgrade bilingual signage and wayfinding at all entry points.")
    if "technology_effectiveness" in df.columns and df["technology_effectiveness"].mean() < 7:
        operational.append("Modernize voter check-in technology and provide backup systems.")
    operational.append("Launch targeted voter education campaigns before the next election cycle.")

    avg_sat = df[[c for c in EXPERIENCE_METRICS if c in df.columns]].mean().mean()
    nps = ((df["nps_score"] >= 9).mean() - (df["nps_score"] <= 6).mean()) * 100

    summary = (
        f"Analysis of {len(df)} responses shows average satisfaction {avg_sat:.1f}/10 "
        f"with NPS {nps:.0f}. Priority focus areas include "
        f"{', '.join(c.replace('_', ' ').title() for c, _ in low_exp[:2]) if low_exp else 'operational excellence'}."
    )

    return {
        "key_concerns": concerns[:5],
        "positive_themes": positive,
        "accessibility_recommendations": accessibility_recs,
        "security_suggestions": security_suggestions,
        "operational_improvements": operational[:5],
        "summary": summary,
    }


def priority_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Impact vs effort matrix for improvement areas."""
    items = [
        ("Queue Management", 8, 4),
        ("Wheelchair Ramps", 9, 6),
        ("Signage Upgrade", 7, 3),
        ("Staff Training", 8, 5),
        ("Cybersecurity Monitoring", 9, 7),
        ("Voter Awareness Campaign", 6, 3),
        ("Language Assistance", 8, 5),
        ("Parking Infrastructure", 5, 6),
    ]

    if not df.empty:
        if "waiting_time_satisfaction" in df.columns and df["waiting_time_satisfaction"].mean() < 7:
            items[0] = ("Queue Management", 9, 4)
        if "polling_station_accessibility" in df.columns and df["polling_station_accessibility"].mean() < 7:
            items[1] = ("Wheelchair Ramps", 10, 6)

    return pd.DataFrame(items, columns=["Initiative", "Impact", "Effort"])
