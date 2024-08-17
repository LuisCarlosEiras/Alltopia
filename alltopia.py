import streamlit as st
from camera_input_live import camera_input_live
from langchain import PromptTemplate, LLMChain
from langchain.memory import ConversationBufferMemory
from groq import ChatGroq

# Função para descrever a imagem usando o LLM
def descrever_imagem(image):
    template = open("templates/vision_assistant.md", "r").read()
    prompt = PromptTemplate(input_variables=["input", "video_description"], template=template)
    llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="input")
    llm_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

    # Gerando a descrição da imagem
    video_description = "Descrição da imagem capturada"
    descricao = llm_chain.run(input=video_description)
    return descricao

# Função para interagir com o usuário sobre a imagem
def dialogar_sobre_imagem(user_input):
    template2 = open("templates/vision_prompter.md", "r").read()
    prompt2 = PromptTemplate(input_variables=["input"], template=template2)
    llm2 = ChatGroq(temperature=0, model_name="llama3-8b-8192")
    memory2 = ConversationBufferMemory(memory_key="chat_history", input_key="input")
    llm_chain2 = LLMChain(llm=llm2, prompt=prompt2, memory=memory2)

    # Resposta ao input do usuário
    resposta = llm_chain2.run(input=user_input)
    return resposta

# Captura da imagem
image = camera_input_live()
if image:
    st.image(image)

    # Descrição da imagem
    descricao = descrever_imagem(image)
    st.write(f"Descrição da Imagem: {descricao}")

    # Caixa de entrada de texto para o usuário interagir
    user_input = st.text_input("Digite algo sobre a imagem:")

    if user_input:
        resposta = dialogar_sobre_imagem(user_input)
        st.write(f"Assistente: {resposta}")
