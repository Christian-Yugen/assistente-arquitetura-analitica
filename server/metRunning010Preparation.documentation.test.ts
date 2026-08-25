import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("MET-RUNNING-010 preparation", () => {
  it("preserves the non-executable intake, ordering-ambiguity exclusion and production block", () => {
    const intake = readFileSync(resolve(root, "artifacts/intake/MET-RUNNING-010.json"), "utf8");
    const policy = readFileSync(resolve(root, "docs/rules/MET_RUNNING_010_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/MET_RUNNING_010_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");

    expect(intake).toContain('"local_readiness": "intake_required"');
    expect(intake).toContain('"implementation_authorized": false');
    expect(policy).toContain("ordenação temporal elegível sem ambiguidade");
    expect(policy).toContain("Não autoriza perfil, classificador, registro, contrato, pipeline, allowlist");
    expect(gate).toContain("autorização específica de Chris");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
