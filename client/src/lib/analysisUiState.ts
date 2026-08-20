export type AnalysisUiState = "auth_loading" | "sign_in_required" | "auth_error" | "analyzing" | "success" | "ready";

export function getAnalysisUiState(input: {
  authLoading: boolean;
  isAuthenticated: boolean;
  authError: boolean;
  isAnalyzing: boolean;
  isSuccess: boolean;
}): AnalysisUiState {
  if (input.authLoading) return "auth_loading";
  if (!input.isAuthenticated) return "sign_in_required";
  if (input.authError) return "auth_error";
  if (input.isAnalyzing) return "analyzing";
  if (input.isSuccess) return "success";
  return "ready";
}
