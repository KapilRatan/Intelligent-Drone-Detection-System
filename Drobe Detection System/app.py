import streamlit as st
import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.signal import stft
import tensorflow as tf

# ======================
# CONFIG
# ======================
IMG_SIZE = 128
NPERSEG = 64

MODEL_PATH = "drone_vs_bird_final.h5"

# Load model
model = tf.keras.models.load_model(MODEL_PATH)

# ⚠️ IMPORTANT: paste your saved values here
GLOBAL_MEAN = 0.0423   # <-- replace with your printed value
GLOBAL_STD  = 0.0946   # <-- replace with your printed value

# ======================
# STFT FUNCTION
# ======================
def create_stft_image(signal):
    signal = np.array(signal, dtype=np.float32).flatten()
    _, _, Zxx = stft(signal, nperseg=NPERSEG)
    Zxx = np.abs(Zxx)
    Zxx = np.log1p(Zxx)

    img = cv2.resize(Zxx, (IMG_SIZE, IMG_SIZE))
    img = np.stack([img]*3, axis=-1)

    return img

# ======================
# NORMALIZATION
# ======================
def normalize(img):
    return (img - GLOBAL_MEAN) / GLOBAL_STD

# ======================
# PREDICTION
# ======================
def predict(img):
    img = normalize(img)
    img = np.expand_dims(img, axis=0)

    prob = model.predict(img)[0][0]

    label = "🛸 Drone" if prob >= 0.5 else "🐦 Bird"
    confidence = prob if prob >= 0.5 else 1 - prob

    return label, float(confidence), float(prob)


# ======================
# UI
# ======================
st.set_page_config(page_title="Drone vs Bird Detection", layout="wide")

st.title("🚁 Drone vs Bird Detection using Micro-Doppler")
st.markdown("Upload `.npy` signal or spectrogram image")

col1, col2 = st.columns(2)

uploaded_file = st.file_uploader("Upload File", type=["npy", "png", "jpg", "jpeg"])

if uploaded_file:
    if uploaded_file.name.endswith(".npy"):
        signal = np.load(uploaded_file)

        if signal.ndim > 1:
            signal = signal[:, 0]

        stft_img = create_stft_image(signal)

    else:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        stft_img = cv2.imdecode(file_bytes, 1)
        stft_img = cv2.resize(stft_img, (IMG_SIZE, IMG_SIZE))

    # Prediction
    label, confidence, raw_prob = predict(stft_img)

    # ======================
    # DISPLAY
    # ======================
    with col1:
        st.subheader("📊 STFT Spectrogram")
        fig, ax = plt.subplots()
        ax.imshow(stft_img[:,:,0], cmap="inferno", aspect='auto')
        ax.axis("off")
        st.pyplot(fig)

    with col2:
        st.subheader("🧠 Prediction")
        st.success(f"Prediction: {label}")
        st.info(f"Confidence: {confidence*100:.2f}%")

        st.subheader("📈 Model Metrics (from training)")
        st.write("Accuracy: ~Your trained accuracy here")
        st.write("AUC: ~Your trained AUC here")