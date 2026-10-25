import { describe, expect, it } from "vitest";
import { answerDecisionFromStoredValue, questionIdsFromDiagnostic } from "./diagnosticActions";

describe("diagnostic action contracts", () => {
  it("extracts only opaque question ids from a diagnostic payload", () => {
    expect(questionIdsFromDiagnostic({ questions: [{ question_id: "q-1" }, { question_id: 3 }, null] })).toEqual(["q-1"]);
  });

  it("accepts only the enumerated human decisions", () => {
    expect(answerDecisionFromStoredValue({ decision: "confirmed" })).toBe("confirmed");
    expect(answerDecisionFromStoredValue({ decision: "free text" })).toBeNull();
    expect(answerDecisionFromStoredValue({})).toBeNull();
  });
});
