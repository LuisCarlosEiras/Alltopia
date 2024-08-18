import streamlit as st
from camera_input_live import camera_input_live
import requests
import os

# Import the secrets module
from streamlit import secrets_manager

# Initialize the secrets manager
secrets_manager.init()

# Load the secrets from the secrets.toml file
secrets = secrets_manager.get_secrets()

# Access the GROG_API_KEY secret
GROG_API_KEY = secrets["GROG_API_KEY"]

image = camera_input_live()

if image:
    st.image(image)

    # Adicione um botão "Pause capturing" que, quando pressionado, gera uma descrição da imagem
    if st.button("Pause capturing"):
        # Converta a imagem para um formato que a API do GROG possa processar
        img_array = np.array(image)
        img_bytes = BytesIO()
        PIL.Image.fromarray(img_array).save(img_bytes, format="PNG")
        img_bytes.seek(0)

        # Faça uma solicitação à API do GROG para gerar a descrição da imagem
        response = requests.post(
            f"https://api.grog.io/v1/describe",
            headers={"Authorization": f"Bearer {GROG_API_KEY}"},
            files={"image": img_bytes}
        )

        # Verifique se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Exiba a descrição da imagem no aplicativo Streamlit
            caption = response.json()["description"]
            st.write("Image description:", caption)
        else:
            st.write("Error:", response.text)
