from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.rotas_chat import router as chat_router

# Instanciação rigorosa do framework
app = FastAPI(
    title="Nexus RAG API",
    description="High-performance RESTful API for Retrieval-Augmented Generation.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(chat_router)

@app.get("/", tags=["Health Check"])
async def health_check() -> JSONResponse:
    """
    Root endpoint to verify if the API is operational.
    Returns a strict JSON payload indicating system health.
    """
    return JSONResponse(
        content={
            "status": "online", 
            "message": "Nexus RAG API is fully operational and waiting for deployment."
        },
        status_code=200
    )