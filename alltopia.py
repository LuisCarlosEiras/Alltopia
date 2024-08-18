import streamlit as st
from camera_input_live import camera_input_live
from langchain import LLMChain, PromptTemplate
from langchain.memory import SimpleMemory
from langchain_groq import ChatGroq

# Acessar a chave da API do Groq a partir dos segredos
api_key = st.secrets["GROQ_API_KEY"]

# LLM Setup
template = open("templates/vision_assistant.md", "r").read()
prompt = PromptTemplate(input_variables=["input", "video_description"],
                        template=template)
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=api_key)
memory = SimpleMemory(memory_key="chat_history", input_key="input")
llm_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

# LLM Prompter
template2 = open("templates/vision_prompter.md", "r").read()
prompt2 = PromptTemplate(input_variables=["input"],
                         template=template2)
llm2 = ChatGroq(temperature=0, model_name="llama3-8b-8192", api_key=api_key)
memory2 = SimpleMemory(memory_key="chat_history", input_key="input")
llm_chain2 = LLMChain(llm=llm2, prompt=prompt2, memory=memory2)

# Streamlit UI
st.title("Vision Assistant and Prompter")

# Video Capture Setup
st.header("Video Capture")
image = camera_input_live()
if image:
    st.image(image, caption="Captured Image", use_column_width=True)

# Video Description Input
st.header("Video Description")
video_description = st.text_area("Describe the video", "")

# Vision Assistant Input and Response
st.header("Vision Assistant")
input_text = st.text_input("Enter your command or query for the assistant", "")
if st.button("Run Vision Assistant"):
    if video_description and input_text:
        response = llm_chain.run(input=input_text, video_description=video_description)
        st.write("Assistant Response:")
        st.write(response)
    else:
        st.warning("Please provide both a video description and a query.")

# Vision Prompter Input and Response
st.header("Vision Prompter")
input_text2 = st.text_input("Enter your command or query for the prompter", "")
if st.button("Run Vision Prompter"):
    if input_text2:
        response2 = llm_chain2.run(input=input_text2)
        st.write("Prompter Response:")
        st.write(response2)
    else:
        st.warning("Please enter a query for the prompter.")

# Chat History Display
st.header("Chat History")
st.write(memory.load_memory())
st.write(memory2.load_memory())

# Save memory states to file (Optional)
if st.button("Save Chat History"):
    with open("chat_history_assistant.txt", "w") as f:
        f.write(str(memory.load_memory()))
    with open("chat_history_prompter.txt", "w") as f:
        f.write(str(memory2.load_memory()))
    st.success("Chat histories saved successfully!")
