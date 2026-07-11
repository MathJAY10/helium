from app.llm.models import Impact, Effort
from app.ranking.models import RankedOpportunity

class OpportunityClassifier:
    @staticmethod
    def is_quick_win(opp: RankedOpportunity) -> bool:
        # Quick Win if Impact >= HIGH AND Effort == LOW
        # For Enums, Impact >= HIGH means Impact == HIGH
        return opp.impact == Impact.HIGH and opp.effort == Effort.LOW

    @staticmethod
    def is_long_term(opp: RankedOpportunity) -> bool:
        # Long Term if Effort == HIGH
        return opp.effort == Effort.HIGH
