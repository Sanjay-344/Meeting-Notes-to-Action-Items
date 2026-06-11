from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langfuse.langchain import CallbackHandler
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os
import json

load_dotenv()


langfuse_handler = CallbackHandler()

# ── Pydantic models ────────────────────────────────────────────────────────────

class ActionItem(BaseModel):
    task: str
    owner: str
    deadline: str
    priority: str


class ActionItems(BaseModel):
    actions: List[ActionItem]


# ── Prompt ─────────────────────────────────────────────────────────────────────

_template = """
You are an AI assistant that extracts action items from meeting notes.

Rules:
1. Extract only explicitly mentioned information.
2. Do NOT guess missing values.
3. If owner is missing, return "not_available".
4. If deadline is missing, return "not_available".
5. Assign priority:
   - High   → if deadline exists
   - Medium → normal tasks
   - Low    → optional tasks

IMPORTANT:
- Return ONLY valid JSON.
- Do NOT use markdown or ```json blocks.
- Use this exact schema:

{{
  "actions": [
    {{
      "task": "string",
      "owner": "string",
      "deadline": "string",
      "priority": "string"
    }}
  ]
}}

Meeting Notes:
{meeting_notes}
"""

prompt = PromptTemplate(
    input_variables=["meeting_notes"],
    template=_template,
)

# ── LLM ────────────────────────────────────────────────────────────────────────

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0,
)

# ── Chain (prompt | llm | str parser) ─────────────────────────────────────────

chain = prompt | llm | StrOutputParser()

# ── Public function ────────────────────────────────────────────────────────────

def extract_action_items(meeting_notes: str) -> dict:
    """
    Run the chain and return a validated dict of action items.
    Every invocation is traced in Langfuse via the callback handler.
    """
    raw: str = chain.invoke(
        {"meeting_notes": meeting_notes},
        config={"callbacks": [langfuse_handler]},
    )

    try:
        cleaned = raw.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(cleaned)

        # Normalise key: action_items → actions
        if "action_items" in parsed:
            parsed["actions"] = parsed.pop("action_items")

        validated = ActionItems(**parsed)
        return validated.dict()

    except Exception as e:
        return {
            "error": str(e),
            "raw_output": raw,
        }
