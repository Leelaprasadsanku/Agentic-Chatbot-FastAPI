from pydantic import BaseModel
from typing import List

class RequestState(BaseModel):
   model_name: str
   model_provider: str
   system_prompt: str
   messages: List[str]
   allow_search: bool
   
   
# Setup API Agent from frontend request

from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent

ALLOWED_MODEL_NAMES = ["gpt-4o-mini", "llama-3.3-70b-versatile","llama3-8b-8192", "deepseek-r1-distill-llama-70b"]

app = FastAPI(title="LangGraph AI Agent")

@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    Endpoint to handle chat requests.
    """
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name.Kindly select a valid model name."}
    if request.model_provider not in ["Groq", "OpenAI"]:
        return {"error": "Invalid model provider. Kindly select a valid model provider."}
    # Extract data from the request
    model_name = request.model_name
    model_provider = request.model_provider
    system_prompt = request.system_prompt
    messages = request.messages
    allow_search = request.allow_search

    # Call the AI agent function
    response = get_response_from_ai_agent(
        llm_id=model_name,
        query=messages,
        allow_search=allow_search,
        system_prompt=system_prompt,
        provider=model_provider
    )

    return {"response": response}

# Run the FastAPI app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)