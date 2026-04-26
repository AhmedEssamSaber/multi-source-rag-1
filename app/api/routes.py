from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, SourceItem

router = APIRouter()

# Injected from main.py
chatbot = None

def set_chatbot(bot):
    global chatbot
    chatbot = bot

@router.get("/")
def root():
    return {"status": "ok", "message": "Medical RAG Chatbot API is running"}

@router.get("/health")
def health():
    return {
        "status": "ok",
        "chunks_indexed": len(chatbot.store.store),
        "memory_turns":   len(chatbot.memory.get_history()) // 2
    }

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    answer, sources, confidence = chatbot.chat(request.query)

    if confidence < 0.0001:
        label = "low"
    elif confidence < 0.001:
        label = "moderate"
    else:
        label = "high"

    return ChatResponse(
        answer=answer,
        sources=[SourceItem(source=s["source"], score=s["score"]) for s in sources],
        confidence=confidence,
        confidence_label=label
    )

@router.post("/reset")
def reset_memory():
    chatbot.memory.clear()
    return {"status": "ok", "message": "Conversation memory cleared"}
