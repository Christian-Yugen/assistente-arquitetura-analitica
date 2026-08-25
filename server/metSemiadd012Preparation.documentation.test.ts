import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("MET-SEMIADD-012 preparation", () => {
  it("preserves the temporal-order exclusion and production block after the draft activation", () => {
    const intake = readFileSync(resolve(root, "artifacts/intake/MET-SEMIADD-012.json"), "utf8");
    const policy = readFileSync(resolve(root, "docs/rules/MET_SEMIADD_012_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/MET_SEMIADD_012_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");

    expect(intake).toContain('"local_readiness": "executable_draft"');
    expect(intake).toContain('"implementation_authorized": true');
    expect(policy).toContain("ordenação temporal elegível sem ambiguidade");
    expect(policy).toContain("Não autoriza perfil, classificador, registro, contrato, pipeline, allowlist");
    expect(gate).toContain("Chris registrou autorização integral");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
