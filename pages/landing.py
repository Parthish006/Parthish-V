"""Landing page for CAPAI."""

from __future__ import annotations

import streamlit as st

from database.db import load_responses
from utils.analytics import compute_kpis
from utils.logo import render_logo


def render() -> None:
    df = load_responses()
    kpis = compute_kpis(df)

    render_logo(width=120, centered=True)

    st.markdown(
        """
        <div class="hero-section">
            <div class="hero-title">CAPAI</div>
            <div class="hero-tagline">Transforming Voter Feedback into Better Elections</div>
            <p style="color:#64748B; max-width:700px; margin:0 auto 1.5rem; line-height:1.6;">
                A world-class voter experience platform that empowers election authorities
                with real-time analytics, NPS tracking, and AI-driven infrastructure recommendations.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    stats = [
        (f"{kpis['total_responses']:,}", "Survey Responses"),
        (f"{kpis['avg_satisfaction']}", "Avg Satisfaction"),
        (f"{kpis['nps_score']}", "NPS Score"),
        ("24/7", "Real-Time Monitoring"),
    ]
    for col, (value, label) in zip([c1, c2, c3, c4], stats):
        with col:
            st.markdown(
                f"""
                <div class="glass-card" style="text-align:center;">
                    <div class="stat-counter">{value}</div>
                    <div class="stat-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🗳️ Start Voter Survey", use_container_width=False, type="primary"):
        st.session_state.page = "Voter Survey"
        st.rerun()

    st.markdown('<div class="section-title">Platform Features</div>', unsafe_allow_html=True)

    features = [
        ("📊", "Real-Time Analytics", "Interactive dashboards with NPS gauges, trend analysis, and demographic breakdowns."),
        ("🤖", "AI-Powered Insights", "Automated sentiment analysis, theme extraction, and priority recommendations."),
        ("♿", "Accessibility Tracking", "Monitor wheelchair access, signage, language support, and senior citizen services."),
        ("🔒", "Security Monitoring", "Track voter confidence in election security and process transparency."),
        ("🏛️", "Infrastructure Engine", "Actionable recommendations for polling station improvements."),
        ("📄", "Export & Reporting", "Download CSV and PDF reports for election commission briefings."),
    ]

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="glass-card" style="margin-top:2rem; text-align:center;">
            <div style="font-size:3rem; margin-bottom:0.5rem;">🏛️🗳️📊</div>
            <div style="font-weight:700; font-size:1.2rem; color:#0A66FF;">
                Election Infrastructure Intelligence
            </div>
            <div style="color:#64748B; margin-top:0.5rem;">
                From polling booth feedback to national-level policy recommendations —
                CAPAI bridges the gap between voters and election authorities.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
