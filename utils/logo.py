"""Shared logo rendering helpers."""

from __future__ import annotations

import base64
import mimetypes

import streamlit as st

from config import LOGO_PATH


def render_logo(width: int = 90, centered: bool = False) -> None:
    if not LOGO_PATH.exists():
        return

    suffix = LOGO_PATH.suffix.lower()
    align = "center" if centered else "left"

    if suffix == ".svg":
        b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode()
        st.markdown(
            f'<div style="text-align:{align};">'
            f'<img src="data:image/svg+xml;base64,{b64}" width="{width}" '
            f'style="border-radius:20px;box-shadow:0 8px 32px rgba(10,102,255,0.3);"/>'
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        mime = mimetypes.guess_type(str(LOGO_PATH))[0] or "image/png"
        b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode()
        st.markdown(
            f'<div style="text-align:{align};">'
            f'<img src="data:{mime};base64,{b64}" width="{width}" '
            f'style="border-radius:20px;box-shadow:0 8px 32px rgba(10,102,255,0.3);"/>'
            f"</div>",
            unsafe_allow_html=True,
        )
