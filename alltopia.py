import streamlit as st
from camera_input_live import camera_input_live
from PIL import Image
import io
from langchain.prompts import PromptTemplate
from groq import Groq

# Configuração da chave API (Token)
groq_api_key = st.secrets["GROQ_API_KEY"]  # Chave armazenada no secrets do Streamlit

# Configuração do modelo LLM
template = open("templates/vision_assistant.md", "r").read()
prompt = PromptTemplate(input_variables=["input", "video_description"],
                        template=template)

client = Groq(api_key=groq_api_key)

def run_groq_query(input_text, video_description):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt.format(input=input_text, video_description=video_description)}
    ]
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0
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
    img = Image.open(io.BytesIO(image.read()))
    # Exibe informações da imagem
    st.write(f"Formato: {img.format}")
    st.write(f"Dimensões: {img.size}")
    st.write(f"Modo: {img.mode}")
    
    # Botão para enviar a imagem para a API Groq
    if st.button("Enviar Imagem para Groq API"):
        # Exemplo de processamento da imagem e envio para o modelo LLM via API Groq
        video_description = "Descrição gerada pelo modelo"  # Placeholder para uma possível descrição gerada
        input_text = "Descreva a imagem capturada"
        
        # Executando a query Groq com a entrada e a descrição do vídeo
        response = run_groq_query(input_text, video_description)
        
        st.write("Resposta da API Groq:")
        st.write(response)
else:
    st.error("Nenhuma imagem capturada.")
