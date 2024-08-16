import streamlit as st
import cv2
import numpy as np
from PIL import Image
import torch
from torchvision import transforms
from torchvision.models import resnet50
from llama_cpp import Llama

# Carregar modelo ResNet pré-treinado para análise de imagem
model = resnet50(pretrained=True)
model.eval()

# Transformações para pré-processamento da imagem
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Inicializar o modelo LLaMA
llm = Llama(model_path="llama-2-7b-chat.gguf")

# Função para capturar imagem da câmera
def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame

# Função para analisar a imagem
def analyze_image(image):
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)
    
    with torch.no_grad():
        output = model(input_batch)
    
    _, predicted_idx = torch.max(output, 1)
    return predicted_idx.item()

# Função para gerar descrição da imagem usando LLaMA
def generate_description(image_class):
    prompt = f"Descreva uma imagem que contém {image_class}."
    response = llm(prompt, max_tokens=100)
    return response['choices'][0]['text'].strip()

# Interface Streamlit
st.title("Análise de Imagem e Diálogo com LLaMA")

if st.button("Capturar Imagem"):
    image = capture_image()
    st.image(image, channels="BGR")
    
    # Converter imagem para formato PIL
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    # Analisar imagem
    image_class = analyze_image(pil_image)
    st.write(f"Classe detectada: {image_class}")
    
    # Gerar descrição
    description = generate_description(image_class)
    st.write("Descrição da imagem:")
    st.write(description)
    
    # Iniciar diálogo
    user_input = st.text_input("Faça uma pergunta sobre a imagem:")
    if user_input:
        prompt = f"Imagem: {description}\nPergunta: {user_input}\nResposta:"
        response = llm(prompt, max_tokens=100)
        st.write("Resposta:")
        st.write(response['choices'][0]['text'].strip())
