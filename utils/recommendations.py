"""Election infrastructure recommendation engine."""

from __future__ import annotations

import pandas as pd

from config import ACCESSIBILITY_OPTIONS, EXPERIENCE_METRICS, SECURITY_METRICS


def generate_recommendations(df: pd.DataFrame) -> list[dict]:
    recs: list[dict] = []

    if df.empty:
        return [
            {
                "title": "Establish baseline voter feedback collection",
                "description": "Deploy CAPAI survey kiosks and QR codes at all polling stations.",
                "priority": "High",
                "category": "Operational",
            },
            {
                "title": "Conduct accessibility audit",
                "description": "Review all polling locations for ADA-equivalent compliance.",
                "priority": "High",
                "category": "Accessibility",
            },
        ]

    def add(title: str, description: str, priority: str, category: str) -> None:
        recs.append(
            {"title": title, "description": description, "priority": priority, "category": category}
        )

    if "polling_station_accessibility" in df.columns and df["polling_station_accessibility"].mean() < 7.5:
        add(
            "Add more wheelchair ramps",
            "Multiple regions report accessibility scores below target. Install ramps and accessible entry paths.",
            "High",
            "Accessibility",
        )

    if "waiting_time_satisfaction" in df.columns and df["waiting_time_satisfaction"].mean() < 7:
        add(
            "Reduce queue waiting times",
            "Deploy express lanes, real-time queue displays, and appointment-based voting pilots.",
            "High",
            "Operational",
        )

    if "staff_helpfulness" in df.columns and df["staff_helpfulness"].mean() < 7.5:
        add(
            "Increase polling staff",
            "Staff helpfulness scores indicate capacity gaps during peak voting hours.",
            "Medium",
            "Operational",
        )

    accessibility_mentions = {}
    for items in df.get("accessibility_feedback", []):
        if isinstance(items, list):
            for item in items:
                accessibility_mentions[item] = accessibility_mentions.get(item, 0) + 1

    if accessibility_mentions.get("Signage Visibility", 0) > len(df) * 0.2:
        add(
            "Improve signage",
            "Voters frequently mention signage issues. Deploy high-contrast, multilingual wayfinding.",
            "High",
            "Accessibility",
        )

    if accessibility_mentions.get("Language Assistance", 0) > len(df) * 0.15:
        add(
            "Expand language assistance",
            "Increase multilingual poll workers and translated ballot guides.",
            "Medium",
            "Accessibility",
        )

    if accessibility_mentions.get("Parking Availability", 0) > len(df) * 0.15:
        add(
            "Improve parking infrastructure",
            "Partner with local authorities to expand accessible parking near polling sites.",
            "Medium",
            "Infrastructure",
        )

    security_avg = df[[c for c in SECURITY_METRICS if c in df.columns]].mean().mean()
    if security_avg < 7.5:
        add(
            "Enhance cybersecurity monitoring",
            "Strengthen election system monitoring, audit trails, and public trust communications.",
            "High",
            "Security",
        )
    else:
        add(
            "Maintain cybersecurity monitoring",
            "Continue 24/7 monitoring and publish transparency reports on election security.",
            "Low",
            "Security",
        )

    if "voting_process_clarity" in df.columns and df["voting_process_clarity"].mean() < 7.5:
        add(
            "Better voter awareness campaigns",
            "Launch pre-election education on ballot layout, ID requirements, and voting steps.",
            "Medium",
            "Operational",
        )

    if "technology_effectiveness" in df.columns and df["technology_effectiveness"].mean() < 7:
        add(
            "Upgrade voting technology",
            "Modernize e-poll books and provide offline fallback for technical failures.",
            "High",
            "Technology",
        )

    if "facility_cleanliness" in df.columns and df["facility_cleanliness"].mean() < 7:
        add(
            "Improve facility maintenance standards",
            "Establish pre-election cleaning protocols and supply checklists for all sites.",
            "Low",
            "Infrastructure",
        )

    for opt in ACCESSIBILITY_OPTIONS:
        if accessibility_mentions.get(opt, 0) == 0 and len(df) > 10:
            add(
                f"Verify {opt.lower()} at all sites",
                f"No recent feedback on {opt.lower()} — conduct proactive compliance checks.",
                "Low",
                "Accessibility",
            )
            break

    if not recs:
        add(
            "Sustain excellence program",
            "Metrics are healthy. Document best practices and replicate across regions.",
            "Low",
            "Operational",
        )

    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    recs.sort(key=lambda r: priority_order.get(r["priority"], 3))
    return recs
