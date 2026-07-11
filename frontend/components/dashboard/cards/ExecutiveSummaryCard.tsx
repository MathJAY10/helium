import { RankedAudit } from "@/types/audit";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Lightbulb, Rocket, ListChecks } from "lucide-react";

interface ExecutiveSummaryCardProps {
  audit: RankedAudit;
}

export function ExecutiveSummaryCard({ audit }: ExecutiveSummaryCardProps) {
  return (
    <Card className="col-span-1 lg:col-span-3 overflow-hidden border-zinc-200 dark:border-zinc-800 shadow-sm">
      <CardHeader className="bg-zinc-50 dark:bg-zinc-900/50 border-b">
        <CardTitle className="text-lg flex items-center gap-2">
          <Lightbulb className="w-5 h-5 text-amber-500" />
          Executive Summary
        </CardTitle>
      </CardHeader>
      <CardContent className="pt-6">
        <p className="text-base leading-relaxed text-zinc-700 dark:text-zinc-300 mb-8">
          {audit.executive_summary}
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2 mb-4">
              <Rocket className="w-4 h-4 text-emerald-500" />
              Quick Wins
            </h3>
            <ul className="space-y-3">
              {audit.quick_wins.map((win, idx) => (
                <li key={idx} className="flex items-start gap-2 text-sm">
                  <div className="mt-1 h-1.5 w-1.5 rounded-full bg-emerald-500 shrink-0" />
                  <span className="leading-tight">{win}</span>
                </li>
              ))}
              {audit.quick_wins.length === 0 && (
                <li className="text-sm text-muted-foreground italic">No quick wins identified.</li>
              )}
            </ul>
          </div>
          
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2 mb-4">
              <ListChecks className="w-4 h-4 text-blue-500" />
              Long-Term Improvements
            </h3>
            <ul className="space-y-3">
              {audit.long_term_improvements.map((imp, idx) => (
                <li key={idx} className="flex items-start gap-2 text-sm">
                  <div className="mt-1 h-1.5 w-1.5 rounded-full bg-blue-500 shrink-0" />
                  <span className="leading-tight">{imp}</span>
                </li>
              ))}
              {audit.long_term_improvements.length === 0 && (
                <li className="text-sm text-muted-foreground italic">No long-term improvements identified.</li>
              )}
            </ul>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
