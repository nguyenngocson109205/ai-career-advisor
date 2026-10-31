from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.agent.runner import run_agent
app = FastAPI(title="Mini Tool Calling Agent")


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1)
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    session_id: str
    answer: str

"""
Chat with agent 
path: /chat
method: post
body{
    message: str
    sesstion_id: str
}
"""

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = run_agent(
        question = request.message,
        session_id = request.session_id
    )
    return ChatResponse(
        session_id= request.session_id,
        answer=answer
    )