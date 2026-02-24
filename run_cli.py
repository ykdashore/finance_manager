from langchain_core.messages import HumanMessage
from app.graph import build_graph
from app.config import DEFAULT_THREAD_ID, DEFAULT_USER_ID, APP_TZ


def main():
    app = build_graph()

    config = {
        "configurable":{
            "user_id": DEFAULT_USER_ID,
            "thread_id": DEFAULT_THREAD_ID,
            "tz":APP_TZ
        }
    }

    print("Personal Finance Manager (type 'quit' or 'exit' to quit))")
    while True:
        text = input("\nYou: ").strip()
        if text.lower() in ["exit", "quit"]:
            break
        out = app.invoke({"messages": [HumanMessage(content=text)]}, config=config)
        last_msg = out["messages"][-1]
        print("\nAgent: ", getattr(last_msg, "content", last_msg))

if __name__ == "__main__":
    main()