"""Chart and KPI analytics helpers."""

from __future__ import annotations

import altair as alt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import EXPERIENCE_LABELS, EXPERIENCE_METRICS, SECURITY_LABELS, SECURITY_METRICS
from utils.nps import calculate_nps, nps_breakdown


def compute_kpis(df: pd.DataFrame) -> dict[str, float | int]:
    if df.empty:
        return {
            "total_responses": 0,
            "avg_satisfaction": 0.0,
            "nps_score": 0.0,
            "accessibility_rating": 0.0,
            "security_rating": 0.0,
        }

    experience_cols = [c for c in EXPERIENCE_METRICS if c in df.columns]
    security_cols = [c for c in SECURITY_METRICS if c in df.columns]

    return {
        "total_responses": len(df),
        "avg_satisfaction": round(df[experience_cols].mean().mean(), 2) if experience_cols else 0.0,
        "nps_score": calculate_nps(df),
        "accessibility_rating": round(df["polling_station_accessibility"].mean(), 2)
        if "polling_station_accessibility" in df.columns
        else 0.0,
        "security_rating": round(df[security_cols].mean().mean(), 2) if security_cols else 0.0,
    }


def nps_gauge_chart(nps: float) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=nps,
            title={"text": "Net Promoter Score", "font": {"size": 20, "color": "#1E293B"}},
            delta={"reference": 50, "increasing": {"color": "#10B981"}},
            gauge={
                "axis": {"range": [-100, 100], "tickwidth": 1},
                "bar": {"color": "#0A66FF"},
                "steps": [
                    {"range": [-100, 0], "color": "rgba(239,68,68,0.25)"},
                    {"range": [0, 50], "color": "rgba(245,158,11,0.25)"},
                    {"range": [50, 100], "color": "rgba(16,185,129,0.25)"},
                ],
                "threshold": {
                    "line": {"color": "#4F46E5", "width": 4},
                    "thickness": 0.75,
                    "value": nps,
                },
            },
            number={"suffix": "", "font": {"size": 36, "color": "#0A66FF"}},
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=20, r=20, t=50, b=20),
        font={"family": "Segoe UI, sans-serif"},
    )
    return fig


def satisfaction_trend_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", showarrow=False, font={"size": 16})
        return fig

    trend = df.copy()
    trend["date"] = pd.to_datetime(trend["created_at"]).dt.date
    daily = (
        trend.groupby("date")["overall_voting_experience"]
        .mean()
        .reset_index()
        .sort_values("date")
    )

    fig = px.line(
        daily,
        x="date",
        y="overall_voting_experience",
        markers=True,
        color_discrete_sequence=["#0A66FF"],
        labels={"date": "Date", "overall_voting_experience": "Avg Satisfaction"},
    )
    fig.update_traces(line={"width": 3}, marker={"size": 8})
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=360,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis={"gridcolor": "rgba(10,102,255,0.1)"},
        yaxis={"gridcolor": "rgba(10,102,255,0.1)", "range": [0, 10]},
    )
    return fig


def accessibility_heatmap(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", showarrow=False)
        return fig

    rows = []
    for _, row in df.iterrows():
        items = row.get("accessibility_feedback") or []
        if isinstance(items, list):
            for item in items:
                rows.append({"Feature": item, "Region": row.get("region", "Unknown")})

    if not rows:
        fig = go.Figure()
        fig.add_annotation(text="No accessibility feedback recorded", showarrow=False)
        return fig

    heat_df = pd.DataFrame(rows)
    pivot = heat_df.groupby(["Feature", "Region"]).size().reset_index(name="Count")
    matrix = pivot.pivot(index="Feature", columns="Region", values="Count").fillna(0)

    fig = px.imshow(
        matrix.values,
        x=list(matrix.columns),
        y=list(matrix.index),
        color_continuous_scale=[[0, "#E0F2FE"], [0.5, "#00B4FF"], [1, "#0A66FF"]],
        aspect="auto",
        labels={"color": "Mentions"},
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=380,
        margin=dict(l=20, r=20, t=30, b=20),
    )
    return fig


def security_analysis_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", showarrow=False)
        return fig

    means = [df[col].mean() for col in SECURITY_METRICS if col in df.columns]
    labels = [SECURITY_LABELS[col] for col in SECURITY_METRICS if col in df.columns]

    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=means,
                marker={
                    "color": means,
                    "colorscale": [[0, "#00B4FF"], [1, "#0A66FF"]],
                    "line": {"width": 0},
                },
                text=[f"{v:.1f}" for v in means],
                textposition="outside",
            )
        ]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=360,
        yaxis={"range": [0, 10], "gridcolor": "rgba(10,102,255,0.1)"},
        xaxis={"tickangle": -15},
        margin=dict(l=20, r=20, t=30, b=80),
        showlegend=False,
    )
    return fig


def region_feedback_chart(df: pd.DataFrame) -> alt.Chart:
    if df.empty:
        return alt.Chart(pd.DataFrame({"region": [], "score": []})).mark_bar()

    region_df = (
        df.groupby("region")["overall_voting_experience"]
        .mean()
        .reset_index()
        .rename(columns={"overall_voting_experience": "score"})
    )

    return (
        alt.Chart(region_df)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X("region:N", title="Region", sort="-y"),
            y=alt.Y("score:Q", title="Avg Satisfaction", scale=alt.Scale(domain=[0, 10])),
            color=alt.Color("score:Q", scale=alt.Scale(range=["#00B4FF", "#0A66FF"]), legend=None),
            tooltip=["region", alt.Tooltip("score:Q", format=".2f")],
        )
        .properties(height=360)
        .configure_view(strokeWidth=0)
        .configure_axis(gridColor="rgba(10,102,255,0.15)")
    )


def demographic_breakdown_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", showarrow=False)
        return fig

    age_counts = df["age_group"].value_counts().reset_index()
    age_counts.columns = ["Age Group", "Count"]

    fig = px.pie(
        age_counts,
        names="Age Group",
        values="Count",
        hole=0.45,
        color_discrete_sequence=px.colors.sequential.Blues_r,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=360,
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=False,
    )
    return fig


def nps_pie_chart(df: pd.DataFrame) -> go.Figure:
    breakdown = nps_breakdown(df)
    labels = list(breakdown.keys())
    values = list(breakdown.values())
    colors = {"Promoter": "#10B981", "Passive": "#F59E0B", "Detractor": "#EF4444"}

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.5,
                marker={"colors": [colors.get(l, "#0A66FF") for l in labels]},
                textinfo="label+percent",
            )
        ]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=360,
        margin=dict(l=20, r=20, t=30, b=20),
    )
    return fig


def experience_radar_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", showarrow=False)
        return fig

    categories = [EXPERIENCE_LABELS[c] for c in EXPERIENCE_METRICS if c in df.columns]
    values = [df[c].mean() for c in EXPERIENCE_METRICS if c in df.columns]
    values_closed = values + [values[0]] if values else values
    categories_closed = categories + [categories[0]] if categories else categories

    fig = go.Figure(
        data=go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill="toself",
            fillcolor="rgba(10,102,255,0.25)",
            line={"color": "#0A66FF", "width": 2},
            name="Experience",
        )
    )
    fig.update_layout(
        polar={
            "radialaxis": {"visible": True, "range": [0, 10], "gridcolor": "rgba(10,102,255,0.2)"},
            "angularaxis": {"gridcolor": "rgba(10,102,255,0.2)"},
            "bgcolor": "rgba(0,0,0,0)",
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
        margin=dict(l=60, r=60, t=40, b=40),
        showlegend=False,
    )
    return fig


def render_kpi_cards(kpis: dict[str, float | int]) -> None:
    cols = st.columns(5)
    cards = [
        ("Total Responses", kpis["total_responses"], "📋", ""),
        ("Avg Satisfaction", kpis["avg_satisfaction"], "⭐", "/10"),
        ("NPS Score", kpis["nps_score"], "📈", ""),
        ("Accessibility", kpis["accessibility_rating"], "♿", "/10"),
        ("Security", kpis["security_rating"], "🔒", "/10"),
    ]
    for col, (label, value, icon, suffix) in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">{icon}</div>
                    <div class="kpi-value">{value}{suffix}</div>
                    <div class="kpi-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
