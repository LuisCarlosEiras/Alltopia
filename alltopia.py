import streamlit as st

try:
    import cv2
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, LlavaProcessor
    import speech_recognition as sr
except ImportError:
    st.error("Algumas bibliotecas necessárias não estão instaladas. Por favor, instale-as usando 'pip install opencv-python-headless torch transformers SpeechRecognition'")
    st.stop()

# Configuração da API key (se necessário)
api_key = st.secrets.get("GROQ_API_KEY", "")

# Carregando os modelos
llava_model_name = "llava-hf/llava-1.5-7b-hf"
llama_model_name = "meta-llama/Llama-2-7b-chat-hf"

try:
    llava_model = AutoModelForCausalLM.from_pretrained(llava_model_name)
    llava_tokenizer = AutoTokenizer.from_pretrained(llava_model_name)
    llava_processor = LlavaProcessor.from_pretrained(llava_model_name)
    
    llama_model = AutoModelForCausalLM.from_pretrained(llama_model_name)
    llama_tokenizer = AutoTokenizer.from_pretrained(llama_model_name)
except Exception as e:
    st.error(f"Erro ao carregar os modelos: {str(e)}")
    st.stop()

# Função para processar imagem com LLaVA
def analyze_image_with_llava(image):
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

# Configurando a interface do Streamlit
st.title("Análise de Imagem com Comandos de Voz")

if st.button("Capturar e Analisar Imagem"):
    command = recognize_speech()
    st.write(f"Comando reconhecido: {command}")
    
    if "analisar" in command.lower():
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
