from typing import Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime
from zoneinfo import ZoneInfo
from langchain_core.tools import tool
# from google.oauth2 import service_account
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from app.config import GOOGLE_APPLICATION_CREDENTIALS_PATH

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS_PATH

CATEGORIES = ["Fuel", "Groceries", "Food & Dining", "Transport", 
              "Shopping", "Bills", "Rent", "Health", "Travel", "Other"
]

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        vertexai=True,           
        project="agenticaiprep", 
        location="us-central1",  
        temperature=0.3,
        max_output_tokens=500,
        max_retries=2,
    )


class ProcessedExpense(BaseModel):

    amount: float = Field(..., gt=0)
    currency: Literal["INR"] = "INR"
    ts: str = Field(..., description="ISO-8601 timestamp in local timezone, include offset")
    merchant: Optional[str] = Field(None, description="Merchant if explicitly mentioned (e.g., HP, Amazon)")
    description: str = Field(..., description="Short description like 'petrol', 'lunch'")
    notes: Optional[str] = None
    is_ambiguous: bool = False
    clarification_question: Optional[str] = None
    
    # Categorization fields
    category: str = Field(..., description=f"One of: {CATEGORIES}")
    category_confidence: float = Field(..., ge=0, le=1, description="Confidence score for category assignment")




@tool
def process_expense(text: str, tz: str = "Asia/Kolkata") -> dict:
    """
    Extract expense info AND categorize in a single call.
    Returns: amount, date, merchant, description, category, and confidence.
    """
    llm = get_llm()
    now = datetime.now(ZoneInfo(tz)).isoformat()

    prompt = f"""
    You extract and categorize expense info from text in ONE STEP.
    
    EXTRACTION RULES:
    - Resolve relative dates like "yesterday", "today", "last Friday" using: NOW={now} and timezone {tz}.
    - If time missing, set 12:00 local time.
    - Merchant ONLY if clearly mentioned; else null.
    - If amount missing or description unclear, set is_ambiguous=true and ask ONE clarification question.
    
    CATEGORIZATION RULES:
    - Classify into ONE category from taxonomy: {CATEGORIES}
    - Provide confidence score (0.0 to 1.0) based on how clearly the expense fits the category.
    
    Return ONLY a JSON (NO MARKDOWN SYMBOLS) matching this schema: {ProcessedExpense.model_json_schema()}
    
    Text: {text}
    """
    
    out = llm.with_structured_output(ProcessedExpense).invoke(prompt)
    resp = out.model_dump()
    return resp
