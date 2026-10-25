import { describe, expect, it } from "vitest";
import { getDiagnosticNextAction } from "./diagnosticNextAction";

describe("getDiagnosticNextAction", () => {
  it("prioritizes source correction over every other decision", () => {
    expect(getDiagnosticNextAction({ findingCount: 7, questionCount: 3, answers: [{ decision: "needs_business_review" }, { decision: "needs_data_correction" }] }).kind).toBe("correct_file");
  });

  it("asks for pending decisions before requesting business review", () => {
    expect(getDiagnosticNextAction({ findingCount: 1, questionCount: 2, answers: [{ decision: "needs_business_review" }] }).kind).toBe("answer_questions");
  });

  it("does not ask for a new upload when all decisions depend on business context", () => {
    const action = getDiagnosticNextAction({ findingCount: 7, questionCount: 2, answers: [{ decision: "needs_business_review" }, { decision: "needs_business_review" }] });
    expect(action.kind).toBe("business_review");
    expect(action.description).toContain("não precisa ser reenviado enquanto ele não mudar");
  });

  it("keeps the current version when no correction or business review is pending", () => {
    expect(getDiagnosticNextAction({ findingCount: 2, questionCount: 1, answers: [{ decision: "confirmed" }] }).kind).toBe("keep_current_version");
  });
});
