"use client";

import { useAudit } from "@/hooks/useAudit";
import { LandingView } from "@/components/dashboard/LandingView";
import { LoadingView } from "@/components/dashboard/LoadingView";
import { DashboardView } from "@/components/dashboard/DashboardView";
import { ErrorView } from "@/components/dashboard/ErrorView";
import { useState } from "react";

export default function Home() {
  const { mutate, data, isPending, error, isError, reset } = useAudit();
  const [hasStarted, setHasStarted] = useState(false);

  const handleGenerate = (url: string) => {
    setHasStarted(true);
    mutate(url);
  };

  const handleRetry = () => {
    setHasStarted(false);
    reset();
  };

  return (
    <main className="min-h-screen p-4 md:p-8 lg:p-12 transition-all duration-500">
      {!hasStarted && !isPending && !data && !isError && (
        <LandingView onGenerate={handleGenerate} />
      )}
      
      {isPending && (
        <LoadingView />
      )}
      
      {isError && (
        <ErrorView error={error} onRetry={handleRetry} />
      )}

      {data && !isPending && !isError && (
        <DashboardView data={data} />
      )}
    </main>
  );
}
