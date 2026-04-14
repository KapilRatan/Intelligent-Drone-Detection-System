"""
Animated circular scan radar (SVG + CSS). Used on the Radar page.
"""

import streamlit as st


def _gradient_ids() -> tuple[str, str]:
    uid = st.session_state.setdefault("_radar_svg_uid", "r1")
    return f"radarSweepGrad_{uid}", uid


def open_radar_panel() -> None:
    """Open the scan radar card (call before SVG + actions)."""
    st.markdown(
        '<div class="radar-scan-panel">'
        '<div class="radar-scan-panel-header">Scan Radar</div>',
        unsafe_allow_html=True,
    )


def render_radar_svg() -> None:
    """Draw the rotating sweep and static grid."""
    grad_id, _ = _gradient_ids()
    html = f"""
    <div class="radar-svg-wrap">
        <svg class="radar-scope" viewBox="-210 -210 420 420" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="{grad_id}" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
                    <stop offset="0%" stop-color="#00ffcc" stop-opacity="0.55"/>
                    <stop offset="55%" stop-color="#00ffcc" stop-opacity="0.12"/>
                    <stop offset="100%" stop-color="#00ffcc" stop-opacity="0"/>
                </linearGradient>
            </defs>
            <g class="radar-sweep-arm">
                <path class="radar-sweep-wedge" fill="url(#{grad_id})"
                      d="M 0 0 L 182 0 A 182 182 0 0 1 139.5 116.5 Z"/>
                <line class="radar-sweep-line" x1="0" y1="0" x2="182" y2="0"
                      stroke="#00ffcc" stroke-width="2.5" stroke-linecap="round"/>
            </g>
            <g class="radar-static">
                <circle cx="0" cy="0" r="48" fill="none" stroke="rgba(0,255,204,0.14)" stroke-width="1"/>
                <circle cx="0" cy="0" r="96" fill="none" stroke="rgba(0,255,204,0.14)" stroke-width="1"/>
                <circle cx="0" cy="0" r="144" fill="none" stroke="rgba(0,255,204,0.14)" stroke-width="1"/>
                <circle cx="0" cy="0" r="188" fill="none" stroke="rgba(0,255,204,0.18)" stroke-width="1"/>
                <line x1="0" y1="-190" x2="0" y2="190" stroke="rgba(0,255,204,0.2)" stroke-width="1"/>
                <line x1="-190" y1="0" x2="190" y2="0" stroke="rgba(0,255,204,0.2)" stroke-width="1"/>
                <text x="0" y="-198" text-anchor="middle" class="radar-compass">N</text>
                <text x="202" y="5" text-anchor="middle" class="radar-compass">E</text>
                <text x="0" y="212" text-anchor="middle" class="radar-compass">S</text>
                <text x="-202" y="5" text-anchor="middle" class="radar-compass">W</text>
            </g>
            <circle cx="0" cy="0" r="4" fill="#00ffcc" class="radar-center-dot"/>
        </svg>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def close_radar_panel() -> None:
    """Close the scan radar card."""
    st.markdown("</div>", unsafe_allow_html=True)


def render_radar_scan_display() -> None:
    """Full panel with SVG only (no Streamlit widgets inside)."""
    open_radar_panel()
    render_radar_svg()
    close_radar_panel()
