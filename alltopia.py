import streamlit as st
from camera_input_live import camera_input_live

# Função para exibir e processar a imagem capturada
def process_and_display_image(image_data):
    if image_data:
        # Converte a imagem capturada para um formato compatível
        img = image_data.to_image()
        st.image(img, caption="Imagem Capturada", use_column_width=True)
        return img
    else:
        st.error("Nenhuma imagem capturada.")
        return None

# Interface do Streamlit
st.title("Captura de Imagens com Streamlit")

# Captura de imagem com streamlit-camera-input-live
image_data = camera_input_live(label="Tire uma foto com a câmera")

# Processamento da imagem capturada
captured_image = process_and_display_image(image_data)

# Se a imagem for capturada, você pode prosseguir para enviar a imagem para a API Groq
if captured_image:
    if st.button("Enviar Imagem para Groq API"):
        st.write("A implementação do envio da imagem para a API Groq seria adicionada aqui.")
