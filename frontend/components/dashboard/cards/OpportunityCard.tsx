import { RankedOpportunity } from "@/types/audit";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Zap, Target, BarChart, Image as ImageIcon } from "lucide-react";

interface OpportunityCardProps {
  opportunity: RankedOpportunity;
}

export function OpportunityCard({ opportunity }: OpportunityCardProps) {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-3 border-b">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="text-xs uppercase tracking-wider">
                {opportunity.category}
              </Badge>
              {opportunity.is_quick_win && (
                <Badge className="bg-amber-100 text-amber-800 hover:bg-amber-100 hover:text-amber-800 border-none flex items-center gap-1">
                  <Zap className="w-3 h-3" /> Quick Win
                </Badge>
              )}
              {!opportunity.is_quick_win && (
                <Badge variant="secondary" className="flex items-center gap-1">
                  <Target className="w-3 h-3" /> Long Term
                </Badge>
              )}
            </div>
            <CardTitle className="text-xl leading-tight pt-1">
              {opportunity.title}
            </CardTitle>
          </div>
          <div className="flex flex-col items-end shrink-0">
            <span className="text-sm text-muted-foreground font-medium uppercase tracking-wider">Priority Score</span>
            <span className="text-3xl font-black text-primary">{opportunity.priority_score.toFixed(1)}</span>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pt-6 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-muted-foreground flex items-center gap-2">
              <Target className="w-4 h-4" /> The Problem
            </h4>
            <p className="text-sm leading-relaxed">{opportunity.problem}</p>
          </div>
          
          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-muted-foreground flex items-center gap-2">
              <BarChart className="w-4 h-4" /> The Evidence
            </h4>
            <p className="text-sm leading-relaxed bg-zinc-50 dark:bg-zinc-900 p-3 rounded-md border text-zinc-700 dark:text-zinc-300">
              {opportunity.evidence}
            </p>
          </div>
        </div>

        <div className="space-y-2">
          <h4 className="text-sm font-semibold text-muted-foreground">Recommendation</h4>
          <p className="text-base font-medium">{opportunity.recommendation}</p>
        </div>

        <div className="space-y-2">
          <h4 className="text-sm font-semibold text-muted-foreground">Experiment Hypothesis</h4>
          <p className="text-sm italic border-l-2 border-primary pl-4 py-1 text-muted-foreground">
            {opportunity.experiment_hypothesis}
          </p>
        </div>

        <div className="flex flex-wrap gap-4 pt-2 border-t mt-4">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-muted-foreground uppercase">Impact</span>
            <Badge variant={opportunity.impact === "HIGH" ? "default" : opportunity.impact === "MEDIUM" ? "secondary" : "outline"}>
              {opportunity.impact}
            </Badge>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-muted-foreground uppercase">Confidence</span>
            <Badge variant={opportunity.confidence === "HIGH" ? "default" : opportunity.confidence === "MEDIUM" ? "secondary" : "outline"}>
              {opportunity.confidence}
            </Badge>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-muted-foreground uppercase">Effort</span>
            <Badge variant={opportunity.effort === "LOW" ? "default" : opportunity.effort === "MEDIUM" ? "secondary" : "outline"}>
              {opportunity.effort}
            </Badge>
          </div>
          
          {opportunity.screenshot_path && (
            <div className="ml-auto">
              <a href={opportunity.screenshot_path} target="_blank" rel="noreferrer" className="text-xs font-medium flex items-center gap-1 text-blue-600 hover:text-blue-800 transition-colors">
                <ImageIcon className="w-4 h-4" /> View Evidence Screenshot
              </a>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
