"""Streamlit page config, model paths, and theme colours."""

from pathlib import Path

# Repo root (parent of the `frontend` package)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

PAGE_CONFIG = {
    "page_title": "MicroDoppler | Drone vs Bird",
    "page_icon": "🛸",
    "layout": "wide",
    "initial_sidebar_state": "collapsed",
}

MODEL_PATH = str(_PROJECT_ROOT / "drone_vs_bird_final.h5")
IMG_SIZE = 128
NPERSEG = 64
GLOBAL_MEAN = 0.0423
GLOBAL_STD = 0.0946

HISTORY_FILE = str(_PROJECT_ROOT / "detection_history.json")
MAX_HISTORY = 100

COLOR_GREEN = "#00ff9d"
COLOR_AMBER = "#ffb800"
COLOR_CYAN = "#00d4ff"
COLOR_BG = "#050d15"
COLOR_BG2 = "#081422"
COLOR_BG3 = "#0d1f33"
COLOR_TEXT = "#c8f0e8"
COLOR_DIM = "#5a8a7a"
