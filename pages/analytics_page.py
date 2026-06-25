"""Analytics dashboard page."""

from __future__ import annotations

import streamlit as st

from database.db import load_responses
from utils.analytics import (
    accessibility_heatmap,
    compute_kpis,
    demographic_breakdown_chart,
    experience_radar_chart,
    nps_gauge_chart,
    nps_pie_chart,
    region_feedback_chart,
    render_kpi_cards,
    satisfaction_trend_chart,
    security_analysis_chart,
)


@st.fragment(run_every=30)
def _live_analytics() -> None:
    df = load_responses()
    kpis = compute_kpis(df)

    st.markdown(
        '<div class="live-indicator"><span class="live-dot"></span> Live Dashboard — Auto-refreshes every 30s</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    render_kpi_cards(kpis)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(nps_gauge_chart(kpis["nps_score"]), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(nps_pie_chart(df), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(satisfaction_trend_chart(df), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(accessibility_heatmap(df), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(security_analysis_chart(df), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    c5, c6 = st.columns(2)
    with c5:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.altair_chart(region_feedback_chart(df), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c6:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(demographic_breakdown_chart(df), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(experience_radar_chart(df), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render() -> None:
    st.markdown('<div class="section-title">📊 Analytics Dashboard</div>', unsafe_allow_html=True)
    _live_analytics()
