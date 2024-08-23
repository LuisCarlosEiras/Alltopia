import streamlit as st
from camera_input_live import camera_input_live
from PIL import Image
import io
from groq import Groq

# Configuração da chave API (Token)
groq_api_key = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=groq_api_key)

def run_groq_query(input_text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": input_text}
    ]
    response = client.chat.completions.create(
        model="llama3-70b-8192",  # ou outro modelo suportado pela Groq
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
    
    # Botão para enviar a descrição para a API Groq
    if st.button("Enviar Descrição para Groq API"):
        # Aqui, em vez de enviar a imagem, vamos apenas descrever o que foi capturado
        input_text = """
        Uma imagem foi capturada usando a câmera. 
        Formato da imagem: {format}
        Dimensões: {width}x{height}
        Modo de cor: {mode}
        
        Por favor, forneça algumas sugestões sobre como poderíamos analisar ou utilizar esta imagem em uma aplicação.
        """.format(format=img.format, width=img.width, height=img.height, mode=img.mode)
        
        # Executando a query Groq com a entrada
        response = run_groq_query(input_text)
        
        st.write("Resposta da API Groq:")
        st.write(response)
else:
    st.error("Nenhuma imagem capturada.")
