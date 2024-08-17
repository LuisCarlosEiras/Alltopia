import streamlit as st
from camera_input_live import camera_input_live
from groq import Groq
from PIL import Image
import io

# Inicializar o cliente Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def resize_image(image, max_size=(800, 800)):
    img = Image.open(image)
    img = img.convert('RGB')
    img.thumbnail(max_size)
    return img

def describe_image_locally(image):
    width, height = image.size
    description = f"A imagem tem dimensões de {width}x{height} pixels."
    return description

def analyze_image(image):
    resized_image = resize_image(image)
    local_description = describe_image_locally(resized_image)
    
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
        return f"Error analyzing image: {str(e)}"

st.title("Image Capture and Analysis")

image = camera_input_live()

if image:
    st.image(image)
    
    with st.spinner("Analyzing image..."):
        image_analysis = analyze_image(image)
        st.subheader("Image Analysis")
        st.write(image_analysis)
