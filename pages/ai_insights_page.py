"""AI insights page."""

from __future__ import annotations

import io

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud

from database.db import load_responses
from utils.ai_insights import generate_insights, priority_matrix


def _wordcloud_image(texts: list[str]) -> bytes | None:
    if not texts:
        return None
    combined = " ".join(texts)
    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        colormap="Blues",
        max_words=80,
    ).generate(combined)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=120)
    plt.close(fig)
    buf.seek(0)
    return buf.read()


def render() -> None:
    st.markdown('<div class="section-title">🤖 AI Insights</div>', unsafe_allow_html=True)

    df = load_responses()
    insights = generate_insights(df)

    st.markdown(
        f"""
        <div class="glass-card">
            <div style="font-weight:700; color:#0A66FF; margin-bottom:0.5rem;">AI Executive Summary</div>
            <div style="line-height:1.6; color:#64748B;">{insights["summary"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-title" style="font-size:1.2rem;">Key Voter Concerns</div>', unsafe_allow_html=True)
        for concern in insights["key_concerns"]:
            st.markdown(f'<div class="insight-card">{concern}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title" style="font-size:1.2rem;">Accessibility Recommendations</div>', unsafe_allow_html=True)
        for rec in insights["accessibility_recommendations"]:
            st.markdown(f'<div class="insight-card">{rec}</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="section-title" style="font-size:1.2rem;">Positive Feedback Themes</div>', unsafe_allow_html=True)
        for theme in insights["positive_themes"]:
            st.markdown(
                f'<div class="insight-card" style="border-left-color:#10B981;">✅ {theme.title()}</div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div class="section-title" style="font-size:1.2rem;">Security Suggestions</div>', unsafe_allow_html=True)
        for sug in insights["security_suggestions"]:
            st.markdown(f'<div class="insight-card">{sug}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="font-size:1.2rem;">Operational Improvements</div>', unsafe_allow_html=True)
    op_cols = st.columns(len(insights["operational_improvements"]))
    for col, item in zip(op_cols, insights["operational_improvements"]):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <div class="feature-desc">{item}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)

    with c3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Feedback Word Cloud")
        texts = df["open_feedback"].dropna().astype(str).tolist() if not df.empty else []
        img_bytes = _wordcloud_image(texts)
        if img_bytes:
            st.image(img_bytes, use_container_width=True)
        else:
            st.info("Submit survey responses to generate a word cloud.")
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Sentiment Analysis")
        if not df.empty and "sentiment" in df.columns:
            sentiment_counts = df["sentiment"].value_counts().reset_index()
            sentiment_counts.columns = ["Sentiment", "Count"]
            color_map = {"Positive": "#10B981", "Neutral": "#F59E0B", "Negative": "#EF4444"}
            fig = px.bar(
                sentiment_counts,
                x="Sentiment",
                y="Count",
                color="Sentiment",
                color_discrete_map=color_map,
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                height=350,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sentiment data available yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Improvement Priority Matrix")
    matrix_df = priority_matrix(df)
    fig = px.scatter(
        matrix_df,
        x="Effort",
        y="Impact",
        text="Initiative",
        size=[30] * len(matrix_df),
        color="Impact",
        color_continuous_scale=["#00B4FF", "#0A66FF"],
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
        xaxis={"title": "Effort (Lower is Better)", "range": [0, 11]},
        yaxis={"title": "Impact (Higher is Better)", "range": [0, 11]},
    )
    fig.add_hline(y=7, line_dash="dash", line_color="rgba(10,102,255,0.3)")
    fig.add_vline(x=5, line_dash="dash", line_color="rgba(10,102,255,0.3)")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
