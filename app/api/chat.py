from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage
from app.models.schemas import ChatSchema, ChatResponseSchema
from app.core.state_graph import build_graph
from app.core.config import APP_TZ
import logging
import uuid
import concurrent.futures

router = APIRouter(prefix="/api/chat", tags=["chat"])

# Initialize the graph once (in production, consider using FastAPI lifecycle events)
graph = None
# Shared thread pool to run blocking LLM calls without hanging the main thread
_executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

logger = logging.getLogger(__name__)


def get_graph():
    global graph
    if graph is None:
        graph = build_graph()
    return graph


@router.post("/message", response_model=ChatResponseSchema)
def send_message(request: ChatSchema):
    """
    Send a message to the finance manager agent.

    The agent will process the message, extract expense info,
    categorize it, and may interact with tools for logging or analytics.
    """
    try:
        thread_id = request.thread_id or str(uuid.uuid4())
        try:
            request.thread_id = thread_id
        except Exception:
            # fallback for immutable models
            object.__setattr__(request, "thread_id", thread_id)

        app = get_graph()

        config = {
            "configurable": {
                "user_id": request.user_id,
                "thread_id": request.thread_id,
                "tz": request.tz or APP_TZ,
            }
        }

        # Run the blocking invoke in a thread with a timeout to avoid indefinite hangs
        logger.info(
            "Invoking LangGraph agent for user %s thread %s",
            request.user_id,
            request.thread_id,
        )
        future = _executor.submit(
            app.invoke, {"messages": [HumanMessage(content=request.message)]}, config
        )
        try:
            output = future.result(timeout=60)
        except concurrent.futures.TimeoutError:
            future.cancel()
            logger.error("LLM invoke timed out for user %s", request.user_id)
            raise HTTPException(status_code=504, detail="LLM request timed out")
        except Exception as e:
            logger.exception("Error during agent invoke: %s", e)
            raise HTTPException(
                status_code=500, detail=f"Error processing message: {e}"
            )

        last_msg = output["messages"][-1]
        response_content = getattr(last_msg, "content", str(last_msg))

        if isinstance(response_content, list):
            text_parts = []
            for block in response_content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
                elif isinstance(block, str):
                    text_parts.append(block)
            response_content = (
                " ".join(text_parts) if text_parts else str(response_content)
            )

        return ChatResponseSchema(
            user_id=request.user_id,
            thread_id=request.thread_id,
            user_message=request.message,
            agent_response=response_content,
            status="success",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing message: {str(e)}"
        )


@router.get("/health")
def health_check():
    """Health check endpoint to verify the chat service is running."""
    return {"status": "healthy", "service": "finance-manager-chat"}
