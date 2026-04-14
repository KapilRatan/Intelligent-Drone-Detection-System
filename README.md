# Intelligent-Drone-Detection-System
An Intelligent Drone Detection System is a sophisticated security solution designed to identify, track, and classify unmanned aerial vehicles (UAVs) in real-time. By leveraging advanced deep learning CNN customized model to analyze Micro-Doppler signatures, ensuring high accuracy even in cluttered environments or bad weather.

### Intelligent Drone Detection System Using Micro-Doppler Signatures
An AI-powered security solution developed for the FANTOMCODE 2026 National Level Hackathon. This system accurately differentiates between drones and birds in radar systems by analyzing Micro-Doppler signatures.

## 📌 Project Overview
Modern radar systems often struggle to distinguish small unmanned aerial vehicles (UAVs) from biological entities like birds due to similar radar cross-sections. Our system solves this by:
Capturing FMCW radar signals.
Extracting motion-based Micro-Doppler patterns.
Converting signals into Time-Frequency Spectrograms.
Utilizing a CNN Deep Learning model for intelligent classification.

## 🏗️ System Architecture
The pipeline follows a modular flow from raw signal capture to a localized user dashboard:
Signal Capture: Receiving raw FMCW radar data.
Feature Processing: Short-Time Fourier Transform (STFT) analysis to generate spectrograms.
Classification: A CNN model featuring Convolution Blocks, Batch Normalization, and Dropout layers for robust detection.
Deployment: A high-performance Streamlit web interface for real-time monitoring and analytics.

## 📊 Performance Metrics
The model was trained on the KTH Drone Dataset (75,868 samples) using under-sampling techniques to ensure class balance.
Accuracy: 98.03% 
AUC: 0.9970 
Precision: 98.28% 
Recall: 97.78% 


├── assets/             # Images, logos, and static files

├── components/         # Reusable UI components (Navbar, Sidebar)
├── config/             # Configuration settings (PAGE_CONFIG)
├── pages/              # Streamlit page modules (Radar, Dashboard)
├── utils/              # Helper functions and style loaders
├── app.py              # Main entry point for the Streamlit application
├── requirements.txt    # Project dependencies
└── drone_vs_bird_final.h5 # Pre-trained CNN model
