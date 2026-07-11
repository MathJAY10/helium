"use client";

import { useEffect, useState } from "react";
import { Skeleton } from "@/components/ui/skeleton";
import { CheckCircle2, CircleDashed } from "lucide-react";
import { cn } from "@/lib/utils";

const STEPS = [
  "Crawling Website",
  "Discovering Products",
  "Parsing HTML",
  "Extracting Features",
  "AI Reasoning",
  "Ranking Opportunities",
];

export function LoadingView() {
  const [activeStep, setActiveStep] = useState(0);

  // Fake progress animation for UX
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveStep((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 4000); // Progress every 4 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="max-w-6xl mx-auto space-y-12 animate-in fade-in duration-500">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
        {/* Progress Timeline */}
        <div className="space-y-6">
          <h2 className="text-2xl font-bold tracking-tight">Generating Audit...</h2>
          <p className="text-muted-foreground">This may take up to 60 seconds depending on store size.</p>
          
          <div className="space-y-4 pt-4">
            {STEPS.map((step, idx) => {
              const isActive = idx === activeStep;
              const isPast = idx < activeStep;
              
              return (
                <div key={idx} className={cn("flex items-center gap-4 transition-all duration-300", 
                  isActive ? "text-primary scale-105 origin-left" : 
                  isPast ? "text-muted-foreground" : "text-muted-foreground/40"
                )}>
                  {isPast ? (
                    <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                  ) : isActive ? (
                    <CircleDashed className="w-5 h-5 animate-spin" />
                  ) : (
                    <div className="w-5 h-5 rounded-full border-2 border-current opacity-20" />
                  )}
                  <span className={cn("font-medium", isActive && "font-bold")}>{step}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Skeleton Preview */}
        <div className="space-y-6 border rounded-xl p-6 bg-zinc-50/50 dark:bg-zinc-900/20">
          <div className="grid grid-cols-2 gap-4">
            <Skeleton className="h-24 w-full rounded-lg" />
            <Skeleton className="h-24 w-full rounded-lg" />
          </div>
          <Skeleton className="h-32 w-full rounded-lg" />
          <div className="space-y-4 pt-4">
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-4 w-1/2" />
            <Skeleton className="h-4 w-5/6" />
          </div>
        </div>
      </div>
    </div>
  );
}
