import streamlit as st
from camera_input_live import camera_input_live
import os
from langchain.llms import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

# Load the API key from Streamlit secrets
groq_api_key = st.secrets["GROQ_API_KEY"]

# Set up the LLMs
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=groq_api_key)
memory = ConversationBufferMemory(memory_key="chat_history", input_key="input")
template = open("templates/vision_assistant.md", "r").read()
prompt = PromptTemplate(input_variables=["input", "video_description"], template=template)
llm_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

# Set up the prompter LLM
llm2 = ChatGroq(temperature=0, model_name="llama3-8b-8192", api_key=groq_api_key)
memory2 = ConversationBufferMemory(memory_key="chat_history", input_key="input")
template2 = open("templates/vision_prompter.md", "r").read()
prompt2 = PromptTemplate(input_variables=["input"], template=template2)
llm_chain2 = LLMChain(llm=llm2, prompt=prompt2, memory=memory2)

# Capture an image from the camera
image = camera_input_live()
if image:
    st.image(image)

    # Describe the image using the vision assistant LLM
    input_text = "Describe the image"
    output = llm_chain.generate(input_text, video_description="Image description")
    st.write("Image description:", output)

    # Dialogue with the user about the image
    user_input = st.text_input("Ask a question about the image")
    if user_input:
        output = llm_chain2.generate(user_input, input=image)
        st.write("Response:", output)
