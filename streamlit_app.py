import streamlit as st
import requests
import json
from datetime import datetime
from typing import Optional
from PIL import Image
import os

# Page configuration
st.set_page_config(
    page_title="SQL Agent Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8081"
API_ENDPOINT = f"{API_BASE_URL}/chat"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# Load avatars
avatar_human = None
avatar_assistant = None

if os.path.exists("my_agent/utils/images/avatar_human.png"):
    try:
        avatar_human = Image.open("my_agent/utils/images/avatar_human.png")
    except Exception as e:
        st.warning(f"Não foi possível carregar avatar_human.png: {e}")

if os.path.exists("my_agent/utils/images/avatar_ia.png"):
    try:
        avatar_assistant = Image.open("my_agent/utils/images/avatar_ia.png")
    except Exception as e:
        st.warning(f"Não foi possível carregar avatar_ia.png: {e}")

# Header
st.title("SQL Agent Chat")
st.markdown(
    "Faça perguntas sobre seus dados e o agente irá responder usando SQL ou ferramentas calculadas.")

# Sidebar with info
with st.sidebar:
    st.header("Configurações")

    api_url = st.text_input(
        "URL da API",
        value=API_BASE_URL,
        help="Endereço da API da aplicação"
    )

    # Update API endpoint if URL changed
    if api_url != API_BASE_URL:
        API_ENDPOINT = f"{api_url}/chat"

    st.markdown("---")
    st.subheader("Informações da Sessão")

    if st.session_state.thread_id:
        st.info(f"**Thread ID:** `{st.session_state.thread_id}`")
    else:
        st.info("Nenhuma conversa iniciada ainda")

    st.markdown("---")
    st.subheader("Exemplos de Perguntas")
    
    # Categorize examples
    examples_by_category = {
        "Desempenho": [
            "Qual é a nota média de exame dos estudantes?",
            "Qual é o score de produtividade máximo?",
            "Qual é o nível médio de burnout?"
        ],
        "Top Estudantes": [
            "Quais são os 10 melhores estudantes por nota?",
            "Quem são os 5 estudantes mais produtivos?",
            "Quais têm o menor burnout?"
        ],
        "Hábitos de Estudo": [
            "Qual é a média de horas de estudo?",
            "Quanto tempo em redes sociais em média?",
            "Qual o tempo total de tela médio?"
        ],
        "Saúde e Bem-estar": [
            "Qual é o score médio de saúde mental?",
            "Quantos minutos de exercício em média?",
            "Qual é a ingestão média de cafeína?"
        ],
        "Análises Demográficas": [
            "Qual a nota média por nível acadêmico?",
            "Qual o burnout médio por gênero?",
            "Produtividade dos alunos de trabalho part-time?"
        ]
    }
    
    counter = 0
    for category, questions in examples_by_category.items():
        with st.expander(category, expanded=False):
            for question in questions:
                counter += 1
                if st.button(question, key=f"example_{counter}", use_container_width=True):
                    st.session_state.pending_question = question
                    st.rerun()

    st.markdown("---")
    st.subheader("Links Úteis")
    st.markdown(f"[Documentação Swagger]({api_url}/docs)")
    st.markdown(f"[Documentação ReDoc]({api_url}/redoc)")

# Display chat history
for message in st.session_state.messages:
    avatar = avatar_human if message["role"] == "user" else avatar_assistant
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if "metadata" in message:
            with st.expander("Detalhes"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.caption(f"**Data/Hora:** {message['metadata'].get('data_hora', 'N/A')}")
                with col2:
                    st.caption(f"**Thread:** `{message['metadata'].get('thread_id', 'N/A')}`")
                with col3:
                    tokens = message['metadata'].get('total_tokens', 0)
                    st.caption(f"**Tokens Usados:** {tokens}")

# Chat input
user_input = st.chat_input("Digite sua pergunta aqui...", key="chat_input")

# Use pending question if available (from example buttons)
if st.session_state.pending_question:
    user_input = st.session_state.pending_question
    st.session_state.pending_question = None

if user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message
    with st.chat_message("user", avatar=avatar_human):
        st.markdown(user_input)

    # Make API request
    with st.chat_message("assistant", avatar=avatar_assistant):
        with st.spinner("Processando sua pergunta..."):
            try:
                response = requests.post(
                    API_ENDPOINT,
                    json={"pergunta": user_input},
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()
                    assistant_message = data.get(
                        "response", "Erro ao processar resposta")
                    thread_id = data.get("thread_id", "desconhecido")
                    data_hora = data.get("data_hora", datetime.utcnow().isoformat())
                    total_tokens = data.get("total_tokens", 0)

                    # Update thread ID
                    st.session_state.thread_id = thread_id

                    # Display response
                    st.markdown(assistant_message)

                    # Show metadata
                    with st.expander("Detalhes"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.caption(f"**Data/Hora:** {data_hora}")
                        with col2:
                            st.caption(f"**Thread:** `{thread_id}`")
                        with col3:
                            st.caption(f"**Tokens Usados:** {total_tokens}")

                    # Add to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_message,
                        "metadata": {
                            "data_hora": data_hora,
                            "thread_id": thread_id,
                            "total_tokens": total_tokens
                        }
                    })
                else:
                    error_msg = f"Erro da API (Status {response.status_code})"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })

            except requests.exceptions.ConnectionError:
                error_msg = "Erro: Não foi possível conectar à API. Verifique se a aplicação está rodando em http://localhost:8000"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
            except requests.exceptions.Timeout:
                error_msg = "Erro: Requisição expirou. Tente novamente."
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
            except Exception as e:
                error_msg = f"Erro inesperado: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

# Clear chat button
if st.session_state.messages:
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Limpar Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.thread_id = None
            st.rerun()

# iniciar streamlit run streamlit_app.py