"use client";

import { useState, useMemo } from "react";
import { AuditResponse } from "@/types/audit";
import { MetricCard } from "./cards/MetricCard";
import { ExecutiveSummaryCard } from "./cards/ExecutiveSummaryCard";
import { OpportunityCard } from "./cards/OpportunityCard";
import { PriorityChart } from "./charts/PriorityChart";
import { CategoryChart } from "./charts/CategoryChart";
import { ImpactChart } from "./charts/ImpactChart";
import { Activity, CheckCircle, FileText, Globe, Clock, Search, Filter } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface DashboardViewProps {
  data: AuditResponse;
}

export function DashboardView({ data }: DashboardViewProps) {
  const { audit, metadata } = data;
  
  const [searchQuery, setSearchQuery] = useState("");
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [activeImpact, setActiveImpact] = useState<string | null>(null);
  const [quickWinsOnly, setQuickWinsOnly] = useState(false);

  const categories = Array.from(new Set(audit.ranked_opportunities.map(o => o.category)));

  const filteredOpportunities = useMemo(() => {
    return audit.ranked_opportunities.filter((o) => {
      const matchesSearch = 
        searchQuery === "" || 
        o.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        o.evidence.toLowerCase().includes(searchQuery.toLowerCase()) ||
        o.recommendation.toLowerCase().includes(searchQuery.toLowerCase());
        
      const matchesCategory = !activeCategory || o.category === activeCategory;
      const matchesImpact = !activeImpact || o.impact === activeImpact;
      const matchesQuickWin = !quickWinsOnly || o.is_quick_win;

      return matchesSearch && matchesCategory && matchesImpact && matchesQuickWin;
    });
  }, [audit.ranked_opportunities, searchQuery, activeCategory, activeImpact, quickWinsOnly]);

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-500 pb-20">
      
      {/* Hero Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 pb-6 border-b">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">CRO Audit Results</h1>
          <a href={metadata.url} target="_blank" rel="noreferrer" className="flex items-center gap-2 text-muted-foreground hover:text-primary transition-colors">
            <Globe className="w-4 h-4" />
            <span className="font-medium underline underline-offset-4">{metadata.url}</span>
          </a>
        </div>
        <div className="flex flex-col items-end">
          <span className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">Overall Score</span>
          <span className="text-5xl font-black text-primary">{audit.overall_score.toFixed(1)}</span>
        </div>
      </div>

      {/* Top Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard 
          title="Audit Duration" 
          value={`${(metadata.duration_ms / 1000).toFixed(1)}s`} 
          icon={<Clock className="w-4 h-4" />} 
        />
        <MetricCard 
          title="Evidence Extracted" 
          value={`${(metadata.evidence_completeness * 100).toFixed(0)}%`} 
          icon={<CheckCircle className="w-4 h-4" />} 
        />
        <MetricCard 
          title="Parser Success Rate" 
          value={`${(metadata.parser_success_rate * 100).toFixed(0)}%`} 
          icon={<Activity className="w-4 h-4" />} 
        />
        <MetricCard 
          title="Total Opportunities" 
          value={audit.ranked_opportunities.length} 
          icon={<FileText className="w-4 h-4" />} 
        />
      </div>

      {/* Executive Summary */}
      <ExecutiveSummaryCard audit={audit} />

      {/* Visualizations */}
      {audit.ranked_opportunities.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <PriorityChart opportunities={audit.ranked_opportunities} />
          <CategoryChart opportunities={audit.ranked_opportunities} />
          <ImpactChart opportunities={audit.ranked_opportunities} />
        </div>
      )}

      {/* Filter and Search Section */}
      <div className="pt-8 border-t space-y-6">
        <div className="flex flex-col justify-between gap-4">
          <h2 className="text-2xl font-bold tracking-tight">Opportunities ({filteredOpportunities.length})</h2>
          
          <div className="flex flex-col md:flex-row gap-4 items-center bg-zinc-50 dark:bg-zinc-900/50 p-4 rounded-xl border">
            <div className="relative flex-1 w-full">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search titles, evidence, recommendations..."
                className="pl-9 w-full bg-background"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            
            <div className="flex items-center gap-2 flex-wrap w-full md:w-auto">
              <Filter className="w-4 h-4 text-muted-foreground hidden md:block" />
              
              <Button 
                variant={quickWinsOnly ? "default" : "outline"} 
                size="sm" 
                onClick={() => setQuickWinsOnly(!quickWinsOnly)}
                className="h-9"
              >
                Quick Wins
              </Button>
              
              <select 
                className="h-9 rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                value={activeImpact || ""}
                onChange={(e) => setActiveImpact(e.target.value || null)}
              >
                <option value="">All Impacts</option>
                <option value="HIGH">High Impact</option>
                <option value="MEDIUM">Medium Impact</option>
                <option value="LOW">Low Impact</option>
              </select>

              <select 
                className="h-9 rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                value={activeCategory || ""}
                onChange={(e) => setActiveCategory(e.target.value || null)}
              >
                <option value="">All Categories</option>
                {categories.map(c => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>
          </div>
        </div>

        {/* Opportunity List */}
        <div className="space-y-6">
          {filteredOpportunities.length > 0 ? (
            filteredOpportunities.map((opp, idx) => (
              <OpportunityCard key={idx} opportunity={opp} />
            ))
          ) : (
            <div className="text-center py-20 border rounded-xl border-dashed bg-zinc-50 dark:bg-zinc-900/20">
              <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-50">Excellent!</h3>
              <p className="text-muted-foreground mt-2">No major CRO opportunities match your filters.</p>
              {(searchQuery || activeCategory || activeImpact || quickWinsOnly) && (
                <Button variant="link" onClick={() => {
                  setSearchQuery("");
                  setActiveCategory(null);
                  setActiveImpact(null);
                  setQuickWinsOnly(false);
                }}>
                  Clear all filters
                </Button>
              )}
            </div>
          )}
        </div>
      </div>

    </div>
  );
}
