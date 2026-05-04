from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.rag_pipeline import get_response

app = FastAPI(
    title="AI Chatbot",
    description="AI Customer support using RAG + LangChain + OpenAI"
)

# Allow Streamlit frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
def root():
    return {"status": "ShopEasy Chatbot API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    try:
        reply = get_response(request.message)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))