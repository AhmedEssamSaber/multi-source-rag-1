from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str

class SourceItem(BaseModel):
    source: str
    score: float

class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceItem]
    confidence: float
    confidence_label: str
