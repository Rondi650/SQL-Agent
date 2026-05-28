import streamlit as st
import requests
import json
from datetime import datetime
from typing import Optional
from PIL import Image
import os

st.set_page_config(
    page_title="SQL Agent Chat",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

API_BASE_URL = "http://localhost:8081"
API_CHAT_ENDPOINT = f"{API_BASE_URL}/chat"
API_RESUME_ENDPOINT = f"{API_BASE_URL}/chat/resume"

if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None
if "pending_approval" not in st.session_state:
    st.session_state.pending_approval = None

avatar_human = None
avatar_assistant = None

if os.path.exists("my_agent/utils/images/avatar_human.png"):
    try:
        avatar_human = Image.open("my_agent/utils/images/avatar_human.png")
    except Exception as e:
        st.warning(f"Nao foi possivel carregar avatar_human.png: {e}")

if os.path.exists("my_agent/utils/images/avatar_ia.png"):
    try:
        avatar_assistant = Image.open("my_agent/utils/images/avatar_ia.png")
    except Exception as e:
        st.warning(f"Nao foi possivel carregar avatar_ia.png: {e}")

st.title("SQL Agent Chat")
st.markdown(
    "Faca perguntas sobre seus dados e o agente ira responder usando SQL ou ferramentas calculadas."
)

with st.sidebar:
    st.header("Configuracoes")

    api_url = st.text_input(
        "URL da API",
        value=API_BASE_URL,
        help="Endereco da API da aplicacao"
    )

    if api_url != API_BASE_URL:
        API_CHAT_ENDPOINT = f"{api_url}/chat"
        API_RESUME_ENDPOINT = f"{api_url}/chat/resume"

    st.markdown("---")
    st.subheader("Informacoes da Sessao")

    if st.session_state.thread_id:
        st.info(f"**Thread ID:** `{st.session_state.thread_id}`")
    else:
        st.info("Nenhuma conversa iniciada ainda")

    st.markdown("---")
    st.subheader("Exemplos de Perguntas")

    examples_by_category = {
        "Desempenho": [
            "Qual e a nota media de exame dos estudantes?",
            "Qual e o score de produtividade maximo?",
            "Qual e o nivel medio de burnout?"
        ],
        "Top Estudantes": [
            "Quais sao os 10 melhores estudantes por nota?",
            "Quem sao os 5 estudantes mais produtivos?",
            "Quais tem o menor burnout?"
        ],
        "Habitos de Estudo": [
            "Qual e a media de horas de estudo?",
            "Quanto tempo em redes sociais em media?",
            "Qual o tempo total de tela medio?"
        ],
        "Saude e Bem-estar": [
            "Qual e o score medio de saude mental?",
            "Quantos minutos de exercicio em media?",
            "Qual e a ingestao media de cafeina?"
        ],
        "Analises Demograficas": [
            "Qual a nota media por nivel academico?",
            "Qual o burnout medio por genero?",
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
    st.subheader("Links Uteis")
    st.markdown(f"[Documentacao Swagger]({api_url}/docs)")
    st.markdown(f"[Documentacao ReDoc]({api_url}/redoc)")

for message in st.session_state.messages:
    avatar = avatar_human if message["role"] == "user" else avatar_assistant
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if "metadata" in message:
            with st.expander("Detalhes"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.caption(
                        f"**Data/Hora:** {message['metadata'].get('data_hora', 'N/A')}")
                with col2:
                    st.caption(
                        f"**Thread:** `{message['metadata'].get('thread_id', 'N/A')}`")
                with col3:
                    tokens = message['metadata'].get('total_tokens', 0)
                    st.caption(f"**Tokens Usados:** {tokens}")


def call_api(endpoint: str, payload: dict) -> dict | None:
    try:
        resp = requests.post(endpoint, json=payload, timeout=60)
        if resp.status_code == 200:
            return resp.json()
        else:
            st.error(f"Erro da API (Status {resp.status_code})")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Erro: Nao foi possivel conectar a API. Verifique se a aplicacao esta rodando em http://localhost:8081")
        return None
    except requests.exceptions.Timeout:
        st.error("Erro: Requisicao expirou. Tente novamente.")
        return None
    except Exception as e:
        st.error(f"Erro inesperado: {str(e)}")
        return None


def handle_final_response(data: dict, thread_id: str):
    assistant_message = data.get("response", "Erro ao processar resposta")
    data_hora = data.get("data_hora", datetime.utcnow().isoformat())
    total_tokens = data.get("total_tokens", 0)

    st.session_state.thread_id = thread_id

    with st.chat_message("assistant", avatar=avatar_assistant):
        st.markdown(assistant_message)
        with st.expander("Detalhes"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"**Data/Hora:** {data_hora}")
            with col2:
                st.caption(f"**Thread:** `{thread_id}`")
            with col3:
                st.caption(f"**Tokens Usados:** {total_tokens}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_message,
        "metadata": {
            "data_hora": data_hora,
            "thread_id": thread_id,
            "total_tokens": total_tokens,
        }
    })


def process_approval_decision(thread_id: str, action: str, feedback: str = ""):
    result = call_api(API_RESUME_ENDPOINT, {
        "thread_id": thread_id,
        "action": action,
        "feedback": feedback,
    })
    if result is None:
        st.session_state.pending_approval = None
        st.rerun()

    if result.get("status") == "awaiting_approval":
        st.session_state.pending_approval = {
            "thread_id": result["thread_id"],
            "tool_calls": result["interrupt"]["tool_calls"],
            "agent_explanation": result.get("agent_explanation", ""),
        }
    else:
        st.session_state.pending_approval = None
        handle_final_response(result, thread_id)
    st.rerun()


user_input = st.chat_input("Digite sua pergunta aqui...", key="chat_input")

if st.session_state.pending_question:
    user_input = st.session_state.pending_question
    st.session_state.pending_question = None

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user", avatar=avatar_human):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar=avatar_assistant):
        with st.spinner("Processando sua pergunta..."):
            result = call_api(API_CHAT_ENDPOINT, {"pergunta": user_input})

    if result:
        if result.get("status") == "awaiting_approval":
            st.session_state.thread_id = result["thread_id"]
            st.session_state.pending_approval = {
                "thread_id": result["thread_id"],
                "tool_calls": result["interrupt"]["tool_calls"],
                "agent_explanation": result.get("agent_explanation", ""),
            }
        else:
            handle_final_response(result, result.get("thread_id", "desconhecido"))
    st.rerun()

if st.session_state.pending_approval:
    st.markdown("---")
    st.markdown("### Revisao Humana")

    info = st.session_state.pending_approval

    if info.get("agent_explanation"):
        with st.chat_message("assistant", avatar=avatar_assistant):
            st.markdown(info["agent_explanation"])

    st.markdown("**Ferramenta(s) que serao executadas:**")
    for tc in info.get("tool_calls", []):
        st.code(f"{tc['name']}({json.dumps(tc['args'], ensure_ascii=False)})", language="python")

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Aprovar", type="primary", use_container_width=True):
            process_approval_decision(info["thread_id"], "approve")

    feedback_text = st.text_input(
        "Feedback (opcional, se for rejeitar):",
        key="feedback_input",
        placeholder="Explique por que a consulta deve ser ajustada..."
    )

    with col2:
        if st.button("Rejeitar", use_container_width=True):
            process_approval_decision(info["thread_id"], "reject", feedback_text)

if st.session_state.messages:
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Limpar Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.thread_id = None
            st.session_state.pending_approval = None
            st.rerun()

# iniciar streamlit run streamlit_app.py
