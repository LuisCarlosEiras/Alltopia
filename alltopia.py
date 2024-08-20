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

# Configuração do LLM para descrição de imagens
template2 = open("templates/vision_prompter.md", "r").read()
prompt2 = PromptTemplate(input_variables=["input"], template=template2)
llm2 = ChatGroq(temperature=0, model_name="llama3-8b-8192")
memory2 = ConversationBufferMemory(memory_key="chat_history", input_key="input")
llm_chain2 = LLMChain(llm=llm2, prompt=prompt2, memory=memory2)

# Configuração do LLM para perguntas sobre a imagem
template = open("templates/vision_assistant.md", "r").read()
prompt = PromptTemplate(input_variables=["input", "image_description"], template=template)
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
    
    # Codificar a imagem
    encoded_image = encode_image(rgb_image)
    
    # Limitar o tamanho da base64 para depuração
    prompt_input = f"Descreva esta imagem: data:image/jpeg;base64,{encoded_image[:2000]}"

    # Exibir o prompt de entrada para depuração
    st.write(f"Prompt de entrada: {prompt_input}")

    # Obter descrição da imagem com retry
    def get_image_description():
        return llm_chain2.run(input=prompt_input)
    
    image_description = retry_with_exponential_backoff(get_image_description)
    
    st.write("Descrição da imagem:")
    st.write(image_description)
    
    # Iniciar conversa
    user_input = st.text_input("Faça uma pergunta sobre a imagem:")
    if user_input:
        # Responder à pergunta do usuário com retry
        def get_response():
            return llm_chain.run(input=user_input, image_description=image_description)
        
        response = retry_with_exponential_backoff(get_response)
        st.write("Resposta:")
        st.write(response)

# Exibir histórico da conversa
if st.button("Mostrar histórico da conversa"):
    st.write(memory.chat_memory.messages)
