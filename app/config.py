import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GOOGLE_APPLICATION_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_PATH")

APP_TZ = os.getenv("APP_TZ")

DB_PATH = os.getenv("DB_PATH")
GRAPH_STATE_DB = os.getenv("GRAPH_STATE_DB", "graph_state.db")

DEFAULT_USER_ID = os.getenv("DEFAULT_USER_ID")
DEFAULT_THREAD_ID = os.getenv("DEFAULT_THREAD_ID")

LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")



