"""
CAPAI – Smart Voter Experience & Election Infrastructure Improvement Platform
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from components.footer import render_footer
from components.sidebar import render_sidebar
from config import FAVICON_PATH
from database.db import init_db, seed_sample_data
from pages import admin, ai_insights_page, analytics_page, infrastructure, landing, survey
from styles.css import get_css
from utils.logo import render_logo

PAGES = {
    "Home": landing.render,
    "Voter Survey": survey.render,
    "Analytics": analytics_page.render,
    "AI Insights": ai_insights_page.render,
    "Infrastructure Recommendations": infrastructure.render,
    "Admin Panel": admin.render,
}


def _ensure_favicon() -> None:
    if FAVICON_PATH.exists():
        return
    try:
        from PIL import Image, ImageDraw

        FAVICON_PATH.parent.mkdir(parents=True, exist_ok=True)
        img = Image.new("RGB", (64, 64), "#0A66FF")
        draw = ImageDraw.Draw(img)
        draw.ellipse([12, 12, 52, 52], fill="#FFFFFF")
        draw.rectangle([26, 22, 38, 36], fill="#0A66FF")
        img.save(FAVICON_PATH)
    except Exception:
        pass


def _ensure_textblob_corpora() -> None:
    try:
        import nltk

        nltk.data.find("tokenizers/punkt")
    except LookupError:
        try:
            import nltk

            nltk.download("punkt", quiet=True)
            nltk.download("punkt_tab", quiet=True)
        except Exception:
            pass


def main() -> None:
    _ensure_favicon()
    _ensure_textblob_corpora()
    init_db()
    seed_sample_data()

    if "theme" not in st.session_state:
        st.session_state.theme = "light"

    page_icon = str(FAVICON_PATH) if FAVICON_PATH.exists() else "🗳️"

    st.set_page_config(
        page_title="CAPAI | Voter Experience Platform",
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(get_css(st.session_state.get("theme", "light")), unsafe_allow_html=True)

    current_page = render_sidebar()

    if current_page != "Home":
        hc1, hc2 = st.columns([1, 5])
        with hc1:
            render_logo(width=48)
        with hc2:
            st.markdown(f"### {current_page}", unsafe_allow_html=True)

    page_fn = PAGES.get(current_page, landing.render)
    page_fn()

    render_footer()


if __name__ == "__main__":
    main()
