import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const specificationPath = resolve(
  import.meta.dirname,
  "../artifacts/specifications/qlt-null-001-logical-spec-v0.1.0-reconstructed.1.json",
);

describe("QLT-NULL-001 reconstructed logical specification", () => {
  it("defines only aggregated inputs, deterministic decisions, boundary tests and a blocked implementation", () => {
    const specification = JSON.parse(readFileSync(specificationPath, "utf8")) as {
      status: string;
      input_profile: { prohibited_fields: string[]; derived_fields: string[] };
      decision_algorithm: string[];
      planned_test_matrix: string[];
      implementation_status: string;
      gate_id: string;
    };

    expect(specification.status).toBe("draft_for_governance_review");
    expect(specification.input_profile.prohibited_fields).toContain("raw_cell_values");
    expect(specification.input_profile.prohibited_fields).toContain("original_sheet_title");
    expect(specification.input_profile.derived_fields).toContain(
      "missing_ratio = missing_cell_count / observed_cell_count",
    );
    expect(specification.decision_algorithm.join(" ")).toContain("0.05");
    expect(specification.decision_algorithm.join(" ")).toContain("0.20");
    expect(specification.planned_test_matrix).toContain(
      "sentinel and formula expressions are excluded from missing counts",
    );
    expect(specification.implementation_status).toBe("blocked_pending_reconstruction_gate");
    expect(specification.gate_id).toBe("QLT-NULL-RECONSTRUCTION-001");
  });
});
