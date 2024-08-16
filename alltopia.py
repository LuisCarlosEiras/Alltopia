import streamlit as st
import cv2
import numpy as np
from transformers import LLaMAForSequenceClassification, LLaMATokenizer

# Carregue o modelo LLaMA
tokenizer = LLaMATokenizer.from_pretrained("llama-3b")
model = LLaMAForSequenceClassification.from_pretrained("llama-3b", num_labels=8)

# Inicialize a câmera
cap = cv2.VideoCapture(0)

# Crie uma sessão Streamlit
st.title("Análise de Imagens com LLaMA")
st.write("Olá! Estou pronto para analisar imagens.")

while True:
    # Leia uma imagem da câmera
    ret, frame = cap.read()
    if not ret:
        break

    # Exiba a imagem na sessão Streamlit
    st.image(frame, caption="Imagem capturada")

    # Pergunte ao usuário sobre a imagem
    user_input = st.text_input("O que você vê nesta imagem?")

    # Analise a imagem com o modelo LLaMA
    inputs = tokenizer.encode_plus(
        user_input,
        add_special_tokens=True,
        max_length=512,
        return_attention_mask=True,
        return_tensors="pt"
    )
    outputs = model(inputs["input_ids"], attention_mask=inputs["attention_mask"])
    logits = outputs.logits
    predicted_class = np.argmax(logits)

    # Escreva sobre a imagem
    st.write(f"Eu acho que a imagem é sobre {predicted_class}.")

    # Aguarde um pouco antes de capturar a próxima imagem
    cv2.waitKey(1)

# Libere a câmera
cap.release()
cv2.destroyAllWindows()
