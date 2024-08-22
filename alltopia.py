import streamlit as st
from camera_input_live import camera_input_live

# Interface do Streamlit
st.title("Captura de Imagens com Streamlit")

# Captura de imagem com streamlit-camera-input-live
image_data = camera_input_live()

# Verificação se a imagem foi capturada e exibição
if image_data:
    st.image(image_data, caption="Imagem Capturada", use_column_width=True)

    # Se a imagem for capturada, você pode prosseguir para enviar a imagem para a API Groq
    if st.button("Enviar Imagem para Groq API"):
        st.write("A implementação do envio da imagem para a API Groq seria adicionada aqui.")
else:
    st.error("Nenhuma imagem capturada.")
