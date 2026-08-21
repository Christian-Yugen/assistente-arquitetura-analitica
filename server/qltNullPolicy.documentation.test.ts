import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const policyPath = resolve(
  import.meta.dirname,
  "../artifacts/specifications/qlt-null-001-policy-v0.1.0-reconstructed.1.json",
);

describe("QLT-NULL-001 reconstructed policy", () => {
  it("separates deterministic missingness from sentinels and formulas while preserving the execution block", () => {
    const policy = JSON.parse(readFileSync(policyPath, "utf8")) as {
      status: string;
      missing_classes: Record<string, { included_in_missing_count: boolean }>;
      severity_thresholds: Array<{ severity: string }>;
      evidence: string[];
      implementation_status: string;
      gate_id: string;
    };

    expect(policy.status).toBe("draft_for_governance_review");
    expect(policy.missing_classes.structural_null.included_in_missing_count).toBe(true);
    expect(policy.missing_classes.blank_text.included_in_missing_count).toBe(true);
    expect(policy.missing_classes.numeric_nan.included_in_missing_count).toBe(true);
    expect(policy.missing_classes.textual_sentinel.included_in_missing_count).toBe(false);
    expect(policy.missing_classes.formula_expression.included_in_missing_count).toBe(false);
    expect(policy.severity_thresholds.map((threshold) => threshold.severity)).toEqual(["low", "medium", "high"]);
    expect(policy.evidence).toContain("EVD-NULL-MISSING-RATIO");
    expect(policy.implementation_status).toBe("blocked_pending_reconstruction_gate");
    expect(policy.gate_id).toBe("QLT-NULL-RECONSTRUCTION-001");
  });
});
