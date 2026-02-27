from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import SystemMessage

# from langchain_openai import ChatOpenAI
import sqlite3
import os
from app.core.state import FinanceState
from app.core.prompts import SYSTEM_PROMPT
from app.tools import ALL_TOOLS
from app.tools.store import init_db
from app.core.config import (
    DEFAULT_USER_ID,
    APP_TZ,
    GOOGLE_APPLICATION_CREDENTIALS_PATH,
    GRAPH_STATE_DB,
    LLM_ID,
)
from langchain_google_genai import ChatGoogleGenerativeAI

if GOOGLE_APPLICATION_CREDENTIALS_PATH:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS_PATH


def _agent_model():
    return ChatGoogleGenerativeAI(
        model=LLM_ID,
        vertexai=True,
        project="agenticaiprep",
        location="us-central1",
        temperature=0.3,
        max_output_tokens=500,
        max_retries=2,
    ).bind_tools(ALL_TOOLS)


def agent_node(state: FinanceState):
    model = _agent_model()

    cfg = state.get("configurable", {}) if isinstance(state, dict) else {}
    user_id = cfg.get("user_id", DEFAULT_USER_ID)
    tz = cfg.get("tz", APP_TZ)

    config_sys = SystemMessage(content=f"CONFIG: user_id={user_id}, tz={tz}")

    messages = [SystemMessage(content=SYSTEM_PROMPT), config_sys] + state.get(
        "messages", []
    )
    print("=" * 50)
    print("Messages being sent to Gemini:")
    for i, msg in enumerate(messages):
        print(f"\nMessage {i}:")
        print(f"  Type: {type(msg).__name__}")
        print(f"  Content: {msg.content if hasattr(msg, 'content') else 'NO CONTENT'}")
        if hasattr(msg, "tool_calls"):
            print(f"  Tool calls: {msg.tool_calls}")
    print("=" * 50)

    msg = model.invoke(messages)
    return {"messages": [msg]}


def build_graph():
    init_db()

    tool_node = ToolNode(ALL_TOOLS)
    g = StateGraph(FinanceState)
    g.add_node("agent", agent_node)
    g.add_node("tools", tool_node)

    g.add_edge(START, "agent")
    g.add_conditional_edges(
        "agent", tools_condition, {"tools": "tools", "__end__": END}
    )
    g.add_edge("tools", "agent")

    conn = sqlite3.connect(GRAPH_STATE_DB, check_same_thread=False)
    checkpointer = SqliteSaver(conn)

    return g.compile(checkpointer=checkpointer)
