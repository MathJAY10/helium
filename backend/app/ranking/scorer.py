from typing import List
from app.ranking.models import RankedOpportunity

class OverallScorer:
    @staticmethod
    def calculate_overall_score(
        opportunities: List[RankedOpportunity], 
        evidence_completeness_score: float, 
        parser_success_rate: float
    ) -> int:
        score = 100.0
        
        high_priority_issues = sum(1 for opp in opportunities if opp.priority_score >= 70)
        medium_priority_issues = sum(1 for opp in opportunities if 40 <= opp.priority_score < 70)
        
        # Penalties
        score -= (high_priority_issues * 5)
        score -= (medium_priority_issues * 2)
        
        # Scale penalties by evidence completeness and parser success
        # E.g. If evidence completeness is 90%, we might subtract 10 points for missing evidence
        evidence_penalty = (1.0 - evidence_completeness_score) * 20 # Up to 20 points penalty for incomplete evidence
        score -= evidence_penalty
        
        parser_penalty = (1.0 - parser_success_rate) * 20 # Up to 20 points penalty for parser failures
        score -= parser_penalty
        
        return max(0, min(100, int(round(score))))
