import streamlit as st
from camera_input_live import camera_input_live
from PIL import Image
import io
import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from groq import ChatGroq  # Certifique-se de ter a biblioteca correta para integração

# Configuração da chave API (Token)
import os
groq_api_key = st.secrets["GROQ_API_KEY"]  # Chave armazenada no secrets do Streamlit

# Configuração do modelo LLM
template = open("templates/vision_assistant.md", "r").read()
prompt = PromptTemplate(input_variables=["input", "video_description"],
                        template=template)
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=groq_api_key)
memory = ConversationBufferMemory(memory_key="chat_history",
                                  input_key="input")
llm_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

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

        # Executando o LLMChain com a entrada e a descrição do vídeo
        response = llm_chain.run(input=input_text, video_description=video_description)
        st.write("Resposta da API Groq:")
        st.write(response)
else:
    st.error("Nenhuma imagem capturada.")
