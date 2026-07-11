from typing import List
from app.llm.models import ValidatedAudit, Impact, Confidence, Effort
from app.feature_engineering.models import QualityMetrics
from app.ranking.models import RankedAudit, RankedOpportunity, RankingMetadata
from app.ranking.calculator import PriorityCalculator
from app.ranking.classifier import OpportunityClassifier
from app.ranking.scorer import OverallScorer
from app.ranking.summary import SummaryGenerator
from app.ranking.validator import RankingValidator

class RankingEngine:
    @staticmethod
    def process(audit: ValidatedAudit, metrics: QualityMetrics) -> RankedAudit:
        # 1. Calculate priority score for each opportunity
        ranked_opps: List[RankedOpportunity] = []
        for opp in audit.opportunities:
            ranked_opps.append(PriorityCalculator.process(opp))
            
        # 2. Sort by priority score with tie breakers
        # Tie breakers: Impact (high), Confidence (high), Effort (low), Original Order
        def sort_key(item_with_index):
            idx, opp = item_with_index
            return (
                opp.priority_score,
                PriorityCalculator._impact_scores[opp.impact],
                PriorityCalculator._confidence_scores[opp.confidence],
                -PriorityCalculator._effort_scores[opp.effort],
                -idx
            )
            
        enumerated_opps = list(enumerate(ranked_opps))
        enumerated_opps.sort(key=sort_key, reverse=True)
        
        sorted_opps = [opp for idx, opp in enumerated_opps]
        
        # 3. Classify Quick Wins and Long Term
        quick_wins = [o for o in sorted_opps if OpportunityClassifier.is_quick_win(o)]
        long_term = [o for o in sorted_opps if OpportunityClassifier.is_long_term(o)]
        
        # 4. Calculate Overall Score
        overall_score = OverallScorer.calculate_overall_score(
            sorted_opps, 
            metrics.evidence_completeness_score, 
            metrics.parser_success_rate
        )
        
        # 5. Build metadata
        high_priority = sum(1 for o in sorted_opps if o.priority_score >= 70)
        medium_priority = sum(1 for o in sorted_opps if 40 <= o.priority_score < 70)
        low_priority = sum(1 for o in sorted_opps if o.priority_score < 40)
        
        total = len(sorted_opps)
        avg_confidence = sum(PriorityCalculator._confidence_scores[o.confidence] for o in sorted_opps) / total if total else 0.0
        avg_effort = sum(PriorityCalculator._effort_scores[o.effort] for o in sorted_opps) / total if total else 0.0
        avg_impact = sum(PriorityCalculator._impact_scores[o.impact] for o in sorted_opps) / total if total else 0.0
        
        metadata = RankingMetadata(
            total_opportunities=total,
            high_priority=high_priority,
            medium_priority=medium_priority,
            low_priority=low_priority,
            average_confidence=avg_confidence,
            average_effort=avg_effort,
            average_impact=avg_impact,
            overall_score_formula="100 - (High Priority * 5) - (Medium Priority * 2) - ((1 - Completeness) * 20) - ((1 - Parser Success) * 20)"
        )
        
        # 6. Generate Executive Summary
        completeness_pct = int(metrics.evidence_completeness_score * 100)
        summary = SummaryGenerator.generate(sorted_opps, len(quick_wins), len(long_term), completeness_pct)
        
        # 7. Assemble final audit
        ranked_audit = RankedAudit(
            overall_score=overall_score,
            executive_summary=summary,
            quick_wins=quick_wins,
            long_term_improvements=long_term,
            ranked_opportunities=sorted_opps,
            ranking_metadata=metadata
        )
        
        # 8. Validate
        RankingValidator.validate(ranked_audit)
        
        return ranked_audit
