import streamlit as st
from camera_input_live import camera_input_live
import numpy as np
from io import BytesIO
from PIL import Image
from langchain import LLMChain, PromptTemplate
from langchain_groq import ChatGroq

# Access the GROG_API_KEY secret
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Configurar o modelo LLaMA3-70B-8192
template = "Descreva a imagem fornecida: {image_description}"
prompt = PromptTemplate(input_variables=["image_description"], template=template)
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=GROQ_API_KEY)
llm_chain = LLMChain(llm=llm, prompt=prompt)

image = camera_input_live()

if image:
    st.image(image)

    # Adicione um botão "Pause capturing" que, quando pressionado, gera uma descrição da imagem
    if st.button("Pause capturing"):
        # Converta a imagem para um array de bytes
        img_array = np.array(image)
        img_bytes = BytesIO()
        Image.fromarray(img_array).save(img_bytes, format="PNG")
        img_bytes.seek(0)

        # Converta a imagem para uma string codificada em base64 para entrada no modelo
        image_description = img_bytes.getvalue()

        # Gere a descrição da imagem usando a LLM
        response = llm_chain.run(image_description=image_description)

        # Exiba a descrição da imagem no aplicativo Streamlit
        st.write("Image description:", response)
