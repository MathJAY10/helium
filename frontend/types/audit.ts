export type PriorityLevel = "HIGH" | "MEDIUM" | "LOW";

export interface RankingMetadata {
  impact_score: number;
  confidence_score: number;
  effort_penalty: number;
  priority_score: number;
}

export interface RankedOpportunity {
  title: string;
  category: string;
  problem: string;
  evidence: string;
  recommendation: string;
  impact: string;
  confidence: string;
  effort: string;
  experiment_hypothesis: string;
  screenshot_path: string | null;
  priority_score: number;
  ranking_metadata: RankingMetadata;
  is_quick_win: boolean;
}

export interface RankedAudit {
  overall_score: number;
  executive_summary: string;
  quick_wins: string[];
  long_term_improvements: string[];
  ranked_opportunities: RankedOpportunity[];
}

export interface AuditResponse {
  audit: RankedAudit;
  metadata: {
    url: string;
    duration_ms: number;
    pages_crawled: number;
    evidence_completeness: number;
    parser_success_rate: number;
  };
}
