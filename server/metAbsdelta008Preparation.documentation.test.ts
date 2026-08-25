import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("MET-ABSDELTA-008 preparation", () => {
  it("preserves the conservative policy scope and production block after the draft activation", () => {
    const intake = readFileSync(resolve(root, "artifacts/intake/MET-ABSDELTA-008.json"), "utf8");
    const policy = readFileSync(resolve(root, "docs/rules/MET_ABSDELTA_008_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/MET_ABSDELTA_008_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");

    expect(intake).toContain('"local_readiness": "executable_draft"');
    expect(intake).toContain('"implementation_authorized": true');
    expect(policy).toContain("não calculada");
    expect(policy).toContain("Não autoriza perfil, classificador, registro, contrato, pipeline, allowlist");
    expect(gate).toContain("Chris registrou autorização específica");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
