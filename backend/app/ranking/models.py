from pydantic import BaseModel, Field
from typing import List
from app.llm.models import Opportunity

class RankedOpportunity(Opportunity):
    priority_score: int = Field(..., ge=0, le=100, description="Priority score from 0-100")

class RankingMetadata(BaseModel):
    total_opportunities: int
    high_priority: int
    medium_priority: int
    low_priority: int
    average_confidence: float
    average_effort: float
    average_impact: float
    overall_score_formula: str

class RankedAudit(BaseModel):
    overall_score: int = Field(..., ge=0, le=100)
    executive_summary: str
    quick_wins: List[RankedOpportunity]
    long_term_improvements: List[RankedOpportunity]
    ranked_opportunities: List[RankedOpportunity]
    ranking_metadata: RankingMetadata
