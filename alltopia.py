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
from PIL import Image
import io
import time

# Inicializar o cliente Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def resize_image(image, max_size=(800, 800)):
    img = Image.open(image)
    img = img.convert('RGB')
    img.thumbnail(max_size)
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return buffered.getvalue()

def encode_image(image_data):
    return base64.b64encode(image_data).decode('utf-8')

def describe_image_with_retry(image, max_retries=3, initial_wait=10):
    resized_image = resize_image(image)
    base64_image = encode_image(resized_image)
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "You are an AI that describes images accurately."},
                    {"role": "user", "content": f"Describe this image in detail: data:image/jpeg;base64,{base64_image}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            if "rate_limit_exceeded" in str(e):
                wait_time = initial_wait * (2 ** attempt)
                st.warning(f"Rate limit exceeded. Waiting for {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                raise e
    
    raise Exception("Max retries reached. Unable to process the image.")

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
        try:
            image_description = describe_image_with_retry(image)
            st.subheader("Image Description")
            st.write(image_description)
        except Exception as e:
            st.error(f"Error analyzing image: {str(e)}")
    
    st.subheader("Chat about the Image")
    user_input = st.text_input("Ask a question about the image:")
    
    if user_input:
        with st.spinner("Processing your question..."):
            try:
                response = chat_about_image(user_input, image_description)
                st.write("AI Response:", response)
            except Exception as e:
                st.error(f"Error processing question: {str(e)}")
