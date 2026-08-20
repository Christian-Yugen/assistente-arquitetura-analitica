import { describe, expect, it } from "vitest";
import { getAnalysisUiState } from "./analysisUiState";

describe("getAnalysisUiState", () => {
  it("prioritizes authentication states before mutation states", () => {
    expect(getAnalysisUiState({ authLoading: true, isAuthenticated: false, authError: false, isAnalyzing: true, isSuccess: false })).toBe("auth_loading");
    expect(getAnalysisUiState({ authLoading: false, isAuthenticated: false, authError: false, isAnalyzing: false, isSuccess: false })).toBe("sign_in_required");
    expect(getAnalysisUiState({ authLoading: false, isAuthenticated: true, authError: true, isAnalyzing: false, isSuccess: false })).toBe("auth_error");
  });

  it("represents ready, pending and successful analysis mutations", () => {
    expect(getAnalysisUiState({ authLoading: false, isAuthenticated: true, authError: false, isAnalyzing: false, isSuccess: false })).toBe("ready");
    expect(getAnalysisUiState({ authLoading: false, isAuthenticated: true, authError: false, isAnalyzing: true, isSuccess: false })).toBe("analyzing");
    expect(getAnalysisUiState({ authLoading: false, isAuthenticated: true, authError: false, isAnalyzing: false, isSuccess: true })).toBe("success");
  });
});
