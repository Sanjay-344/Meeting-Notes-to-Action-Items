📝 Meeting Notes to Action Items Extractor

An AI-powered application that automatically extracts actionable tasks from meeting notes and converts them into a structured format containing task descriptions, owners, deadlines, and priorities. The application leverages Large Language Models (LLMs) through Groq's Llama 3.3 70B model to streamline meeting follow-ups and improve team productivity.

🚀 Features
Extracts action items from unstructured meeting notes.
Identifies:
.Task Description
.Task Owner
.Deadline
.Priority Level
.Handles missing information gracefully.
.Returns structured JSON output.
.User-friendly Streamlit interface.
.Powered by Groq's Llama 3.3 70B model.
.Langfuse integration for monitoring and tracing LLM interactions

User enters meeting notes
            │
            ▼
     Streamlit UI
            │
            ▼
   LangChain Pipeline
            │
            ▼
    Prompt Template
            │
            ▼
 Groq Llama 3.3 70B
            │
            ▼
  JSON Output Generated
            │
            ▼
 Pydantic Validation
            │
            ▼
 Structured Action Items
            │
            ▼
   Display in Streamlit

   "The system takes unstructured meeting notes as input, uses LangChain and Groq's Llama 3.3 70B model to extract actionable tasks, validates the output using Pydantic, and presents structured action items with owners, deadlines, and priorities through an interactive Streamlit interface."
