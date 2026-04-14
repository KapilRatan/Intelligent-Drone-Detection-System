"""
Collapsible sidebar showing model configuration and quick stats.
"""

import streamlit as st

from config.settings import MODEL_PATH, IMG_SIZE, NPERSEG, GLOBAL_MEAN, GLOBAL_STD
from utils.history_manager import load_history, compute_stats


def render_sidebar() -> None:
    """Render the sidebar with model info and quick detection stats."""
    with st.sidebar:

        st.markdown("""
        <div style="
            font-family:'Share Tech Mono',monospace;
            font-size:10px;
            letter-spacing:2px;
            text-transform:uppercase;
            color:#5a8a7a;
            margin-bottom:16px;
            padding-bottom:10px;
            border-bottom:1px solid rgba(0,255,157,0.12);
        ">◈ System Info</div>
        """, unsafe_allow_html=True)

        config_rows = [
            ("Model file", MODEL_PATH),
            ("Input size", f"{IMG_SIZE} × {IMG_SIZE}"),
            ("NPERSEG", str(NPERSEG)),
            ("Global mean", str(GLOBAL_MEAN)),
            ("Global std", str(GLOBAL_STD)),
        ]
        for label, value in config_rows:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;
                        margin-bottom:8px;font-size:12px">
                <span style="color:#5a8a7a;font-family:'Share Tech Mono',monospace;
                             font-size:10px;letter-spacing:1px">{label}</span>
                <span style="color:#c8f0e8;font-family:'Share Tech Mono',monospace;
                             font-size:10px">{value}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='margin:16px 0 10px;border-top:1px solid rgba(0,255,157,0.12)'></div>",
                    unsafe_allow_html=True)

        history = load_history()
        stats = compute_stats(history)

        st.markdown("""
        <div style="
            font-family:'Share Tech Mono',monospace;
            font-size:10px;
            letter-spacing:2px;
            text-transform:uppercase;
            color:#5a8a7a;
            margin-bottom:12px;
        ">◈ Quick Stats</div>
        """, unsafe_allow_html=True)

        quick = [
            ("Total scans", str(stats["total"]), "#00ff9d"),
            ("Drones", str(stats["drones"]), "#ffb800"),
            ("Birds", str(stats["birds"]), "#00d4ff"),
            (
                "Avg conf",
                f"{stats['avg_conf']}%" if stats["avg_conf"] else "—",
                "#c8f0e8",
            ),
        ]
        for label, value, color in quick:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;
                        margin-bottom:10px;align-items:baseline">
                <span style="color:#5a8a7a;font-family:'Share Tech Mono',monospace;
                             font-size:10px;letter-spacing:1px">{label}</span>
                <span style="color:{color};font-family:'Share Tech Mono',monospace;
                             font-size:16px;font-weight:600">{value}</span>
            </div>""", unsafe_allow_html=True)
