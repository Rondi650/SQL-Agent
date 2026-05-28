from datetime import datetime

from fastapi import FastAPI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.types import Command
from rich import print
from rich.markdown import Markdown

from my_agent import agent
from my_agent.models.request import PerguntaModel, ResumeModel
from my_agent.models.response import RespostaModel
from my_agent.config.settings import THREAD_CONFIG

app = FastAPI()


@app.post("/chat")
def chat_start(data: PerguntaModel) -> dict | RespostaModel:
    pergunta = data.pergunta
    thread_id = f"api_{datetime.now().timestamp()}"
    config = THREAD_CONFIG.copy()
    config["configurable"]["thread_id"] = thread_id

    last_output = None
    for step in agent.stream(
        {"messages": [HumanMessage(content=pergunta)]},
        config=config,
        stream_mode="values",
    ):
        print(step)
        print(Markdown("---"))

        if isinstance(step, dict) and "__interrupt__" in step:
            interrupt_val = step["__interrupt__"][0].value
            agent_explanation = (
                step["messages"][-1].content if step.get("messages") else ""
            )
            return {
                "status": "awaiting_approval",
                "thread_id": thread_id,
                "interrupt": interrupt_val,
                "agent_explanation": agent_explanation,
            }

        last_output = step

    msg = last_output["messages"][-1].content

    tokens_usados = 0
    last_msg = last_output["messages"][-1]
    if isinstance(last_msg, AIMessage) and last_msg.usage_metadata:
        tokens_usados = last_msg.usage_metadata.get("total_tokens", 0)

    print(Markdown(f"**Total de tokens usados:** {tokens_usados}"))

    return RespostaModel(
        response=msg,
        thread_id=thread_id,
        total_tokens=tokens_usados,
    )


@app.post("/chat/resume")
def chat_resume(data: ResumeModel) -> dict | RespostaModel:
    config = THREAD_CONFIG.copy()
    config["configurable"]["thread_id"] = data.thread_id

    resume_value = {"action": data.action, "feedback": data.feedback}

    last_output = None
    for step in agent.stream(
        Command(resume=resume_value),
        config=config,
        stream_mode="values",
    ):
        print(step)
        print(Markdown("---"))

        if isinstance(step, dict) and "__interrupt__" in step:
            interrupt_val = step["__interrupt__"][0].value
            agent_explanation = (
                step["messages"][-1].content if step.get("messages") else ""
            )
            return {
                "status": "awaiting_approval",
                "thread_id": data.thread_id,
                "interrupt": interrupt_val,
                "agent_explanation": agent_explanation,
            }

        last_output = step

    if last_output is None:
        return RespostaModel(
            response="Nenhuma resposta gerada.",
            thread_id=data.thread_id,
            total_tokens=0,
        )

    msg = last_output["messages"][-1].content

    tokens_usados = 0
    last_msg = last_output["messages"][-1]
    if isinstance(last_msg, AIMessage) and last_msg.usage_metadata:
        tokens_usados = last_msg.usage_metadata.get("total_tokens", 0)

    print(Markdown(f"**Total de tokens usados:** {tokens_usados}"))

    return RespostaModel(
        response=msg,
        thread_id=data.thread_id,
        total_tokens=tokens_usados,
    )


# Iniciar o servidor com: uvicorn main:app --reload --port 8081
