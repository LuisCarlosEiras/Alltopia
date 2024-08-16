import streamlit as st
import cv2
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import speech_recognition as sr
from io import BytesIO
import numpy as np

api_key = st.secrets["OPENAI_API_KEY"]

# Carregando os modelos
llava_model = AutoModelForCausalLM.from_pretrained("llava-v1.6-34b")
llava_tokenizer = AutoTokenizer.from_pretrained("llava-v1.6-34b")

llama_model = AutoModelForCausalLM.from_pretrained("llama3-8b-819")
llama_tokenizer = AutoTokenizer.from_pretrained("llama3-8b-819")

# Função para processar imagem com LLaVA
def analyze_image_with_llava(image):
    img_resized = cv2.resize(image, (224, 224))
    
    inputs = llava_tokenizer("Descreva a imagem:", return_tensors="pt")
    outputs = llava_model.generate(inputs.input_ids)
    description = llava_tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return description

# Função para capturar comando de voz
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Diga o comando:")
        audio = recognizer.listen(source)
        
        try:
            command = recognizer.recognize_google(audio, language='pt-BR')
            return command
        except sr.UnknownValueError:
            return "Não entendi o que você disse"
        except sr.RequestError:
            return "Erro ao tentar reconhecer o comando"

# Configurando a interface do Streamlit
st.title("Análise de Imagem com Comandos de Voz")

if st.button("Capturar e Analisar Imagem"):
    command = recognize_speech()
    st.write(f"Comando reconhecido: {command}")
    
    if "analisar" in command:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if ret:
            description = analyze_image_with_llava(frame)
            st.image(frame, channels="BGR", caption=f"Eu vejo: {description}")
        else:
            st.write("Erro ao capturar a imagem.")

elif st.button("Sair"):
    st.write("Encerrando a aplicação.")
