import streamlit as st
from camera_input_live import camera_input_live
from PIL import Image
import io
import requests

# Inicializar o cliente Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

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
        # Prepare a requisição
        url = "https://api.groq.com/v1/your-endpoint"  # substitua com o endpoint correto
        headers = {
            "Authorization": f"Bearer {client.api_key}",
            "Content-Type": "application/octet-stream"
        }
        
        # Envia a imagem como bytes
        response = requests.post(url, headers=headers, data=io.BytesIO(image.read()))
        
        # Verifica a resposta da API
        if response.status_code == 200:
            st.success("Imagem enviada com sucesso para a API Groq!")
            st.json(response.json())  # Exibe a resposta da API
        else:
            st.error(f"Falha ao enviar a imagem. Status code: {response.status_code}")
            st.write(response.text)
else:
    st.error("Nenhuma imagem capturada.")
import streamlit as st
from camera_input_live import camera_input_live
from PIL import Image
import io
import requests

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
        token = st.secrets["groq_api"]["token"]
        
        # Prepare a requisição
        url = "https://api.groq.com/v1/images/describe"  # substitua com o endpoint correto
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/octet-stream"
        }
        
        # Envia a imagem como bytes
        response = requests.post(url, headers=headers, data=io.BytesIO(image.read()))
        
        # Verifica a resposta da API
        if response.status_code == 200:
            st.success("Imagem enviada com sucesso para a API Groq!")
            st.json(response.json())  # Exibe a resposta da API
        else:
            st.error(f"Falha ao enviar a imagem. Status code: {response.status_code}")
            st.write(response.text)
else:
    st.error("Nenhuma imagem capturada.")
