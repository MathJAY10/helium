"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, Zap, Cpu, Target, ArrowRight } from "lucide-react";

interface LandingViewProps {
  onGenerate: (url: string) => void;
}

export function LandingView({ onGenerate }: LandingViewProps) {
  const [url, setUrl] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (url) onGenerate(url);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] px-4 max-w-4xl mx-auto text-center space-y-12">
      <div className="space-y-6">
        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-zinc-900 dark:text-zinc-50">
          Shopify CRO Opportunity Engine
        </h1>
        <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
          Generate evidence-backed CRO recommendations using AI. Stop guessing, start converting.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="w-full max-w-xl mx-auto space-y-4">
        <div className="relative flex items-center shadow-sm rounded-lg">
          <div className="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none text-muted-foreground">
            <Search className="h-5 w-5" />
          </div>
          <Input
            type="url"
            required
            placeholder="https://your-shopify-store.com"
            className="pl-12 pr-4 py-6 text-lg border-2 border-zinc-200 dark:border-zinc-800 rounded-lg w-full focus-visible:ring-primary focus-visible:border-primary transition-all"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
        </div>
        <div className="flex flex-col sm:flex-row gap-3 pt-2">
          <Button type="submit" size="lg" className="w-full sm:w-2/3 h-12 text-base font-semibold group">
            Generate Audit
            <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
          </Button>
          <Button 
            type="button" 
            variant="outline" 
            size="lg" 
            className="w-full sm:w-1/3 h-12 text-base"
            onClick={() => {
              setUrl("https://gymshark.com");
              onGenerate("https://gymshark.com");
            }}
          >
            Sample URL
          </Button>
        </div>
      </form>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 pt-12 border-t w-full max-w-3xl mx-auto text-sm text-muted-foreground font-medium">
        <div className="flex items-center justify-center gap-2">
          <Zap className="h-4 w-4 text-amber-500" /> Evidence Based
        </div>
        <div className="flex items-center justify-center gap-2">
          <Target className="h-4 w-4 text-emerald-500" /> Deterministic
        </div>
        <div className="flex items-center justify-center gap-2">
          <Cpu className="h-4 w-4 text-blue-500" /> AI Recommendations
        </div>
        <div className="flex items-center justify-center gap-2">
          <Search className="h-4 w-4 text-indigo-500" /> Priority Ranking
        </div>
      </div>
    </div>
  );
}
