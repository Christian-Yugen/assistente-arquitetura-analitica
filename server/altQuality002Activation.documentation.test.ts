import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

describe("ALT-QUALITY-002 draft activation", () => {
  it("documents authorization, synthetic calibration and production block", () => {
    const root = resolve(import.meta.dirname, "..");
    const gate = readFileSync(resolve(root, "docs/gates/ALT_QUALITY_002_DRAFT_CALIBRATION_001.md"), "utf8");
    const reconstruction = readFileSync(resolve(root, "docs/gates/ALT_QUALITY_002_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");
    expect(reconstruction).toContain("sim, atutorizado");
    expect(gate).toContain("TP=1");
    expect(gate).toContain("FP=0");
    expect(gate).toContain("FN=0");
    expect(gate).toContain("contagens agregadas");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
