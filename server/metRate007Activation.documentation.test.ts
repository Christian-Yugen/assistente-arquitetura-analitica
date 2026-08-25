import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("MET-RATE-007 activation", () => {
  it("records Chris's draft-only authorization, the individual gate and the production block", () => {
    const intake = readFileSync(resolve(root, "artifacts/intake/MET-RATE-007.json"), "utf8");
    const reconstructionGate = readFileSync(resolve(root, "docs/gates/MET_RATE_007_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");
    const calibrationGate = readFileSync(resolve(root, "docs/gates/MET_RATE_007_DRAFT_CALIBRATION_001.md"), "utf8");
    const manifest = readFileSync(resolve(root, "artifacts/golden/met-rate-draft-golden-v1.manifest.json"), "utf8");

    expect(intake).toContain('"implementation_authorized": true');
    expect(intake).toContain('"implementation_authorized_by": "Chris"');
    expect(intake).toContain('"production_authorized": false');
    expect(reconstructionGate).toContain("sim, autorizado");
    expect(calibrationGate).toContain("TP=1, FP=0 e FN=0");
    expect(calibrationGate).toContain("Produção permanece bloqueada");
    expect(manifest).toContain('"rule_id":"MET-RATE-007"');
    expect(manifest).toContain('"production_authorized":false');
  });
});
