import streamlit as st
from camera_input_live import camera_input_live
from groq import Groq
from PIL import Image
import io
import time

# Inicializar o cliente Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def resize_image(image, max_size=(800, 800)):
    img = Image.open(image)
    img = img.convert('RGB')
    img.thumbnail(max_size)
    return img

def describe_image_locally(image):
    # Análise básica da imagem usando PIL
    width, height = image.size
    colors = image.getcolors(image.size[0] * image.size[1])
    dominant_color = max(colors, key=lambda x: x[0])[1]
    brightness = sum(dominant_color) / 3

    description = f"A imagem tem dimensões de {width}x{height} pixels. "
    description += f"A cor dominante tem valores RGB de {dominant_color}. "
    description += f"A luminosidade média estimada é de {brightness:.2f} (em uma escala de 0 a 255)."

    return description

def analyze_image_with_retry(image, max_retries=3, initial_wait=10):
    resized_image = resize_image(image)
    local_description = describe_image_locally(resized_image)
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "You are an AI that analyzes image descriptions."},
                    {"role": "user", "content": f"Analyze this image description and provide insights: {local_description}"}
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
            {"role": "assistant", "content": f"The image analysis shows: {image_description}"},
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
            image_analysis = analyze_image_with_retry(image)
            st.subheader("Image Analysis")
            st.write(image_analysis)
        except Exception as e:
            st.error(f"Error analyzing image: {str(e)}")
    
    st.subheader("Chat about the Image")
    user_input = st.text_input("Ask a question about the image:")
    
    if user_input:
        with st.spinner("Processing your question..."):
            try:
                response = chat_about_image(user_input, image_analysis)
                st.write("AI Response:", response)
            except Exception as e:
                st.error(f"Error processing question: {str(e)}")
