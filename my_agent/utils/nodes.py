from typing import Literal
from langgraph.graph import MessagesState
from langgraph.types import interrupt, Command
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from my_agent.config.settings import llm
from my_agent.config.prompts import GENERATE_QUERY_SYSTEM_PROMPT
from .tools import CUSTOM_TOOLS


def _sanitize_messages(msgs):
    result = list(msgs)
    for i in range(len(result) - 1, -1, -1):
        msg = result[i]
        if isinstance(msg, AIMessage) and msg.tool_calls:
            tc_ids = {tc["id"] for tc in msg.tool_calls}
            for j in range(i + 1, len(result)):
                if isinstance(result[j], ToolMessage) and result[j].tool_call_id in tc_ids:
                    tc_ids.discard(result[j].tool_call_id)
            if tc_ids:
                result[i] = AIMessage(content=msg.content)
    return result

def roteador(state: MessagesState) -> MessagesState:
    msgs = _sanitize_messages(state["messages"])
    llm_with_tools = llm.bind_tools(CUSTOM_TOOLS)
    system_message = SystemMessage(GENERATE_QUERY_SYSTEM_PROMPT)
    resp = llm_with_tools.invoke([system_message] + msgs)
    return {"messages": [resp]}

def should_continue(state: MessagesState) -> Literal["human_approval", "__end__"]:
    last = state["messages"][-1]
    if not isinstance(last, AIMessage) or not last.tool_calls:
        return "__end__"
    return "human_approval"

def human_approval_node(state: MessagesState) -> Command:
    last = state["messages"][-1]
    if not isinstance(last, AIMessage) or not last.tool_calls:
        return Command(goto="__end__")

    tool_call_details = [
        {"name": tc["name"], "args": tc.get("args", {})}
        for tc in last.tool_calls
    ]

    response = interrupt(
        {
            "type": "human_approval",
            "question": "O agente deseja executar a seguinte consulta. Aprovar?",
            "tool_calls": tool_call_details,
        }
    )

    if response.get("action") == "approve":
        return Command(goto="tools")
    else:
        feedback = response.get("feedback", "Consulta recusada. Reavaliar.")
        cleaned = AIMessage(content=last.content, id=last.id)
        feedback_msg = HumanMessage(
            content=(
                f"Sua abordagem anterior foi recusada. "
                f"Feedback: {feedback}. "
                f"Tente uma abordagem diferente."
            )
        )
        return Command(
            goto="roteador",
            update={"messages": [cleaned, feedback_msg]},
        )
