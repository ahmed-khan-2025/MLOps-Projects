from fastapi import APIRouter


router = APIRouter(
    prefix="/api",
    tags=["Health"],
)


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "industrial-ai-monitoring-platform",
    }