from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", summary="Service health check")
async def get_health() -> dict[str, str]:
    """Return a simple payload indicating API health."""
    return {"status": "ok"}
