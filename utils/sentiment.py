"""Sentiment analysis using TextBlob."""

from __future__ import annotations

from textblob import TextBlob


def analyze_sentiment(text: str) -> tuple[str, float]:
    if not text or not str(text).strip():
        return "Neutral", 0.0

    polarity = TextBlob(str(text)).sentiment.polarity
    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"
    return label, round(float(polarity), 3)
