import { AuditResponse } from "@/types/audit";

export class ApiError extends Error {
  constructor(public status: number, message: string, public details?: unknown) {
    super(message);
    this.name = "ApiError";
  }
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function generateAudit(url: string): Promise<AuditResponse> {
  const response = await fetch(`${API_URL}/api/audit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new ApiError(
      response.status,
      errorData?.message || "An unexpected error occurred",
      errorData?.details
    );
  }

  return response.json();
}
