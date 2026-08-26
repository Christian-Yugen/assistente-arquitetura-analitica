import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("MDL-MIXED-013 activation boundaries", () => {
  it("vincula a autorização draft, o golden sintético e o pipeline fail-closed", () => {
    const intake = JSON.parse(readFileSync(resolve(root, "artifacts/intake/MDL-MIXED-013.json"), "utf8"));
    const reconstructionGate = readFileSync(resolve(root, "docs/gates/MDL_MIXED_013_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");
    const calibrationGate = readFileSync(resolve(root, "docs/gates/MDL_MIXED_013_DRAFT_CALIBRATION_001.md"), "utf8");
    const manifest = JSON.parse(readFileSync(resolve(root, "artifacts/golden/mdl-mixed-draft-golden-v1.manifest.json"), "utf8"));
    expect(intake.execution_profile).toBe("draft");
    expect(intake.authorization.implementation_authorized).toBe(true);
    expect(intake.authorization.implementation_authorization_record).toBe("Chat: Sim");
    expect(intake.production_blocked).toBe(true);
    expect(reconstructionGate).toContain("Chat: Sim");
    expect(calibrationGate).toContain("independent_mixed_table_signal_count=0");
    expect(calibrationGate).toContain("tp=1");
    expect(calibrationGate).toContain("fp=0");
    expect(calibrationGate).toContain("fn=0");
    expect(manifest.synthetic_only).toBe(true);
    expect(manifest.production_authorized).toBe(false);
  });
});
