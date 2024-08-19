import streamlit as st
from camera_input_live import camera_input_live
from langchain import LLMChain, PromptTemplate
from langchain_groq import ChatGroq
import base64

# Configuração do modelo e da cadeia LLM
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
template = "Descreva a imagem fornecida: {image_description}"
prompt = PromptTemplate(input_variables=["image_description"], template=template)

try:
    llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=GROQ_API_KEY)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
except Exception as e:
    st.error(f"Erro ao inicializar o ChatGroq: {str(e)}")
    st.stop()

# Interface do usuário
st.title("Descritor de Imagens")
image = camera_input_live()

if image:
    st.image(image)
    if st.button("Descrever imagem"):
        try:
            # Converte a imagem para base64
            image_base64 = base64.b64encode(image.getvalue()).decode()
            
            # Gera a descrição da imagem
            response = llm_chain.run(image_description=image_base64)
            
            # Exibe a descrição
            st.write("Descrição da imagem:", response)
        except Exception as e:
            st.error(f"Erro ao processar a imagem: {str(e)}")
