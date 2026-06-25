"""CAPAI glassmorphism CSS with dark/light mode support."""

from config import COLORS


def get_css(theme: str = "light") -> str:
    is_dark = theme == "dark"

    bg = "#0B1220" if is_dark else COLORS["background"]
    card_bg = "rgba(15, 23, 42, 0.72)" if is_dark else "rgba(255, 255, 255, 0.72)"
    card_border = "rgba(0, 180, 255, 0.25)" if is_dark else "rgba(10, 102, 255, 0.18)"
    text = "#E2E8F0" if is_dark else COLORS["text"]
    muted = "#94A3B8" if is_dark else "#64748B"
    sidebar_bg = "linear-gradient(180deg, #0A1628 0%, #0F2744 50%, #0A1E3A 100%)"
    hero_bg = (
        "linear-gradient(135deg, rgba(10,102,255,0.35) 0%, rgba(79,70,229,0.25) 50%, rgba(0,180,255,0.2) 100%)"
        if is_dark
        else "linear-gradient(135deg, rgba(10,102,255,0.12) 0%, rgba(79,70,229,0.08) 50%, rgba(0,180,255,0.1) 100%)"
    )

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }}

    .stApp {{
        background: {bg};
        color: {text};
        background-image: radial-gradient(circle at 10% 20%, rgba(10,102,255,0.08) 0%, transparent 40%),
                          radial-gradient(circle at 90% 80%, rgba(0,180,255,0.08) 0%, transparent 40%);
    }}

    [data-testid="stSidebar"] {{
        background: {sidebar_bg} !important;
        border-right: 1px solid rgba(0, 180, 255, 0.2);
    }}

    [data-testid="stSidebar"] * {{
        color: #E2E8F0 !important;
    }}

    .sidebar-logo {{
        text-align: center;
        padding: 1rem 0 0.5rem;
        animation: fadeInDown 0.8s ease;
    }}

    .sidebar-logo img {{
        width: 90px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(10, 102, 255, 0.4);
        transition: transform 0.3s ease;
    }}

    .sidebar-logo img:hover {{
        transform: scale(1.05);
    }}

    .sidebar-brand {{
        font-size: 1.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00B4FF, #FFFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 0.5rem;
        letter-spacing: 1px;
    }}

    .sidebar-tagline {{
        font-size: 0.75rem;
        color: #94A3B8 !important;
        margin-top: 0.25rem;
    }}

    .nav-item {{
        padding: 0.65rem 1rem;
        margin: 0.25rem 0;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        border: 1px solid transparent;
    }}

    .nav-item:hover {{
        background: rgba(10, 102, 255, 0.25);
        border-color: rgba(0, 180, 255, 0.3);
        transform: translateX(4px);
    }}

    .nav-item.active {{
        background: linear-gradient(90deg, rgba(10,102,255,0.4), rgba(0,180,255,0.2));
        border-color: rgba(0, 180, 255, 0.5);
        box-shadow: 0 4px 15px rgba(10, 102, 255, 0.3);
    }}

    .glass-card {{
        background: {card_bg};
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid {card_border};
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px rgba(10, 102, 255, 0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeInUp 0.6s ease;
    }}

    .glass-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(10, 102, 255, 0.15);
    }}

    .kpi-card {{
        background: {card_bg};
        backdrop-filter: blur(12px);
        border: 1px solid {card_border};
        border-radius: 16px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease;
        box-shadow: 0 4px 20px rgba(10, 102, 255, 0.1);
    }}

    .kpi-card:hover {{
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 8px 30px rgba(10, 102, 255, 0.2);
        border-color: {COLORS["primary"]};
    }}

    .kpi-icon {{
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }}

    .kpi-value {{
        font-size: 2rem;
        font-weight: 800;
        color: {COLORS["primary"]};
        line-height: 1.2;
    }}

    .kpi-label {{
        font-size: 0.85rem;
        color: {muted};
        margin-top: 0.25rem;
        font-weight: 500;
    }}

    .hero-section {{
        background: {hero_bg};
        border: 1px solid {card_border};
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        animation: fadeInUp 0.8s ease;
    }}

    .hero-title {{
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, {COLORS["primary"]}, {COLORS["secondary"]});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }}

    .hero-tagline {{
        font-size: 1.3rem;
        color: {muted};
        margin-bottom: 1.5rem;
        font-weight: 500;
    }}

    .stat-counter {{
        font-size: 2.5rem;
        font-weight: 800;
        color: {COLORS["primary"]};
    }}

    .stat-label {{
        font-size: 0.9rem;
        color: {muted};
        font-weight: 500;
    }}

    .feature-card {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
        transition: all 0.3s ease;
    }}

    .feature-card:hover {{
        border-color: {COLORS["primary"]};
        transform: translateY(-3px);
    }}

    .feature-icon {{
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }}

    .feature-title {{
        font-size: 1.1rem;
        font-weight: 700;
        color: {text};
        margin-bottom: 0.5rem;
    }}

    .feature-desc {{
        font-size: 0.9rem;
        color: {muted};
        line-height: 1.5;
    }}

    .cta-button {{
        display: inline-block;
        background: linear-gradient(90deg, {COLORS["primary"]}, {COLORS["secondary"]});
        color: white !important;
        padding: 0.85rem 2.5rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.1rem;
        text-decoration: none;
        box-shadow: 0 8px 25px rgba(10, 102, 255, 0.35);
        transition: all 0.3s ease;
        border: none;
    }}

    .cta-button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(10, 102, 255, 0.45);
    }}

    .insight-card {{
        background: linear-gradient(135deg, rgba(10,102,255,0.08), rgba(79,70,229,0.05));
        border-left: 4px solid {COLORS["primary"]};
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        animation: slideInLeft 0.5s ease;
    }}

    .priority-high {{ border-left-color: #EF4444; }}
    .priority-medium {{ border-left-color: #F59E0B; }}
    .priority-low {{ border-left-color: #10B981; }}

    .rec-card {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }}

    .rec-card:hover {{
        border-color: {COLORS["primary"]};
        box-shadow: 0 6px 24px rgba(10, 102, 255, 0.12);
    }}

    .badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .badge-high {{ background: rgba(239,68,68,0.15); color: #EF4444; }}
    .badge-medium {{ background: rgba(245,158,11,0.15); color: #F59E0B; }}
    .badge-low {{ background: rgba(16,185,129,0.15); color: #10B981; }}

    .footer {{
        text-align: center;
        padding: 2rem 1rem 1rem;
        margin-top: 3rem;
        border-top: 1px solid {card_border};
        color: {muted};
        font-size: 0.85rem;
    }}

    .footer-badges {{
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin-top: 0.75rem;
        flex-wrap: wrap;
    }}

    .footer-badge {{
        background: rgba(10, 102, 255, 0.08);
        border: 1px solid {card_border};
        border-radius: 20px;
        padding: 0.35rem 1rem;
        font-size: 0.75rem;
        font-weight: 600;
        color: {COLORS["primary"]};
    }}

    .section-title {{
        font-size: 1.6rem;
        font-weight: 800;
        color: {text};
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(10, 102, 255, 0.2);
    }}

    .nps-badge-promoter {{ color: #10B981; font-weight: 700; }}
    .nps-badge-passive {{ color: #F59E0B; font-weight: 700; }}
    .nps-badge-detractor {{ color: #EF4444; font-weight: 700; }}

    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes fadeInDown {{
        from {{ opacity: 0; transform: translateY(-20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes slideInLeft {{
        from {{ opacity: 0; transform: translateX(-20px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}

    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
    }}

    .live-indicator {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.85rem;
        color: #10B981;
        font-weight: 600;
    }}

    .live-dot {{
        width: 8px;
        height: 8px;
        background: #10B981;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }}

    div[data-testid="stMetric"] {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 12px;
        padding: 0.75rem;
    }}

    .stButton > button {{
        background: linear-gradient(90deg, {COLORS["primary"]}, {COLORS["secondary"]}) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }}

    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(10, 102, 255, 0.35) !important;
    }}

    .survey-section {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }}
    </style>
    """
