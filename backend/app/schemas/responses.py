from pydantic import BaseModel
from app.ranking.models import RankedAudit

class AuditMetadata(BaseModel):
    url: str
    duration_ms: int
    evidence_completeness: float
    parser_success_rate: float

class AuditResponse(BaseModel):
    audit: RankedAudit
    metadata: AuditMetadata
