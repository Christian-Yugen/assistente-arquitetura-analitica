import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

describe("MET-DAX-015 draft activation", () => {
  it("documents authorization, synthetic calibration, fail-closed pipeline and production block", () => {
    const root = resolve(import.meta.dirname, "..");
    const gate = readFileSync(resolve(root, "docs/gates/MET_DAX_015_DRAFT_CALIBRATION_001.md"), "utf8");
    const reconstruction = readFileSync(resolve(root, "docs/gates/MET_DAX_015_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");
    expect(reconstruction).toContain("autorização de implementação");
    expect(gate).toContain("TP=1");
    expect(gate).toContain("FP=0");
    expect(gate).toContain("FN=0");
    expect(gate).toContain("permanece fail-closed");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
