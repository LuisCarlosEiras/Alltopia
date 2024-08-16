import cv2
import streamlit as st
import numpy as np

def main():
    st.title("Visualizador de Câmera")

    # Tenta inicializar a câmera
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Não foi possível abrir a câmera. Verifique se ela está conectada e não está sendo usada por outro aplicativo.")
            return
    except Exception as e:
        st.error(f"Erro ao inicializar a câmera: {str(e)}")
        return

    # Cria um espaço para exibir a imagem
    image_placeholder = st.empty()

    stop_button = st.button('Parar')

    while not stop_button:
        try:
            # Captura frame por frame
            ret, frame = cap.read()

            if ret:
                # Converte a imagem de BGR para RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Exibe a imagem no Streamlit
                image_placeholder.image(frame)
            else:
                st.warning("Não foi possível capturar o frame da câmera.")
                break
        
        except Exception as e:
            st.error(f"Erro durante a captura: {str(e)}")
            break

        # Atualiza o estado do botão
        stop_button = st.button('Parar')

    # Libera a câmera
    cap.release()
    st.write("Câmera desligada.")

if __name__ == '__main__':
    main()
