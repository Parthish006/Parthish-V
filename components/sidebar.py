"""Sidebar navigation component."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from config import LOGO_PATH
from utils.logo import render_logo

NAV_ITEMS = [
    ("🏠 Home", "Home"),
    ("🗳️ Voter Survey", "Voter Survey"),
    ("📊 Analytics", "Analytics"),
    ("🤖 AI Insights", "AI Insights"),
    ("🏛️ Infrastructure Recommendations", "Infrastructure Recommendations"),
    ("⚙️ Admin Panel", "Admin Panel"),
]


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
        render_logo(width=90, centered=True)
        st.markdown(
            """
            <div class="sidebar-brand">CAPAI</div>
            <div class="sidebar-tagline">Smart Voter Experience Platform</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        if "page" not in st.session_state:
            st.session_state.page = "Home"

        for label, page_name in NAV_ITEMS:
            active = st.session_state.page == page_name
            css_class = "nav-item active" if active else "nav-item"
            if st.button(label, key=f"nav_{page_name}", use_container_width=True):
                st.session_state.page = page_name
                st.rerun()

        st.markdown("---")

        theme = st.toggle("🌙 Dark Mode", value=st.session_state.get("theme") == "dark")
        st.session_state.theme = "dark" if theme else "light"

        st.markdown(
            """
            <div style="margin-top: 2rem; padding: 1rem; text-align: center;">
                <div style="font-size: 0.7rem; color: #64748B;">
                    🔒 Secure • ♿ Accessible<br/>
                    Government-Grade Platform
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return st.session_state.page
