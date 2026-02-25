import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GOOGLE_APPLICATION_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_PATH")

LLM_ID = os.getenv("LLM_ID", "gemini-2.5-pro")

APP_TZ = os.getenv("APP_TZ", "Asia/Kolkata")

DB_PATH = os.getenv("DB_PATH", "expenses.db")
DB_URL = os.getenv("DB_URL", f"sqlite:///{DB_PATH}")
GRAPH_STATE_DB = os.getenv("GRAPH_STATE_DB", "graph_state.db")

DEFAULT_USER_ID = os.getenv("DEFAULT_USER_ID", "default_user")
DEFAULT_THREAD_ID = os.getenv("DEFAULT_THREAD_ID", "default_thread")

LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
