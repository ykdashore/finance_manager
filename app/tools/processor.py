from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from zoneinfo import ZoneInfo
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import re
from app.core.config import LLM_ID

# import json
# from langchain_core.messages import HumanMessage


CATEGORIES = [
    "Fuel",
    "Groceries",
    "Food & Dining",
    "Transport",
    "Shopping",
    "Bills",
    "Rent",
    "Health",
    "Travel",
    "Other",
]


def get_llm():
    return ChatGoogleGenerativeAI(
        model=LLM_ID,
        vertexai=True,
        project="agenticaiprep",
        location="us-central1",
        temperature=0.3,
        max_output_tokens=5000,
        max_retries=2,
    )


class ProcessedExpense(BaseModel):
    amount: float = Field(..., gt=0)
    currency: Literal["INR"] = "INR"
    ts: str = Field(
        ..., description="ISO-8601 timestamp in local timezone, include offset"
    )
    merchant: Optional[str] = Field(
        None, description="Merchant if explicitly mentioned (e.g., HP, Amazon)"
    )
    description: str = Field(
        ..., description="Short description like 'petrol', 'lunch'"
    )
    notes: Optional[str] = None
    is_ambiguous: bool = False
    clarification_question: Optional[str] = None

    # Categorization fields
    category: str = Field(..., description=f"One of: {CATEGORIES}")
    category_confidence: float = Field(
        ..., ge=0, le=1, description="Confidence score for category assignment"
    )

    # When the expense was made (YYYY-MM-DDTHH:MM:SS±HH:MM with complete timezone offset)
    created_at: datetime = Field(
        ...,
        description="ISO-8601 datetime when expense was made, with complete timezone offset (e.g., 2026-02-25T12:00:00+05:30)",
    )

    @field_validator("created_at", mode="before")
    @classmethod
    def fix_malformed_datetime(cls, v):
        """Fix malformed datetime strings from LLM output"""
        if isinstance(v, str):
            # Pattern: incomplete datetime like "2026-02-24T12:" or "2026-02-24T12:3" etc.
            # Complete with :00:00+05:30 if missing minutes/seconds/timezone
            match = re.match(
                r"^(\d{4}-\d{2}-\d{2}T\d{2}):?(\d{0,2})?:?(\d{0,2})?([+-]\d{2}:?\d{0,2})?(.*)$",
                v,
            )
            if match:
                date_time, minutes, seconds, tz_offset, extra = match.groups()

                # Reconstruct with defaults
                minutes = minutes if minutes else "00"
                seconds = seconds if seconds else "00"

                if tz_offset:
                    # Fix incomplete timezone like +05:3 to +05:30
                    if len(tz_offset) < 6:  # +05:3, +05, etc.
                        tz_offset = re.sub(r"([+-]\d{2}):?(\d)?$", r"\1:0\2", tz_offset)
                else:
                    tz_offset = "+05:30"  # Default to India timezone

                v = f"{date_time}:{minutes}:{seconds}{tz_offset}"

            v = re.sub(r"([+-]\d{2})(\d{2})$", r"\1:\2", v)

        return v


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
    - If date not specified, assume it's the current date in user's timezone.
    - If time missing, set 12:00 local time.
    - created_at MUST be ISO-8601 format with COMPLETE timezone offset: YYYY-MM-DDTHH:MM:SS+HH:MM (e.g., 2026-02-25T12:00:00+05:30)
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


# @tool
# def process_expense(text: str, tz: str = "Asia/Kolkata") -> dict:
#     """
#     Extract expense info AND categorize in a single call.
#     Returns: amount, date, merchant, description, category, and confidence.
#     """
#     llm = get_llm()
#     now = datetime.now(ZoneInfo(tz)).isoformat()

#     schema = ProcessedExpense.model_json_schema()

#     prompt = f"""You extract and categorize expense info from text in ONE STEP.

# EXTRACTION RULES:
# - Resolve relative dates like "yesterday", "today", "last Friday" using: NOW={now} and timezone {tz}.
# - If date not specified, assume it's the current date in user's timezone.
# - If time missing, set 12:00 local time.
# - created_at MUST be ISO-8601 format with COMPLETE timezone offset: YYYY-MM-DDTHH:MM:SS+HH:MM (e.g., 2026-02-25T12:00:00+05:30)
# - Merchant ONLY if clearly mentioned; else null.
# - If amount missing or description unclear, set is_ambiguous=true and ask ONE clarification question.

# CATEGORIZATION RULES:
# - Classify into ONE category from: {CATEGORIES}
# - Provide confidence score (0.0 to 1.0).

# OUTPUT RULES (CRITICAL):
# - Return ONLY a single raw JSON object.
# - NO markdown, NO backticks, NO code fences, NO explanation.
# - The JSON must include ALL required fields from this schema: {schema}

# Text: {text}"""

#     max_retries = 3
#     last_error = None
#     breakpoint()
#     for attempt in range(max_retries):
#         try:
#             response = llm.invoke([HumanMessage(content=prompt)])
#             raw = response.content.strip()

#             raw = re.sub(r"^```(?:json)?\s*", "", raw)
#             raw = re.sub(r"\s*```$", "", raw)
#             raw = raw.strip()

#             match = re.search(r"\{.*\}", raw, re.DOTALL)
#             if not match:
#                 raise ValueError(f"No JSON object found in response: {raw[:200]}")
#             raw = match.group()

#             data = json.loads(raw)
#             expense = ProcessedExpense(**data)  # Pydantic validates + runs field_validators
#             return expense.model_dump()

#         except (json.JSONDecodeError, ValueError) as e:
#             last_error = e
#             prompt += f"\n\nATTEMPT {attempt + 1} FAILED: {str(e)}\nFix the error and return valid JSON only."
#             continue

#     raise ValueError(f"process_expense failed after {max_retries} attempts. Last error: {last_error}")
