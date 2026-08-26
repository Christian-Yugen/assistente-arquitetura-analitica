import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("ALT-AVGAVG-008 preparation", () => {
  it("keeps the average-of-averages policy aggregate-only, non-executable and production blocked", () => {
    const intake = readFileSync(resolve(root, "artifacts/intake/ALT-AVGAVG-008.json"), "utf8");
    const policy = readFileSync(resolve(root, "docs/rules/ALT_AVGAVG_008_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/ALT_AVGAVG_008_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");

    expect(intake).toContain('"execution_blocked": true');
    expect(intake).toContain('"implementation_authorized": false');
    expect(intake).toContain('"production_authorized": false');
    expect(policy).toContain("fonte independente, autorizada, opaca e agregada");
    expect(policy).toContain("não poderá calcular, recomputar, ponderar, comparar, corrigir ou escolher");
    expect(policy).toContain("Qualquer código executável requer uma autorização nova e explícita de Chris");
    expect(gate).toContain("não altera a contagem do workspace");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
