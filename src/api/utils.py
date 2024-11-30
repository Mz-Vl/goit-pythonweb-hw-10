from fastapi import APIRouter

router = APIRouter(prefix="/healthcheck", tags=["healthcheck"])

@router.get("/")
async def healthcheck():
    """
    Endpoint API
    """
    return {"status": "ok", "message": "API is working"}
