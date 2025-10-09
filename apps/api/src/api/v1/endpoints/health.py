from fastapi import APIRouter

from ...schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", summary="Service health check")
async def get_health() -> HealthResponse:
    """Return a simple payload indicating API health."""
    return HealthResponse(status="ok")
