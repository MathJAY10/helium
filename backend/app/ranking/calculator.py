from app.llm.models import Opportunity, Impact, Confidence, Effort
from app.ranking.models import RankedOpportunity

class PriorityCalculator:
    _impact_scores = {Impact.HIGH: 5, Impact.MEDIUM: 3, Impact.LOW: 1}
    _confidence_scores = {Confidence.HIGH: 5, Confidence.MEDIUM: 3, Confidence.LOW: 1}
    _effort_scores = {Effort.HIGH: 5, Effort.MEDIUM: 3, Effort.LOW: 1}

    @classmethod
    def calculate_priority_score(cls, opportunity: Opportunity) -> int:
        i = cls._impact_scores[opportunity.impact]
        c = cls._confidence_scores[opportunity.confidence]
        e = cls._effort_scores[opportunity.effort]
        
        # Priority Score = (Impact × Confidence × 20) / Effort
        raw_score = round((i * c * 20) / e)
        
        # Ensure it fits the 0-100 constraint
        return max(0, min(100, raw_score))

    @classmethod
    def process(cls, opportunity: Opportunity) -> RankedOpportunity:
        score = cls.calculate_priority_score(opportunity)
        data = opportunity.model_dump()
        data["priority_score"] = score
        return RankedOpportunity(**data)
