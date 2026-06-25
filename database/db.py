"""SQLite database operations for CAPAI survey responses."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from config import DB_PATH


def _ensure_db_dir() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    _ensure_db_dir()
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS survey_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            age_group TEXT,
            gender TEXT,
            region TEXT,
            urban_rural TEXT,
            first_time_voter TEXT,
            polling_station_accessibility REAL,
            staff_helpfulness REAL,
            waiting_time_satisfaction REAL,
            security_confidence REAL,
            voting_process_clarity REAL,
            facility_cleanliness REAL,
            technology_effectiveness REAL,
            overall_voting_experience REAL,
            nps_score INTEGER,
            nps_category TEXT,
            accessibility_feedback TEXT,
            safety_at_polling_station REAL,
            trust_in_election_process REAL,
            confidence_in_vote_security REAL,
            open_feedback TEXT,
            sentiment TEXT,
            sentiment_score REAL
        )
        """
    )
    conn.commit()
    conn.close()


def seed_sample_data() -> None:
    """Seed demo data when database is empty."""
    df = load_responses()
    if not df.empty:
        return

    import random

    from config import ACCESSIBILITY_OPTIONS, AGE_GROUPS, GENDERS, REGIONS, URBAN_RURAL
    from utils.nps import classify_nps
    from utils.sentiment import analyze_sentiment

    samples = [
        "Great experience, staff were very helpful and the process was smooth.",
        "Long waiting times but overall secure and well organized.",
        "Need better wheelchair access and clearer signage at the entrance.",
        "Excellent security measures and friendly poll workers.",
        "Confusing ballot layout, please improve voter education materials.",
        "Clean facility and efficient technology at check-in.",
        "Parking was limited and language assistance was unavailable.",
        "Very transparent process, I felt my vote was counted securely.",
    ]

    conn = get_connection()
    for i in range(48):
        nps = random.randint(0, 10)
        feedback = random.choice(samples)
        sentiment, score = analyze_sentiment(feedback)
        accessibility = random.sample(
            ACCESSIBILITY_OPTIONS, k=random.randint(1, min(3, len(ACCESSIBILITY_OPTIONS)))
        )
        created = datetime(2026, 1, 1).replace(
            day=min(28, 1 + (i % 28)),
            hour=8 + (i % 10),
            minute=(i * 7) % 60,
        )

        conn.execute(
            """
            INSERT INTO survey_responses (
                created_at, age_group, gender, region, urban_rural, first_time_voter,
                polling_station_accessibility, staff_helpfulness, waiting_time_satisfaction,
                security_confidence, voting_process_clarity, facility_cleanliness,
                technology_effectiveness, overall_voting_experience,
                nps_score, nps_category, accessibility_feedback,
                safety_at_polling_station, trust_in_election_process, confidence_in_vote_security,
                open_feedback, sentiment, sentiment_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                created.isoformat(),
                random.choice(AGE_GROUPS),
                random.choice(GENDERS),
                random.choice(REGIONS),
                random.choice(URBAN_RURAL),
                random.choice(["Yes", "No"]),
                random.uniform(5, 10),
                random.uniform(5, 10),
                random.uniform(4, 10),
                random.uniform(6, 10),
                random.uniform(5, 10),
                random.uniform(6, 10),
                random.uniform(5, 10),
                random.uniform(5, 10),
                nps,
                classify_nps(nps),
                json.dumps(accessibility),
                random.uniform(6, 10),
                random.uniform(6, 10),
                random.uniform(6, 10),
                feedback,
                sentiment,
                score,
            ),
        )
    conn.commit()
    conn.close()


def insert_response(data: dict[str, Any]) -> int:
    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO survey_responses (
            created_at, age_group, gender, region, urban_rural, first_time_voter,
            polling_station_accessibility, staff_helpfulness, waiting_time_satisfaction,
            security_confidence, voting_process_clarity, facility_cleanliness,
            technology_effectiveness, overall_voting_experience,
            nps_score, nps_category, accessibility_feedback,
            safety_at_polling_station, trust_in_election_process, confidence_in_vote_security,
            open_feedback, sentiment, sentiment_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().isoformat(),
            data.get("age_group"),
            data.get("gender"),
            data.get("region"),
            data.get("urban_rural"),
            data.get("first_time_voter"),
            data.get("polling_station_accessibility"),
            data.get("staff_helpfulness"),
            data.get("waiting_time_satisfaction"),
            data.get("security_confidence"),
            data.get("voting_process_clarity"),
            data.get("facility_cleanliness"),
            data.get("technology_effectiveness"),
            data.get("overall_voting_experience"),
            data.get("nps_score"),
            data.get("nps_category"),
            json.dumps(data.get("accessibility_feedback", [])),
            data.get("safety_at_polling_station"),
            data.get("trust_in_election_process"),
            data.get("confidence_in_vote_security"),
            data.get("open_feedback"),
            data.get("sentiment"),
            data.get("sentiment_score"),
        ),
    )
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return int(row_id)


def load_responses(
    region: str | None = None,
    age_group: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> pd.DataFrame:
    conn = get_connection()
    query = "SELECT * FROM survey_responses WHERE 1=1"
    params: list[Any] = []

    if region and region != "All Regions":
        query += " AND region = ?"
        params.append(region)
    if age_group and age_group != "All Age Groups":
        query += " AND age_group = ?"
        params.append(age_group)
    if date_from:
        query += " AND date(created_at) >= date(?)"
        params.append(date_from)
    if date_to:
        query += " AND date(created_at) <= date(?)"
        params.append(date_to)

    query += " ORDER BY created_at DESC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()

    if not df.empty and "accessibility_feedback" in df.columns:
        df["accessibility_feedback"] = df["accessibility_feedback"].apply(
            lambda x: json.loads(x) if isinstance(x, str) and x else []
        )
    return df


def delete_response(response_id: int) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM survey_responses WHERE id = ?", (response_id,))
    conn.commit()
    conn.close()
