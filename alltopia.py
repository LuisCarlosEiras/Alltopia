import streamlit as st
from camera_input_live import camera_input_live
from PIL import Image
import io

# Interface do Streamlit
st.title("Captura de Imagens com Streamlit")

# Captura de imagem com streamlit-camera-input-live
image_data = camera_input_live()

# Verificação se a imagem foi capturada e exibição
if image_data is not None:
    # Converte o objeto BytesIO em uma imagem PIL
    image = Image.open(io.BytesIO(image_data.read()))
    
    # Exibe a imagem capturada
    st.image(image, caption="Imagem Capturada", use_column_width=True)
    
    # Exibe informações adicionais da imagem (opcional)
    st.write(f"Tipo da imagem capturada: {type(image)}")
    st.write(f"Dimensões da imagem: {image.size}")  # Agora acessamos as dimensões da imagem PIL
    
    # Se a imagem for capturada, você pode prosseguir para enviar a imagem para a API Groq
    if st.button("Enviar Imagem para Groq API"):
        st.write("A implementação do envio da imagem para a API Groq seria adicionada aqui.")
else:
    st.error("Nenhuma imagem capturada.")
