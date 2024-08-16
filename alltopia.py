import cv2
import streamlit as st

def main():
    st.title("Visualizador de Câmera")

    # Inicializa a câmera
    cap = cv2.VideoCapture(0)

    # Cria um espaço para exibir a imagem
    image_placeholder = st.empty()

    while True:
        # Captura frame por frame
        ret, frame = cap.read()

        if ret:
            # Converte a imagem de BGR para RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Exibe a imagem no Streamlit
            image_placeholder.image(frame)
        
        # Adiciona um botão para parar a captura
        if st.button('Parar'):
            break

    # Libera a câmera e fecha as janelas
    cap.release()

if __name__ == '__main__':
    main()
