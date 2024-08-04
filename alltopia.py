import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI

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

# Estilo CSS para o título, subtítulos e imagem centralizada
st.markdown("""
<style>
    .full-width-title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        color: #333333;
        padding: 20px 0;
        margin: 0;
        width: 100%;
        # background-color: #f0f8ff;
    }
    .subtitle {
        font-size: 24px;
        text-align: center;
        color: #333333;
        margin-top: -20px;
        padding-bottom: 20px;
        # background-color: #f0f8ff;
    }
    div.stButton > button:first-child {
        # background-color: #0066cc;
        color: white;
        font-size: 20px;
        font-weight: bold;
        padding: 14px 20px;
        border-radius: 10px;
        border: 2px solid #0066cc;
        transition: all 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #0052a3;
        border-color: #0052a3;
    }
    .full-width-section {
        padding: 20px;
        background-color: #f0f2f6;
        margin-top: 30px;
    }
    .centered-image {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }
    .centered-image img {
        max-width: 50%;
        height: auto;
    }
</style>
""", unsafe_allow_html=True)

# Título em largura total
st.markdown('<p class="full-width-title">Alltopia, o game</p>', unsafe_allow_html=True)

# Subtítulo
st.markdown('<p class="subtitle">Crie sua sociedade perfeita</p>', unsafe_allow_html=True)

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

# Inicializar o dicionário de valores
valores = {caracteristica: 5.0 for caracteristica in caracteristicas}

# Dividir a tela em duas colunas do mesmo tamanho
col1, col2 = st.columns(2)

# Criação de sliders para cada característica na coluna da esquerda
with col1:
    st.markdown('<p class="subtitle">Escolha as características</p>', unsafe_allow_html=True)
    for caracteristica in caracteristicas:
        valores[caracteristica] = st.slider(caracteristica, 0.0, 10.0, 5.0)

# Exibir o gráfico de barras na coluna da direita
with col2:
    st.markdown('<p class="subtitle">Valores das características</p>', unsafe_allow_html=True)
    
    # Criar um DataFrame para o gráfico
    df = pd.DataFrame(list(valores.items()), columns=['Característica', 'Valor'])
    
    # Definir uma paleta de cores personalizada
    color_palette = px.colors.qualitative.Prism

    # Criar o gráfico de barras usando Plotly Express com cores diferentes
    fig = px.bar(df, x='Característica', y='Valor', 
                 labels={'Valor': 'Pontuação', 'Característica': ''},
                 height=400,
                 color='Característica',
                 color_discrete_sequence=color_palette)
    
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)
    
    # Exibir o gráfico
    st.plotly_chart(fig, use_container_width=True)

# Analisar a sociedade
media, analise = analisar_sociedade(valores)

# Seção de análise em largura total
st.markdown('<div class="full-width-section">', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Análise da Sociedade Resultante</p>', unsafe_allow_html=True)
st.write(f"Média dos Valores: {media:.2f}")
st.write(f"Classificação: {analise}")

# Função para obter a chave API de forma segura
def get_openai_api_key():
    return st.secrets["OPENAI_API_KEY"]

# Análise usando o modelo de linguagem natural da OpenAI
if st.button("Analise sua sociedade com OpenAI"):
    api_key = get_openai_api_key()
    if not api_key:
        st.error("Chave API da OpenAI não encontrada. Por favor, configure a chave nas configurações do Streamlit.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            
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
                temperature=1.0
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
                temperature=1.0
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
            st.image(image_url, width=716)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.subheader("Análise da sua utopia pelo OpenAI")
            
            # Dividir a análise em parágrafos e subtítulos
            paragrafos = analysis.split('\n\n')
            for paragrafo in paragrafos:
                if ': ' in paragrafo:
                    subtitulo, texto = paragrafo.split(': ', 1)
                    st.markdown(f"**{subtitulo}**")
                    st.write(texto)
                else:
                    st.write(paragrafo)
        
        except Exception as e:
            st.error(f"Erro ao chamar a API da OpenAI: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)
