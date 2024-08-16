import streamlit as st
import cv2
import torch
import time
import requests
from transformers import AutoProcessor, LlavaForConditionalGeneration, AutoTokenizer, AutoModelForCausalLM
import speech_recognition as sr

# Configuração
st.set_page_config(page_title="Análise de Imagem com Comandos de Voz", layout="wide")

# Função para carregar modelo em 8-bit
@st.cache_resource
def load_model_in_8bit(model_name):
    try:
        return LlavaForConditionalGeneration.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            load_in_8bit=True,
        )
    except Exception as e:
        st.error(f"Erro ao carregar o modelo {model_name}: {str(e)}")
        return None

# Carregando os modelos
@st.cache_resource
def load_models():
    llava_model_name = "llava-hf/llava-1.5-3b-hf"
    llama_model_name = "meta-llama/Llama-2-7b-chat-hf"

    max_retries = 3
    retry_delay = 5

    for _ in range(max_retries):
        try:
            llava_model = load_model_in_8bit(llava_model_name)
            llava_processor = AutoProcessor.from_pretrained(llava_model_name)
            
            llama_model = load_model_in_8bit(llama_model_name)
            llama_tokenizer = AutoTokenizer.from_pretrained(llama_model_name)
            
            return llava_model, llava_processor, llama_model, llama_tokenizer
        except Exception as e:
            st.warning(f"Tentativa falhou: {str(e)}. Tentando novamente em {retry_delay} segundos...")
            time.sleep(retry_delay)
    
    st.error("Falha ao carregar os modelos após várias tentativas.")
    return None, None, None, None

# Função para processar imagem com LLaVA
def analyze_image_with_llava(image, llava_model, llava_processor):
    if llava_model is None or llava_processor is None:
        return "Modelo não carregado corretamente."
    
    img_resized = cv2.resize(image, (224, 224))
    inputs = llava_processor(text="Descreva a imagem:", images=img_resized, return_tensors="pt")
    
    with torch.no_grad():
        outputs = llava_model.generate(**inputs, max_new_tokens=100)
    
    description = llava_processor.decode(outputs[0], skip_special_tokens=True)
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

# Interface principal
def main():
    st.title("Análise de Imagem com Comandos de Voz")

    llava_model, llava_processor, llama_model, llama_tokenizer = load_models()

    if llava_model is None:
        st.error("Não foi possível carregar os modelos. Por favor, tente novamente mais tarde.")
        return

    if st.button("Capturar e Analisar Imagem"):
        command = recognize_speech()
        st.write(f"Comando reconhecido: {command}")
        
        if "analisar" in command.lower():
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()
            if ret:
                description = analyze_image_with_llava(frame, llava_model, llava_processor)
                st.image(frame, channels="BGR", caption="Imagem capturada")
                st.write(f"Análise: {description}")
            else:
                st.write("Erro ao capturar a imagem.")
    elif st.button("Sair"):
        st.write("Encerrando a aplicação.")

if __name__ == "__main__":
    main()
