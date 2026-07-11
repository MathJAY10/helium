from app.ranking.models import RankedAudit

class RankingValidator:
    @staticmethod
    def validate(audit: RankedAudit) -> bool:
        # Pydantic inherently validates the ge=0 and le=100 constraints
        # on instantiation, but we provide an explicit validation step
        # as requested.
        
        if not (0 <= audit.overall_score <= 100):
            raise ValueError(f"Overall score must be 0-100, got {audit.overall_score}")
            
        for opp in audit.ranked_opportunities:
            if not (0 <= opp.priority_score <= 100):
                raise ValueError(f"Priority score must be 0-100, got {opp.priority_score}")
                
        return True
