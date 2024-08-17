# import streamlit as st
# from camera_input_live import camera_input_live
# image = camera_input_live()
# if image:
#   st.image(image)

import streamlit as st
from camera_input_live import camera_input_live
from groq import Groq
import base64
import os

# Inicializar o cliente Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def encode_image(image):
    return base64.b64encode(image.getvalue()).decode('utf-8')

def describe_image(image):
    base64_image = encode_image(image)
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are an AI that describes images accurately."},
            {"role": "user", "content": f"Describe this image in detail: data:image/jpeg;base64,{base64_image}"}
        ]
    )
    return response.choices[0].message.content

def chat_about_image(user_input, image_description):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are an AI assistant that can discuss images based on their descriptions."},
            {"role": "assistant", "content": f"The image shows: {image_description}"},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

st.title("Image Capture and Analysis")

image = camera_input_live()

if image:
    st.image(image)
    
    with st.spinner("Analyzing image..."):
        image_description = describe_image(image)
    
    st.subheader("Image Description")
    st.write(image_description)
    
    st.subheader("Chat about the Image")
    user_input = st.text_input("Ask a question about the image:")
    
    if user_input:
        with st.spinner("Processing your question..."):
            response = chat_about_image(user_input, image_description)
        st.write("AI Response:", response)
