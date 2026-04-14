"""
Radar page: signal upload → STFT spectrogram → CNN prediction.
"""

import time

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

from utils.signal_processor import create_stft_image, load_image_file
from utils.model_handler import load_model, run_prediction
from utils.history_manager import append_entry
from utils.plot_helpers import plot_spectrogram
from components.cards import result_card, empty_state
from components.radar_scan import close_radar_panel, open_radar_panel, render_radar_svg


def _render_header() -> None:
    st.markdown("""
    <div class="section-eyebrow">// Radar Detection System</div>
    <div class="section-title">Signal Analysis &amp; Classification</div>
    """, unsafe_allow_html=True)


def _render_upload_panel():
    st.markdown('<div class="panel"><div class="panel-header">Signal Input</div>',
                unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Signal file",
        type=["npy", "png", "jpg", "jpeg"],
        help="Same inputs as before: .npy time-series signal or spectrogram image (PNG, JPG, JPEG).",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    return uploaded


def _render_spectrogram_panel(uploaded, stft_img: np.ndarray | None) -> None:
    st.markdown('<div class="panel"><div class="panel-header">STFT Spectrogram</div>',
                unsafe_allow_html=True)

    if stft_img is None:
        st.markdown(empty_state("Awaiting signal input"), unsafe_allow_html=True)
    else:
        fig = plot_spectrogram(stft_img[:, :, 0])
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    st.markdown("</div>", unsafe_allow_html=True)


def _render_radar_side(stft_img: np.ndarray | None, filename: str) -> None:
    open_radar_panel()
    render_radar_svg()

    st.markdown('<div class="radar-actions-wrap">', unsafe_allow_html=True)

    if stft_img is None:
        st.markdown(
            '<p class="radar-hint">Upload a <strong>signal file</strong> on the left, '
            "then run <strong>Analyze</strong> to classify.</p>",
            unsafe_allow_html=True,
        )
    else:
        model = load_model()
        if model is None:
            st.error("Model file not found. Place `drone_vs_bird_final.h5` in the project root.")
        else:
            if st.button("⬡  Analyze Signal", use_container_width=True):
                _run_and_display(model, stft_img, filename)
            elif "last_result" in st.session_state:
                st.markdown(
                    result_card(**st.session_state["last_result"]),
                    unsafe_allow_html=True,
                )

    st.markdown("</div>", unsafe_allow_html=True)
    close_radar_panel()


def _run_and_display(model, stft_img: np.ndarray, filename: str) -> None:
    prog = st.progress(0, text="Preprocessing signal...")

    for i in range(1, 85, 12):
        prog.progress(i, text=f"Running CNN... {i}%")
        time.sleep(0.05)

    label, cls, conf, raw_prob = run_prediction(model, stft_img)
    prog.progress(100, text="Done")
    prog.empty()

    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")

    append_entry({
        "file": filename,
        "label": label,
        "cls": cls,
        "conf": round(conf * 100, 1),
        "prob": round(raw_prob, 4),
        "time": time_str,
        "date": now.strftime("%Y-%m-%d"),
        "hour": now.hour,
    })

    st.session_state["last_result"] = {
        "label": label,
        "cls": cls,
        "conf": conf,
        "raw_prob": raw_prob,
        "time_str": time_str,
    }

    st.markdown(
        result_card(label, cls, conf, raw_prob, time_str),
        unsafe_allow_html=True,
    )


def render_radar_page() -> None:
    _render_header()

    col_left, col_right = st.columns([1, 1], gap="medium")

    stft_img = None
    filename = ""

    with col_left:
        uploaded = _render_upload_panel()

        if uploaded is not None:
            filename = uploaded.name
            with st.spinner("Generating spectrogram..."):
                if uploaded.name.endswith(".npy"):
                    raw = np.load(uploaded)
                    if raw.ndim > 1:
                        raw = raw[:, 0]
                    stft_img = create_stft_image(raw)
                else:
                    stft_img = load_image_file(uploaded.read())

        _render_spectrogram_panel(uploaded, stft_img)

    with col_right:
        _render_radar_side(stft_img, filename)
