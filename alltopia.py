import streamlit as st
from camera_input_live import camera_input_live
from PIL import Image
import io

st.title("Captura de Imagens com Streamlit")

# Captura de imagem com streamlit-camera-input-live
image = camera_input_live()

# Verificação se a imagem foi capturada e exibição
if image:
    st.image(image)
    
    # Converte o arquivo BytesIO para uma imagem PIL
    img = Image.open(io.BytesIO(image.read()))

    # Exibe informações da imagem
    st.write(f"Formato: {img.format}")
    st.write(f"Dimensões: {img.size}")
    st.write(f"Modo: {img.mode}")
    
    # Botão para enviar a imagem para a API Groq
    if st.button("Enviar Imagem para Groq API"):
        st.write("Implementação do envio da imagem para a API Groq será adicionada aqui.")
