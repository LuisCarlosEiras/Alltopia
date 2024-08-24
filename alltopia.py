import streamlit as st
from camera_input_live import camera_input_live
from PIL import Image
import io
from groq import Groq
import base64

# Configuração da chave API (Token)
groq_api_key = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=groq_api_key)

def run_groq_query(messages):
    response = client.chat.completions.create(
        model="llama3-70b-8192",  # ou outro modelo suportado pela Groq
        messages=messages,
        max_tokens=300
    )
    return response.choices[0].message.content

# Função para baixar a imagem
def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

# Interface do Streamlit
st.title("Captura de Imagens com Streamlit e API Groq")

# Inicializar o histórico de mensagens na sessão do estado
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant specializing in image analysis."}
    ]

# Captura de imagem com streamlit-camera-input-live
image = camera_input_live()

# Verificação se a imagem foi capturada e exibição
if image:
    st.image(image)
    
    # Converte o arquivo BytesIO para uma imagem PIL
    img = Image.open(io.BytesIO(image.getvalue()))
    # Exibe informações da imagem
    st.write(f"Formato: {img.format}")
    st.write(f"Dimensões: {img.size}")
    st.write(f"Modo: {img.mode}")
    
    # Adiciona link para download da imagem
    st.markdown(get_image_download_link(img, "captured_image.png", "Baixar imagem capturada"), unsafe_allow_html=True)
    
    # Campo de texto para perguntas do usuário
    user_question = st.text_input("Faça uma pergunta sobre a imagem:")
    
    if st.button("Enviar pergunta para Groq API"):
        # Prepara a mensagem com a descrição da imagem e a pergunta do usuário
        input_text = f"""
        Uma imagem foi capturada usando a câmera. 
        Formato da imagem: {img.format}
        Dimensões: {img.width}x{img.height}
        Modo de cor: {img.mode}
        
        Pergunta do usuário: {user_question}
        """
        
        # Adiciona a mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": input_text})
        
        # Executando a query Groq com o histórico de mensagens
        response = run_groq_query(st.session_state.messages)
        
        # Adiciona a resposta ao histórico
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.write("Resposta da API Groq:")
        st.write(response)
    
    # Exibe o histórico da conversa
    st.subheader("Histórico da Conversa")
    for message in st.session_state.messages[1:]:  # Ignora a primeira mensagem do sistema
        st.write(f"{message['role'].capitalize()}: {message['content']}")
        
else:
    st.error("Nenhuma imagem capturada.")
