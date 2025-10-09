from fastapi import FastAPI

from .api import router as api_router

app = FastAPI(
    title="Proficiency API",
    version="0.0.1",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)


@app.get("/health", tags=["Health"])
async def read_health() -> dict[str, str]:
    """Basic health endpoint used for readiness probes."""
    return {"status": "ok"}


app.include_router(api_router, prefix="/api")
