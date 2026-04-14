"""
Top navigation bar and horizontal page switcher.
Persists selection in st.session_state["active_page"].
"""

import streamlit as st

_NAV_HTML = """
<div style="
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 24px;
    background: rgba(8,20,34,0.95);
    border-bottom: 1px solid rgba(0,255,157,0.15);
    margin-bottom: 24px;
    border-radius: 0 0 12px 12px;
">
    <div style="
        font-family: 'Share Tech Mono', monospace;
        font-size: 14px;
        color: #00ff9d;
        letter-spacing: 3px;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 10px;
    ">
        <span style="
            width: 8px; height: 8px;
            background: #00ff9d;
            border-radius: 50%;
            box-shadow: 0 0 8px #00ff9d;
            display: inline-block;
            animation: none;
        "></span>
        MicroDoppler
    </div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:11px;color:#5a8a7a;letter-spacing:1px">
        System <span style="color:#00ff9d">ONLINE</span>
        &nbsp;|&nbsp;
        Model <span style="color:#00ff9d">CNN v2.1</span>
    </div>
</div>
"""


def render_navbar() -> None:
    """Render the top bar and bind page selection to session state."""
    st.markdown(_NAV_HTML, unsafe_allow_html=True)
    st.radio(
        "Navigation",
        ["Radar", "Dashboard"],
        horizontal=True,
        label_visibility="collapsed",
        key="active_page",
    )
