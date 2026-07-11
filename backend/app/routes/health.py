from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Health"])

class HealthResponse(BaseModel):
    status: str
    version: str

@router.get("/health", response_model=HealthResponse, summary="Health Check")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

@router.get("/version", response_model=HealthResponse, summary="Version")
async def version():
    return {"status": "ok", "version": "1.0.0"}
