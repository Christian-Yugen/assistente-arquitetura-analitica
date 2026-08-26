import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("ALT-SUMPCT-007 preparation", () => {
  it("preserves the aggregate-only authorization and production block", () => {
    const intake = readFileSync(resolve(root, "artifacts/intake/ALT-SUMPCT-007.json"), "utf8");
    const policy = readFileSync(resolve(root, "docs/rules/ALT_SUMPCT_007_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/ALT_SUMPCT_007_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");

    expect(intake).toContain('"execution_profile": "draft"');
    expect(intake).toContain('"implementation_authorized": true');
    expect(intake).toContain('"production_authorized": false');
    expect(policy).toContain("fonte independente, autorizada, opaca e agregada");
    expect(policy).toContain("não poderá calcular, somar, comparar, corrigir, ponderar ou escolher");
    expect(policy).toContain("Qualquer código executável requer uma autorização nova e explícita de Chris");
    expect(gate).toContain("sim, aprovado vamos acelerar que eu quero colocar esse projeto em produção");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
