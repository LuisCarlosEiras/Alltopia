import streamlit as st
from camera_input_live import camera_input_live
from PIL import Image
import io
import base64
from groq import Groq

# Configuração da chave API (Token)
groq_api_key = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=groq_api_key)

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def run_groq_query(input_text, image_base64):
    messages = [
        {"role": "system", "content": "You are a helpful assistant capable of analyzing images."},
        {"role": "user", "content": [
            {"type": "text", "text": input_text},
            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_base64}"}
        ]}
    ]
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",  # Certifique-se de que a Groq suporta este modelo
        messages=messages,
        max_tokens=300
    )
    return response.choices[0].message.content

# Interface do Streamlit
st.title("Captura de Imagens com Streamlit e API Groq")

# Captura de imagem com streamlit-camera-input-live
image = camera_input_live()

# Verificação se a imagem foi capturada e exibição
if image:
    st.image(image)
    
    # Converte o arquivo BytesIO para uma imagem PIL
    img = Image.open(io.BytesIO(image.getvalue()))
    # Exibe informações da imagem
    st.write(f"Formato: {img.format}")
    st.write(f"Dimensões: {img.size}")
    st.write(f"Modo: {img.mode}")
    
    # Botão para enviar a imagem para a API Groq
    if st.button("Enviar Imagem para Groq API"):
        # Codifica a imagem em base64
        image_base64 = encode_image(image)
        
        input_text = "Descreva detalhadamente a imagem capturada."
        
        # Executando a query Groq com a entrada e a imagem
        response = run_groq_query(input_text, image_base64)
        
        st.write("Resposta da API Groq:")
        st.write(response)
else:
    st.error("Nenhuma imagem capturada.")
