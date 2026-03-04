import token

from fastapi import FastAPI
from my_agent import agent
from my_agent.models.request import PerguntaModel
from my_agent.models.response import RespostaModel
from langchain_core.messages import HumanMessage, AIMessage
from my_agent.config.settings import THREAD_CONFIG
from rich import print
from rich.markdown import Markdown

app = FastAPI()

@app.post("/chat")
def chat_endpoint(data: PerguntaModel) -> RespostaModel:
    """Endpoint para chat com o agente"""
    pergunta = data.pergunta
    msg=""

    tokens_usados = 0
    for step in agent.stream(
        {"messages": [HumanMessage(content=pergunta)]},
        config=THREAD_CONFIG,
        stream_mode="values"
    ):
        print(step)
        print(Markdown("---"))
           
        msg = step["messages"][-1].content

        last_msg = step["messages"][-1]
        if isinstance(last_msg, AIMessage) and last_msg.usage_metadata:
            tokens = last_msg.usage_metadata.get("total_tokens", 0)
            tokens_usados += tokens
    print(Markdown(f"**Total de tokens usados:** {tokens_usados}"))
        
    return RespostaModel(
        response=msg,
        thread_id="api_conversation",
        total_tokens=tokens_usados
    )
    
# Iniciar o servidor com: uvicorn main:app --reload