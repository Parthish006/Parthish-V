"""Infrastructure recommendations page."""

from __future__ import annotations

import streamlit as st

from database.db import load_responses
from utils.recommendations import generate_recommendations


def render() -> None:
    st.markdown(
        '<div class="section-title">🏛️ Election Infrastructure Recommendations</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#64748B;">AI-generated actionable recommendations based on voter feedback analysis.</p>',
        unsafe_allow_html=True,
    )

    df = load_responses()
    recommendations = generate_recommendations(df)

    high = [r for r in recommendations if r["priority"] == "High"]
    medium = [r for r in recommendations if r["priority"] == "Medium"]
    low = [r for r in recommendations if r["priority"] == "Low"]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("🔴 High Priority", len(high))
    with c2:
        st.metric("🟡 Medium Priority", len(medium))
    with c3:
        st.metric("🟢 Low Priority", len(low))

    st.markdown("<br>", unsafe_allow_html=True)

    for rec in recommendations:
        badge_class = f"badge badge-{rec['priority'].lower()}"
        st.markdown(
            f"""
            <div class="rec-card priority-{rec['priority'].lower()}">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                    <div style="font-weight:700; font-size:1.1rem;">{rec['title']}</div>
                    <span class="{badge_class}">{rec['priority']}</span>
                </div>
                <div style="color:#64748B; line-height:1.5; margin-bottom:0.5rem;">{rec['description']}</div>
                <div style="font-size:0.8rem; color:#0A66FF; font-weight:600;">📁 {rec['category']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
