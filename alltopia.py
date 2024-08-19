import streamlit as st
from camera_input_live import camera_input_live
from langchain import LLMChain, PromptTemplate
from langchain_groq import ChatGroq
from PIL import Image
import cv2
import numpy as np
import io

# Configuração do modelo e da cadeia LLM
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
template = "Descreva a imagem com base nas seguintes características: {image_features}"
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
    img_array = np.array(img)
    
    # Convertendo para BGR (formato do OpenCV)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Calculando a cor média
    average_color = img_bgr.mean(axis=0).mean(axis=0)
    
    # Detectando bordas
    edges = cv2.Canny(img_bgr, 100, 200)
    edge_percentage = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
    
    # Calculando brilho médio
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    brightness = gray.mean()
    
    # Criando uma descrição básica
    description = f"Cor média RGB: {average_color[::-1].astype(int)}. "
    description += f"Aproximadamente {edge_percentage:.2%} da imagem contém bordas detectáveis. "
    description += f"Brilho médio: {brightness:.2f}/255. "
    
    # Classificação básica de brilho
    if brightness < 84:
        description += "A imagem parece ser escura. "
    elif brightness > 170:
        description += "A imagem parece ser clara. "
    else:
        description += "A imagem tem um brilho médio. "
    
    return description

# Interface do usuário
st.title("Descritor de Imagens")
image = camera_input_live()

if image:
    st.image(image)
    if st.button("Descrever imagem"):
        try:
            # Extrai características da imagem
            image_features = extract_image_features(image)
            
            # Loga as características extraídas
            st.write(f"Características da imagem: {image_features}")
            
            # Gera a descrição da imagem
            response = llm_chain.run(image_features=image_features)
            
            # Loga a resposta do modelo
            st.write(f"Resposta do modelo: {response}")
            
            # Exibe a descrição
            st.write("Descrição da imagem:", response)
            
        except Exception as e:
            st.error(f"Erro ao processar a imagem: {str(e)}")
