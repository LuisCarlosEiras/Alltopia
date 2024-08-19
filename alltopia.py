import streamlit as st
from camera_input_live import camera_input_live
from langchain import LLMChain, PromptTemplate
from langchain_groq import ChatGroq
from PIL import Image
import io

# Configuração do modelo e da cadeia LLM
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
template = "Descreva a imagem fornecida: {image_features}"
prompt = PromptTemplate(input_variables=["image_features"], template=template)

try:
    llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=GROQ_API_KEY)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
except Exception as e:
    st.error(f"Erro ao inicializar o ChatGroq: {str(e)}")
    st.stop()

def extract_image_features(image):
    img = Image.open(image)
    img = img.convert('RGB')
    # Aqui você pode adicionar lógica para extrair características da imagem (cores, objetos, etc.)
    # Exemplo: Apenas retornando uma descrição genérica para fins de ilustração
    return "Imagem com cores vivas, contendo céu azul e vegetação."

# Interface do usuário
st.title("Descritor de Imagens")
image = camera_input_live()

if image:
    st.image(image)
    if st.button("Descrever imagem"):
        try:
            # Extrai características da imagem em vez de convertê-la para base64
            image_features = extract_image_features(image)
            
            # Gera a descrição da imagem
            response = llm_chain.run(image_features=image_features)
            
            # Exibe a descrição
            st.write(f"Características da imagem: {image_features}")

        except Exception as e:
            st.error(f"Erro ao processar a imagem: {str(e)}")
