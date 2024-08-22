import streamlit as st
import cv2
import numpy as np

def capture_image():
    # Inicializa a captura de vídeo
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Não foi possível acessar a câmera.")
        return None

    # Captura um frame
    ret, frame = cap.read()
    cap.release()

    if not ret:
        st.error("Não foi possível capturar a imagem.")
        return None

    # Converte a imagem BGR para RGB, pois Streamlit exibe imagens em RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    return frame_rgb

# Interface do Streamlit
st.title("Captura de Imagens com Streamlit e OpenCV")

if st.button("Capturar Imagem"):
    image = capture_image()
    if image is not None:
        st.image(image, caption="Imagem Capturada", use_column_width=True)
