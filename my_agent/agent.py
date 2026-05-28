from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver
from pathlib import Path
from .utils import (
    CUSTOM_TOOLS,
    roteador,
    should_continue,
    human_approval_node,
)

def create_agent():
    """Cria e compila o grafo do agente"""
    tools_node = ToolNode(CUSTOM_TOOLS, name="tools")
    
    builder = StateGraph(MessagesState)
    builder.add_node("roteador", roteador)
    builder.add_node("tools", tools_node)
    builder.add_node("human_approval", human_approval_node)
    
    builder.add_edge(START, "roteador")
    builder.add_conditional_edges(
        "roteador",
        should_continue,
        {"human_approval": "human_approval", "__end__": "__end__"},
    )
    builder.add_edge("human_approval", "tools")
    builder.add_edge("tools", "roteador")
    
    checkpointer = InMemorySaver()
    agent = builder.compile(checkpointer=checkpointer)
    
    return agent

# Criar instância do agente
agent = create_agent()

# Show workflow
CAMINHO = Path(__file__).parent

png_bytes = agent.get_graph().draw_mermaid_png()

with open(CAMINHO / "agent_workflow.png", "wb") as f:
    f.write(png_bytes)