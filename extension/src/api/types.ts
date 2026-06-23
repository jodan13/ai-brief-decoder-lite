export type RunStatus = "running" | "succeeded" | "failed";
export type Severity = "low" | "medium" | "high";
export type SafeErrorCode = "invalid_provider_output" | "provider_error" | "run_not_found";

export interface RiskItem {
  risk: string;
  severity: Severity;
  reason: string;
}

export interface StructuredBriefResult {
  summary: string;
  goals: string[];
  deliverables: string[];
  constraints: string[];
  risks: RiskItem[];
  clarifying_questions: string[];
  recommended_next_action: string;
}

export interface DecodeRunResponse {
  run_id: string;
  status: RunStatus;
  input_text: string;
  structured_result: StructuredBriefResult | null;
  raw_provider_output: string | null;
  safe_error_code: SafeErrorCode | null;
  safe_error_message: string | null;
  created_at: string;
  updated_at: string;
}
