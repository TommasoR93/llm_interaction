from fastapi import (
    FastAPI,
    BackgroundTasks,
    HTTPException, 
    Depends
)

from models import *
from dependency import verify_api_key
from tasks import save_feedback

app = FastAPI(title="AI Engineer API")

#Endpoint 1

@app.get("/health", response_model=HealthResponse)
def health():
    return {
        "status" : "ok"
    }

#Endpoint 2
@app.get("/models/{model_name}", response_model=ModelResponse)
def get_model(model_name: str):
    if model_name != "gpt-5.5":
        raise HTTPException(status_code=404, detail="Model not found")
    return {
        "name": model_name,
        "provider" : "OpenAI",
        "version" : "5"
    }

#Endpoint 3

@app.get("/search")
def search(q: str, limit: int = 10):
    return {
        "query": q,
        "results": [
            "FastAPI tutorial",
            "FastAPI Docs"
        ][:limit]
    }

#Endpoint 4
@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    api_key=Depends(verify_api_key)
):

    return {
        "response":
        f"You asked: {request.prompt}",

        "model":
        request.model
    }

#Endpoint 5
@app.post(
    "/summarize",
    response_model=SummarizeResponse
)
def summarize(
    request: SummarizeRequest
):

    summary = request.text[:50]

    return {
        "summary": summary
    }

#Endpoint 6
@app.get(
    "/profile",
    response_model=ProfileResponse
)
def profile(
    api_key=Depends(verify_api_key)
):

    return {
        "id":1,
        "name":"Tommaso",
        "role":"AI Engineer"
    }

#Endpoint 7
@app.post(
    "/feedback",
    response_model=FeedbackResponse
)
def feedback(
    request: FeedbackRequest,
    background_tasks: BackgroundTasks
):

    background_tasks.add_task(
        save_feedback,
        request.message
    )


    return {
        "status":"received"
    }
