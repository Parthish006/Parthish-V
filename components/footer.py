"""Footer component."""

import streamlit as st


def render_footer() -> None:
    st.markdown(
        """
        <div class="footer">
            <div>CAPAI © 2026 | Empowering Better Elections Through Data & AI</div>
            <div class="footer-badges">
                <span class="footer-badge">🔒 Data Security Certified</span>
                <span class="footer-badge">♿ WCAG Accessibility Compliant</span>
                <span class="footer-badge">📋 Privacy Notice</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
