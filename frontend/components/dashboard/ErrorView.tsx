import { ApiError } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { AlertTriangle, Globe, Clock, Bot, RefreshCcw } from "lucide-react";

interface ErrorViewProps {
  error: Error | ApiError | null;
  onRetry: () => void;
}

export function ErrorView({ error, onRetry }: ErrorViewProps) {
  let title = "An Unexpected Error Occurred";
  let description = "Please try again later or check the URL.";
  let Icon = AlertTriangle;
  
  if (error instanceof ApiError) {
    if (error.status === 422) {
      title = "Invalid URL";
      description = "The provided URL is invalid or not allowed. We do not support localhost, private IPs, or non-HTTP URLs.";
      Icon = Globe;
    } else if (error.status === 408) {
      title = "Audit Timeout";
      description = "The audit took too long to complete. Try a more specific collection or product page.";
      Icon = Clock;
    } else if (error.status === 429) {
      title = "AI Rate Limit Reached";
      description = "Gemini API limits exceeded. Please wait a moment before trying again.";
      Icon = Bot;
    } else if (error.status === 503) {
      title = "Crawler Failure";
      description = "We could not extract meaningful content from this website. It might be heavily protected or structured unusually.";
      Icon = Globe;
    } else {
      description = error.message;
    }
  } else if (error) {
    description = error.message;
  }

  return (
    <div className="flex items-center justify-center min-h-[60vh] p-4 animate-in zoom-in-95 duration-300">
      <Card className="max-w-md w-full border-red-200 dark:border-red-900/50 shadow-md">
        <CardHeader className="text-center space-y-4 pb-6">
          <div className="mx-auto w-12 h-12 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center text-red-600 dark:text-red-400">
            <Icon className="w-6 h-6" />
          </div>
          <div className="space-y-1">
            <CardTitle className="text-xl font-bold">{title}</CardTitle>
            <CardDescription className="text-base text-zinc-600 dark:text-zinc-400">
              {description}
            </CardDescription>
          </div>
        </CardHeader>
        <CardContent className="flex justify-center">
          <Button onClick={onRetry} className="gap-2">
            <RefreshCcw className="w-4 h-4" /> Try Again
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
