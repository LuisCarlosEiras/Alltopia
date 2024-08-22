import streamlit as st
import cv2

def capture_image():
    cap = cv2.VideoCapture(0)  # Experimente alterar o índice para 1, 2, etc.

    if not cap.isOpened():
        st.error("Não foi possível acessar a câmera.")
        return None

    ret, frame = cap.read()

    cap.release()

    if not ret:
        st.error("Não foi possível capturar a imagem.")
        return None

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame_rgb

st.title("Captura de Imagens com Streamlit e OpenCV")

if st.button("Capturar Imagem"):
    image = capture_image()
    if image is not None:
        st.image(image, caption="Imagem Capturada", use_column_width=True)
    else:
        st.error("Imagem não foi capturada. Verifique a câmera e tente novamente.")
