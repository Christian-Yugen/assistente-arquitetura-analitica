import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("MET-DOMAIN-013 draft activation", () => {
  it("preserves the authorized draft intake, opaque-domain restriction and production block", () => {
    const intake = readFileSync(resolve(root, "artifacts/intake/MET-DOMAIN-013.json"), "utf8");
    const policy = readFileSync(resolve(root, "docs/rules/MET_DOMAIN_013_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/MET_DOMAIN_013_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");

    expect(intake).toContain('"local_readiness": "executable_draft"');
    expect(intake).toContain('"implementation_authorized": true');
    expect(intake).toContain('"production_authorized": false');
    expect(policy).toContain("sinal de domínio já classificado de forma independente, opaca e agregada");
    expect(policy).toContain("Não autoriza perfil, classificador, registro, contrato, pipeline, allowlist");
    expect(gate).toContain("autorização específica de implementação");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
