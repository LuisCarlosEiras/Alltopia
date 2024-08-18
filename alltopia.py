import streamlit as st
from camera_input_live import camera_input_live
import openai  # Substitua por sua biblioteca LLM escolhida

# Configurações da API OpenAI (ajuste conforme necessário)
openai.api_key = "YOUR_API_KEY"

def describe_image(image_bytes):
    """Gera uma descrição da imagem usando a API OpenAI.

    Args:
        image_bytes: Bytes da imagem a ser descrita.

    Returns:
        Uma string com a descrição da imagem.
    """

    response = openai.Image.create(
        model="gpt-4-vision",  # Modelo GPT-4 com capacidades visuais
        image=image_bytes,
        prompt="Descreva a imagem em detalhes.",
        max_tokens=100
    )
    return response.choices[0].text.caption

# Interface do Streamlit
st.title("Descricionador de Imagens")

image = camera_input_live()
if image:
    st.image(image, caption="Imagem Capturada")

    # Converter a imagem para bytes
    with io.BytesIO() as buffer:
        image.save(buffer, format='JPEG')
        image_bytes = buffer.getvalue()

    # Gerar a descrição da imagem
    description = describe_image(image_bytes)
    st.write("**Descrição da Imagem:**")
    st.markdown(description)
