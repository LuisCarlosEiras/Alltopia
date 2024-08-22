import streamlit as st
import cv2
import requests
import numpy as np

# Configuração da chave da API do Groq
groq_api_key = st.secrets["groq"]["api_key"]

# Função para capturar imagem da câmera
def capture_image():
    # Inicializa a captura de vídeo
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Não foi possível acessar a câmera.")
        return None

    # Captura um frame
    ret, frame = cap.read()

    # Libera a captura de vídeo
    cap.release()

    if not ret:
        st.error("Não foi possível capturar a imagem.")
        return None

    return frame

# Função para exibir a imagem no Streamlit
def display_image(image):
    st.image(image, channels="BGR")

# Função para enviar a imagem ao Groq API
def send_image_to_groq(image):
    st.write("Enviando imagem para Groq API...")

    # Converte a imagem para bytes
    _, img_encoded = cv2.imencode('.jpg', image)
    files = {'file': img_encoded.tobytes()}

    # Realiza a chamada à API do Groq
    response = requests.post(
        url="https://api.groq.com/v1/your-endpoint",  # Substitua pelo endpoint correto da API
        headers={"Authorization": f"Bearer {groq_api_key}"},
        files=files
    )

    # Verifica se a chamada foi bem-sucedida
    if response.status_code == 200:
        st.write("Imagem enviada com sucesso!")
        st.json(response.json())  # Exibe a resposta da API
    else:
        st.error(f"Erro ao enviar imagem: {response.status_code}")
        st.error(response.text)

# Interface do Streamlit
st.title("Captura de Imagens com Streamlit e OpenCV")

if st.button("Capturar Imagem"):
    image = capture_image()
    if image is not None:
        st.write("Imagem capturada:")
        display_image(image)

        if st.button("Enviar Imagem para Groq API"):
            send_image_to_groq(image)
