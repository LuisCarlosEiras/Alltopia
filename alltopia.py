import streamlit as st
from camera_input_live import camera_input_live
from PIL import Image
import io
import base64
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import os
import time
import random

# Configuração da página Streamlit
st.set_page_config(page_title="Assistente de Visão", layout="wide")

# Configuração da chave API do Groq
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# Função para redimensionar a imagem
def resize_image(image, max_size=(512, 512)):
    image = image.copy()
    image.thumbnail(max_size)
    return image

# Função para converter imagem de RGBA para RGB
def convert_rgba_to_rgb(image):
    if image.mode == 'RGBA':
        return image.convert('RGB')
    return image

# Função para codificar a imagem em base64 (com compactação JPEG)
def encode_image(image, format="JPEG", quality=85):
    buffered = io.BytesIO()
    image.save(buffered, format=format, quality=quality)
    return base64.b64encode(buffered.getvalue()).decode()

# Função para realizar retry com backoff exponencial
def retry_with_exponential_backoff(func, max_retries=5, base_delay=1, max_delay=60):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
            st.warning(f"Erro ao chamar a API. Tentando novamente em {delay:.2f} segundos...")
            time.sleep(delay)

# Configuração do LLM e da memória para a conversa
template = open("templates/vision_assistant.md", "r").read()
prompt = PromptTemplate(input_variables=["input", "image"], template=template)
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")
memory = ConversationBufferMemory(memory_key="chat_history", input_key="input")
llm_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

# Interface do Streamlit
st.title("Assistente de Visão")

# Captura de imagem
image = camera_input_live()
if image:
    st.image(image)
    
    # Redimensionar e converter a imagem para RGB
    resized_image = resize_image(Image.open(io.BytesIO(image.getvalue())))
    rgb_image = convert_rgba_to_rgb(resized_image)
    
    # Codificar a imagem para base64
    encoded_image = encode_image(rgb_image)
    
    if st.button("Descrever Imagem"):
        # Gerar a descrição da imagem usando o modelo LLM
        def get_image_description(encoded_image):
            return llm_chain.run(input="Descreva essa imagem em detalhes.", image=encoded_image)
        
        image_description = retry_with_exponential_backoff(lambda: get_image_description(encoded_image))
        
        # Exibir a descrição da imagem
        st.write("Descrição da imagem:")
        st.write(image_description)
        
        # Iniciar conversa
        user_input = st.text_input("Faça uma pergunta sobre a imagem:")
        if user_input:
            # Responder à pergunta do usuário com retry
            def get_response(encoded_image):
                return llm_chain.run(input=user_input, image=encoded_image)
            
            response = retry_with_exponential_backoff(lambda: get_response(encoded_image))
            st.write("Resposta:")
            st.write(response)

# Exibir histórico da conversa
if st.button("Mostrar histórico da conversa"):
    st.write(memory.chat_memory.messages)
