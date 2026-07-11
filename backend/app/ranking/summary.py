from typing import List
from app.ranking.models import RankedOpportunity

class SummaryGenerator:
    @staticmethod
    def generate(
        opportunities: List[RankedOpportunity], 
        quick_wins: int, 
        long_term: int, 
        completeness_pct: int
    ) -> str:
        total = len(opportunities)
        confidence_text = "high" if completeness_pct >= 85 else ("moderate" if completeness_pct >= 50 else "low")
        
        # Format the numbers as words for small numbers if desired, but integer is fine for deterministic
        return (
            f"The audit identified {total} opportunities. "
            f"{quick_wins} are high-impact quick wins and {long_term} require longer-term implementation. "
            f"Evidence completeness was {completeness_pct}%, resulting in {confidence_text} confidence across most recommendations."
        )
