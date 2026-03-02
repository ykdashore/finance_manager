import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000/api/chat/message"
DEFAULT_USER_ID = "demo_user"
DEFAULT_TZ = "Asia/Kolkata"

st.set_page_config(
    page_title="AI Finance Manager",
    layout="centered",
)

st.title("AI Personal Finance Manager")
st.markdown(
    """
    <style>
    .stChatMessage {
        border-radius: 16px;
        padding: 14px;
        font-size: 16px;
    }
    .stChatInputContainer {
        border-top: 1px solid #ddd;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.caption("LangGraph + Gemini + FastAPI + SQLAlchemy")


if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "user_id" not in st.session_state:
    st.session_state.user_id = DEFAULT_USER_ID


with st.sidebar:
    st.header("Session Controls")

    st.text_input("User ID", key="user_id")

    if st.button("New Chat"):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.success("New session started")

    st.markdown("---")
    st.write("Thread ID:")
    st.code(st.session_state.thread_id)


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


user_input = st.chat_input("Log an expense or ask for a report...")

if user_input:
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare payload for FastAPI
    payload = {
        "message": user_input,
        "user_id": st.session_state.user_id,
        "thread_id": st.session_state.thread_id,
        "tz": DEFAULT_TZ,
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json=payload, timeout=65)
                response.raise_for_status()
                data = response.json()

                assistant_reply = data.get(
                    "agent_response",
                    "No response received from agent.",
                )

            except requests.exceptions.Timeout:
                assistant_reply = "Request timed out."
            except Exception as e:
                assistant_reply = f"Error connecting to backend: {e}"

            st.markdown(assistant_reply)

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
