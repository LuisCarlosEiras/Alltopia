import streamlit as st
from openai import OpenAI
import pandas as pd
import plotly.express as px

# Configure sua chave de API da OpenAI
client = OpenAI(api_key='sua_chave_api_aqui')

# Características de uma sociedade utópica
caracteristicas = [
    "Igualdade Social",
    "Justiça e Equidade",
    "Bem-Estar Geral",
    "Paz e Harmonia",
    "Sustentabilidade",
    "Liberdade",
    "Tecnologia e Inovação",
    "Governança Participativa",
    "Comunidade e Solidariedade",
    "Felicidade e Realização Pessoal"
]

# ... [O restante do código CSS permanece o mesmo]

# Função para analisar a sociedade com base nos valores ajustados
def analisar_sociedade(valores):
    media = sum(valores.values()) / len(valores)
    
    if media >= 7:
        analise = "Utopia Alta"
    elif media >= 4:
        analise = "Utopia Moderada"
    else:
        analise = "Utopia Baixa"
    
    return media, analise

# ... [O código para a interface do usuário permanece o mesmo]

# Analisar a sociedade
media, analise = analisar_sociedade(valores)

# Seção de análise em largura total
st.markdown('<div class="full-width-section">', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Análise da Sociedade Resultante</p>', unsafe_allow_html=True)
st.write(f"Média dos Valores: {media:.2f}")
st.write(f"Classificação: {analise}")

# Análise usando o modelo de linguagem natural da OpenAI
if st.button("Analisar com OpenAI"):
    input_text = (
        f"Analise a sociedade utópica com as seguintes características: {valores}. "
        "Escreva a análise com subtítulos e 5 parágrafos de texto, em português do Brasil."
    )
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=input_text,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7
    )
    analysis = response.choices[0].text.strip()
    
    # Gerar prompt para imagem do DALL-E
    image_prompt_input = (
        f"Crie uma imagem que represente uma sociedade utópica com as seguintes características: {valores}. "
        "O prompt deve ter 3 linhas de texto, em português do Brasil."
    )
    image_prompt_response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=image_prompt_input,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )
    image_prompt = image_prompt_response.choices[0].text.strip()
    
    # Gerar imagem automaticamente com o prompt
    response = client.images.generate(
        model="dall-e-3",
        prompt=image_prompt,
        size="1024x1024",
        n=1,
    )
    image_url = response.data[0].url
    
    # Exibir a imagem centralizada
    st.markdown('<div class="centered-image">', unsafe_allow_html=True)
    st.image(image_url, use_column_width=False)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.subheader("Análise da Sociedade pelo OpenAI")
    
    # Dividir a análise em parágrafos e subtítulos
    paragrafos = analysis.split('\n\n')
    for paragrafo in paragrafos:
        if ': ' in paragrafo:
            subtitulo, texto = paragrafo.split(': ', 1)
            st.markdown(f"**{subtitulo}**")
            st.write(texto)
        else:
            st.write(paragrafo)

st.markdown('</div>', unsafe_allow_html=True)
