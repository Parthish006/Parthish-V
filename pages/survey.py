"""Voter survey page."""

from __future__ import annotations

import streamlit as st

from config import (
    ACCESSIBILITY_OPTIONS,
    AGE_GROUPS,
    EXPERIENCE_LABELS,
    EXPERIENCE_METRICS,
    GENDERS,
    REGIONS,
    SECURITY_LABELS,
    SECURITY_METRICS,
    URBAN_RURAL,
)
from database.db import insert_response
from utils.nps import classify_nps
from utils.sentiment import analyze_sentiment


def render() -> None:
    st.markdown('<div class="section-title">🗳️ Voter Experience Survey</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#64748B;">Your feedback helps improve election infrastructure for all citizens.</p>',
        unsafe_allow_html=True,
    )

    with st.form("voter_survey", clear_on_submit=True):
        st.markdown('<div class="survey-section">', unsafe_allow_html=True)
        st.subheader("Basic Information")
        c1, c2 = st.columns(2)
        with c1:
            age_group = st.selectbox("Age Group", AGE_GROUPS)
            gender = st.selectbox("Gender", GENDERS)
            region = st.selectbox("Region", REGIONS)
        with c2:
            urban_rural = st.selectbox("Urban / Rural", URBAN_RURAL)
            first_time = st.radio("First Time Voter?", ["Yes", "No"], horizontal=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="survey-section">', unsafe_allow_html=True)
        st.subheader("Voting Experience (Rate 1–10)")
        experience_scores = {}
        cols = st.columns(2)
        for i, metric in enumerate(EXPERIENCE_METRICS):
            with cols[i % 2]:
                experience_scores[metric] = st.slider(
                    EXPERIENCE_LABELS[metric], 1, 10, 7, key=f"exp_{metric}"
                )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="survey-section">', unsafe_allow_html=True)
        st.subheader("Net Promoter Score")
        nps_score = st.slider(
            "How likely are you to recommend this voting experience to other citizens? (0–10)",
            0,
            10,
            8,
        )
        nps_category = classify_nps(nps_score)
        badge_class = {
            "Promoter": "nps-badge-promoter",
            "Passive": "nps-badge-passive",
            "Detractor": "nps-badge-detractor",
        }[nps_category]
        st.markdown(
            f'<p>Classification: <span class="{badge_class}">{nps_category}</span></p>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="survey-section">', unsafe_allow_html=True)
        st.subheader("Accessibility Feedback")
        accessibility = st.multiselect(
            "Which accessibility features did you use or notice?",
            ACCESSIBILITY_OPTIONS,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="survey-section">', unsafe_allow_html=True)
        st.subheader("Security Feedback (Rate 1–10)")
        security_scores = {}
        for metric in SECURITY_METRICS:
            security_scores[metric] = st.slider(
                SECURITY_LABELS[metric], 1, 10, 8, key=f"sec_{metric}"
            )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="survey-section">', unsafe_allow_html=True)
        st.subheader("Open Feedback")
        open_feedback = st.text_area(
            "Share suggestions for improving future elections.",
            placeholder="Tell us about your experience...",
            height=120,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        submitted = st.form_submit_button("Submit Survey ✓", use_container_width=True, type="primary")

    if submitted:
        sentiment, sentiment_score = analyze_sentiment(open_feedback)
        data = {
            "age_group": age_group,
            "gender": gender,
            "region": region,
            "urban_rural": urban_rural,
            "first_time_voter": first_time,
            **experience_scores,
            "nps_score": nps_score,
            "nps_category": nps_category,
            "accessibility_feedback": accessibility,
            **security_scores,
            "open_feedback": open_feedback,
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
        }
        row_id = insert_response(data)
        st.success(f"Thank you! Your feedback has been recorded (Response #{row_id}).")
        st.balloons()
