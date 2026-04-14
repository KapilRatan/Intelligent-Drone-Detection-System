import streamlit as st
from config.settings import PAGE_CONFIG
from components.navbar import render_navbar
from components.sidebar import render_sidebar
from pages.radar import render_radar_page
from pages.dashboard import render_dashboard_page
from utils.style_loader import load_styles

# ── Page config (must be first Streamlit call) ──────────────────
st.set_page_config(**PAGE_CONFIG)

# ── Inject global CSS ───────────────────────────────────────────
load_styles()

# ── Top navigation bar ──────────────────────────────────────────
render_navbar()

# ── Sidebar ─────────────────────────────────────────────────────
render_sidebar()

# ── Page routing (navbar binds st.session_state["active_page"]) ──
page = st.session_state.get("active_page", "Radar")

if page == "Radar":
    render_radar_page()
elif page == "Dashboard":
    render_dashboard_page()