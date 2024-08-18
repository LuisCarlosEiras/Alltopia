import streamlit as st
from camera_input_live import camera_input_live
import llama

# Inicialize o modelo Llama3-70b-8192
llama_model = llama.LLaMAForImageCaptioning.from_pretrained("Llama3-70b-8192")

image = camera_input_live()

if image:
    st.image(image)

    # Adicione um botão "Pause capturing" que, quando pressionado, gera uma descrição da imagem
    if st.button("Pause capturing"):
        # Converta a imagem para um formato que o modelo Llama possa processar
        img_array = np.array(image)
        img_tensor = torch.tensor(img_array).unsqueeze(0)

        # Gere a descrição da imagem usando o modelo Llama
        caption = llama_model.generate(img_tensor, max_length=50)

        # Exiba a descrição da imagem no aplicativo Streamlit
        st.write("Image description:", caption)
