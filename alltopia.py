import streamlit as st
import cv2

# Inicialize a câmera
cap = cv2.VideoCapture(0)

# Crie um título para a aplicação
st.title("Câmera em Tempo Real")

# Crie um container para a imagem
image_container = st.container()

while True:
    # Leia um frame da câmera
    ret, frame = cap.read()
    
    # Converta o frame para um formato que o Streamlit possa entender
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Exiba o frame na aplicação
    image_container.image(frame, use_column_width=True)
    
    # Aguarde um pouco antes de ler o próximo frame
    cv2.waitKey(1)
