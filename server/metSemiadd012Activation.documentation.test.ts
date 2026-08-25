import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("MET-SEMIADD-012 activation", () => {
  it("records Chris's draft-only authorization, individual calibration gate and production block", () => {
    const intake = readFileSync(resolve(root, "artifacts/intake/MET-SEMIADD-012.json"), "utf8");
    const reconstructionGate = readFileSync(resolve(root, "docs/gates/MET_SEMIADD_012_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");
    const calibrationGate = readFileSync(resolve(root, "docs/gates/MET_SEMIADD_012_DRAFT_CALIBRATION_001.md"), "utf8");
    const manifest = readFileSync(resolve(root, "artifacts/golden/met-semiadd-draft-golden-v1.manifest.json"), "utf8");

    expect(intake).toContain('"implementation_authorized": true');
    expect(intake).toContain('"implementation_authorized_by": "Chris"');
    expect(intake).toContain('"production_authorized": false');
    expect(reconstructionGate).toContain("Chris registrou autorização integral");
    expect(calibrationGate).toContain("TP=1");
    expect(calibrationGate).toContain("ordem temporal duplicada");
    expect(calibrationGate).toContain("Produção permanece bloqueada");
    expect(manifest).toContain('"rule_id":"MET-SEMIADD-012"');
    expect(manifest).toContain('"production_authorized":false');
  });
});
