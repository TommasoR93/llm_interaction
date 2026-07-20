from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str

class ModelResponse(BaseModel):
    name: str
    provider: str
    version: str

class ChatRequest(BaseModel):
    prompt: str
    model: str

class ChatResponse(BaseModel):
    response: str
    model: str

class SummarizeRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    summary: str

class ProfileResponse(BaseModel):
    id: str
    name: str
    role: str

class FeedbackRequest(BaseModel):
    message: str
    rating: int

class FeedbackResponse(BaseModel):
    status: str

