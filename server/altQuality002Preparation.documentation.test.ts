import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("ALT-QUALITY-002 draft activation", () => {
  it("preserves authorized aggregated policy and production block", () => {
    const intake = readFileSync(resolve(root, "artifacts/intake/ALT-QUALITY-002.json"), "utf8");
    const policy = readFileSync(resolve(root, "docs/rules/ALT_QUALITY_002_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/ALT_QUALITY_002_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");
    expect(intake).toContain('"local_readiness": "executable_draft"');
    expect(intake).toContain('"implementation_authorized": true');
    expect(policy).toContain("ao menos três findings de qualidade de severidade alta");
    expect(policy).toContain("não exibirá planilha, coluna, cabeçalho, valor, posição, frequência, pares ou identificadores");
    expect(gate).toContain("sim, atutorizado");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
