import { useMutation } from "@tanstack/react-query";
import { generateAudit, ApiError } from "@/lib/api";
import { AuditResponse } from "@/types/audit";

export function useAudit() {
  return useMutation<AuditResponse, ApiError, string>({
    mutationFn: (url: string) => generateAudit(url),
  });
}
