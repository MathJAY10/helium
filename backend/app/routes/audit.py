from fastapi import APIRouter, Depends, Request
from app.schemas.requests import AuditRequest
from app.schemas.responses import AuditResponse
from app.services.audit_service import AuditService
from app.utils.config import Settings, get_settings

router = APIRouter(prefix="/api/audit", tags=["Audit"])

@router.post(
    "",
    response_model=AuditResponse,
    summary="Generate CRO Audit",
    description="Crawls a Shopify store, extracts features, performs LLM reasoning, and returns a prioritized CRO audit.",
    responses={
        200: {"description": "Audit successfully generated"},
        400: {"description": "Invalid URL"},
        408: {"description": "Timeout"},
        422: {"description": "Validation Error"},
        429: {"description": "Gemini Rate Limit"},
        500: {"description": "Unexpected Error"},
        503: {"description": "Crawler Failure"}
    }
)
async def generate_audit(
    payload: AuditRequest, 
    request: Request,
    settings: Settings = Depends(get_settings)
) -> AuditResponse:
    request_id = getattr(request.state, "request_id", "unknown")
    service = AuditService(settings)
    
    # We use await here; the entire orchestrator pipeline is async-compatible
    # In a fully productionized system, long-running tasks might be pushed to a queue.
    # Per instructions: "Do NOT use Celery. Everything runs synchronously."
    return await service.run_audit(str(payload.url), request_id)
