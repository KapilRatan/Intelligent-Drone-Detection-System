"""
Dashboard page: detection history log and distribution chart.
"""

import streamlit as st
import matplotlib.pyplot as plt

from utils.history_manager import load_history, clear_history, compute_stats
from utils.plot_helpers import plot_donut
from components.cards import stat_card, history_table, empty_state


def _render_header() -> None:
    st.markdown("""
    <div class="section-eyebrow">// Detection Dashboard</div>
    <div class="section-title">Detection History &amp; Analytics</div>
    """, unsafe_allow_html=True)


def _render_stats_row(stats: dict) -> None:
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            stat_card("Total Scans", str(stats["total"]), "green", "all detections"),
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            stat_card("Drones", str(stats["drones"]), "amber", "UAS detected"),
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            stat_card("Birds", str(stats["birds"]), "cyan-c", "avian detected"),
            unsafe_allow_html=True,
        )
    with c4:
        avg = f"{stats['avg_conf']}%" if stats["avg_conf"] is not None else "—"
        st.markdown(
            stat_card("Avg Confidence", avg, "plain", "model certainty"),
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-bottom:4px'></div>", unsafe_allow_html=True)


def _render_history_panel(history: list, stats: dict) -> None:
    st.markdown(
        '<div class="panel"><div class="panel-header">Detection Log</div>',
        unsafe_allow_html=True,
    )
    st.markdown(history_table(history), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if stats["total"] > 0:
        if st.button("🗑  Clear History", type="secondary"):
            clear_history()
            st.session_state.pop("last_result", None)
            st.rerun()


def _render_distribution_panel(stats: dict) -> None:
    st.markdown(
        '<div class="panel"><div class="panel-header">Distribution</div>',
        unsafe_allow_html=True,
    )

    if stats["total"] == 0:
        st.markdown(
            empty_state("No data yet"),
            unsafe_allow_html=True,
        )
    else:
        fig = plot_donut(stats["drones"], stats["birds"])
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    st.markdown("</div>", unsafe_allow_html=True)


def render_dashboard_page() -> None:
    _render_header()

    history = load_history()
    stats = compute_stats(history)

    _render_stats_row(stats)

    col_table, col_charts = st.columns([3, 2], gap="medium")

    with col_table:
        _render_history_panel(history, stats)

    with col_charts:
        _render_distribution_panel(stats)
