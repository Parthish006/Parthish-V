"""Admin dashboard page."""

from __future__ import annotations

from datetime import date

import streamlit as st

from config import AGE_GROUPS, REGIONS
from database.db import delete_response, load_responses
from utils.analytics import compute_kpis
from utils.exports import export_csv, export_pdf


def render() -> None:
    st.markdown('<div class="section-title">⚙️ Admin Panel</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Filters")
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        region_filter = st.selectbox("Region", ["All Regions"] + REGIONS, key="admin_region")
    with fc2:
        age_filter = st.selectbox("Age Group", ["All Age Groups"] + AGE_GROUPS, key="admin_age")
    with fc3:
        date_from = st.date_input("From Date", value=None, key="admin_from")
    with fc4:
        date_to = st.date_input("To Date", value=None, key="admin_to")
    st.markdown("</div>", unsafe_allow_html=True)

    df = load_responses(
        region=region_filter,
        age_group=age_filter,
        date_from=str(date_from) if date_from else None,
        date_to=str(date_to) if date_to else None,
    )

    kpis = compute_kpis(df)
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.metric("Filtered Responses", kpis["total_responses"])
    with mc2:
        st.metric("NPS Score", kpis["nps_score"])
    with mc3:
        st.metric("Avg Satisfaction", f"{kpis['avg_satisfaction']}/10")

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Export Reports")
    ec1, ec2 = st.columns(2)
    with ec1:
        st.download_button(
            "📥 Download CSV",
            data=export_csv(df),
            file_name=f"capai_responses_{date.today().isoformat()}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with ec2:
        st.download_button(
            "📄 Download PDF Report",
            data=export_pdf(df),
            file_name=f"capai_report_{date.today().isoformat()}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Response Management")
    if df.empty:
        st.info("No responses match the current filters.")
    else:
        display_df = df.copy()
        if "accessibility_feedback" in display_df.columns:
            display_df["accessibility_feedback"] = display_df["accessibility_feedback"].apply(
                lambda x: ", ".join(x) if isinstance(x, list) else str(x)
            )
        show_cols = [
            "id", "created_at", "region", "age_group", "gender",
            "nps_score", "nps_category", "overall_voting_experience",
            "sentiment", "open_feedback",
        ]
        show_cols = [c for c in show_cols if c in display_df.columns]
        st.dataframe(display_df[show_cols], use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("Delete Response")
        dc1, dc2 = st.columns([3, 1])
        with dc1:
            delete_id = st.number_input("Response ID to delete", min_value=1, step=1, key="delete_id")
        with dc2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Delete", type="secondary"):
                delete_response(int(delete_id))
                st.warning(f"Response #{delete_id} deleted.")
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="glass-card">
            <div class="live-indicator"><span class="live-dot"></span> Real-Time Monitoring Active</div>
            <div style="color:#64748B; margin-top:0.5rem; font-size:0.9rem;">
                Dashboard refreshes automatically. All voter data is stored securely in SQLite with
                sentiment analysis and NPS classification applied on submission.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
