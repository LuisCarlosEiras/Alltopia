import streamlit as st
import cv2
import numpy as np
from transformers import LLaMAForCausalLM, LLaMATokenizer

# Carregue o modelo LLaMA e o tokenizer
tokenizer = LLaMATokenizer.from_pretrained("llama-3b")
model = LLaMAForCausalLM.from_pretrained("llama-3b")

# Inicialize a câmera
cap = cv2.VideoCapture(0)

# Crie uma sessão Streamlit
st.title("Análise de Imagens com LLaMA")
st.write("Olá! Estou pronto para analisar imagens.")

# Variável para parar o loop
stop_analysis = False

# Loop de captura e análise
while not stop_analysis:
    # Leia uma imagem da câmera
    ret, frame = cap.read()
    if not ret:
        st.write("Não foi possível capturar a imagem.")
        break

    # Exiba a imagem na sessão Streamlit
    st.image(frame, caption="Imagem capturada")

    # Pergunte ao usuário sobre a imagem
    user_input = st.text_input("O que você vê nesta imagem?", key="user_input")

    if user_input:
        # Analise o texto fornecido pelo usuário com o modelo LLaMA
        inputs = tokenizer(user_input, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(**inputs)
        prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Exiba a predição na interface
        st.write(f"Eu acho que a imagem é sobre: {prediction}")

    # Aguarde um pouco antes de capturar a próxima imagem
    cv2.waitKey(1)

    # Adicione um botão para interromper a análise
    if st.button("Parar Análise"):
        stop_analysis = True

# Libere a câmera
cap.release()
cv2.destroyAllWindows()
