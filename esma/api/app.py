"""
FastAPI application for ESMA SQL Agent
"""
import uuid
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from esma.config.settings import settings
from esma.agents.esma import ESMAAgent


class ChatRequest(BaseModel):
    """Request model for chat endpoints"""
    message: str = Field(..., description="User query about ENAHO or GEIH databases")
    thread_id: Optional[str] = Field(None, description="Thread ID for conversation continuity")


class ChatResponse(BaseModel):
    """Response model for non-streaming chat"""
    response: str = Field(..., description="Agent response to the query")
    thread_id: str = Field(..., description="Thread ID for this conversation")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")


agent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to initialize and cleanup resources"""
    global agent
    print("Starting up ESMA Agent...")
    print(f"Author: {settings.author}")
    agent = ESMAAgent()
    yield


app = FastAPI(
    title="ESMA SQL Agent API",
    description="API for querying ENAHO and GEIH household survey databases",
    version="1.0.0",
    lifespan=lifespan
)


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Non-streaming chat endpoint.
    Creates a new thread if thread_id is not provided.
    """
    try:
        thread_id = request.thread_id or f"esma-chat-{str(uuid.uuid4())}"        
        config = {"configurable": {"thread_id": thread_id}}
        response = await agent.ainvoke(request.message, config=config)
        
        return ChatResponse(
            response=response,
            thread_id=thread_id
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Failed to process request", "detail": str(e)}
        )


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint using Server-Sent Events.
    Creates a new thread if thread_id is not provided.
    """
    try:
        thread_id = request.thread_id or f"esma-chat-{str(uuid.uuid4())}" 
        config = {"configurable": {"thread_id": thread_id}}
        
        async def generate():
            """Generator for streaming responses"""
            async for chunk in agent.astream(request.message, config=config):
                yield f"data: {{\"type\": \"content\", \"content\": {repr(chunk)}}}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Thread-ID": thread_id
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Failed to process streaming request", "detail": str(e)}
        )


@app.post("/thread/new")
async def create_new_thread():
    """
    Create a new thread/conversation.
    Returns a new thread_id for starting a fresh conversation.
    """
    thread_id = f"esma-chat-{str(uuid.uuid4())}" 
    return {"thread_id": thread_id, "message": "New conversation thread created"}


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "ESMA SQL Agent API",
        "endpoints": {
            "/chat": "Non-streaming chat (POST)",
            "/chat/stream": "Streaming chat with SSE (POST)", 
            "/thread/new": "Create new conversation thread (POST)",
            "/docs": "Interactive API documentation"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)