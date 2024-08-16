import streamlit as st
from PIL import Image
import numpy as np

def main():
    st.title("Visualizador de Imagem")

    # Cria um widget para upload de arquivo
    uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Lê a imagem
        image = Image.open(uploaded_file)
        
        # Converte a imagem para um array numpy
        image_array = np.array(image)
        
        # Exibe a imagem no Streamlit
        st.image(image_array, caption='Imagem carregada', use_column_width=True)

if __name__ == '__main__':
    main()
