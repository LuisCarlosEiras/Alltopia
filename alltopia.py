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

# Configuração da página Streamlit
st.set_page_config(page_title="Assistente de Visão", layout="wide")

# Configuração da chave API do Groq
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# Função para codificar a imagem em base64
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Configuração do LLM
template = open("templates/vision_assistant.md", "r").read()
prompt = PromptTemplate(input_variables=["input", "image_description"],
                        template=template)
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")
memory = ConversationBufferMemory(memory_key="chat_history",
                                  input_key="input")
llm_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

# Configuração do LLM Prompter
template2 = open("templates/vision_prompter.md", "r").read()
prompt2 = PromptTemplate(input_variables=["input"],
                         template=template2)
llm2 = ChatGroq(temperature=0, model_name="llama3-8b-8192")
memory2 = ConversationBufferMemory(memory_key="chat_history",
                                   input_key="input")
llm_chain2 = LLMChain(llm=llm2, prompt=prompt2, memory=memory2)

# Interface do Streamlit
st.title("Assistente de Visão")

# Captura de imagem
image = camera_input_live()
if image:
    st.image(image)
    
    # Codificar a imagem em base64
    encoded_image = encode_image(Image.open(io.BytesIO(image.getvalue())))
    
    # Obter descrição da imagem
    image_description = llm_chain2.run(input=f"Descreva esta imagem: data:image/png;base64,{encoded_image}")
    
    st.write("Descrição da imagem:")
    st.write(image_description)
    
    # Iniciar conversa
    user_input = st.text_input("Faça uma pergunta sobre a imagem:")
    if user_input:
        response = llm_chain.run(input=user_input, image_description=image_description)
        st.write("Resposta:")
        st.write(response)

# Exibir histórico da conversa
if st.button("Mostrar histórico da conversa"):
    st.write(memory.chat_memory.messages)
