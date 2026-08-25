import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

describe("MET-DOMAIN-013 draft activation", () => {
  it("documenta autorização, calibração sintética, limite fail-closed e produção bloqueada", () => {
    const root = resolve(import.meta.dirname, "..");
    const gate = readFileSync(resolve(root, "docs/gates/MET_DOMAIN_013_DRAFT_CALIBRATION_001.md"), "utf8");
    const reconstruction = readFileSync(resolve(root, "docs/gates/MET_DOMAIN_013_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");
    expect(reconstruction).toContain("ok. autorizado, continue");
    expect(gate).toContain("TP=1");
    expect(gate).toContain("FP=0");
    expect(gate).toContain("FN=0");
    expect(gate).toContain("fixa o sinal de domínio em zero");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
