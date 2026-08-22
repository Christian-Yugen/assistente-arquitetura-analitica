import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (relativePath: string) => fs.readFileSync(path.join(root, relativePath), "utf8");

describe("MDL-FACTNOGRAIN-019 preparation governance", () => {
  it("keeps implementation and production blocked pending specific policy approval", () => {
    const intake = read("artifacts/intake/MDL-FACTNOGRAIN-019.json");
    const policy = read("docs/rules/MDL_FACTNOGRAIN_019_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/MDL_FACTNOGRAIN_019_LOGICAL_SPEC_PROPOSAL_001.md");

    expect(intake).toContain('"execution_blocked": true');
    expect(intake).toContain('"implementation_authorized": false');
    expect(policy).toContain("Proposta A");
    expect(policy).toContain("Não autoriza perfil, classificador, registro, contrato, pipeline, catálogo, teste, dataset golden, calibração ou ativação");
    expect(specification).toContain("não executável");
    expect(specification).toContain("não deduz nem escolhe granularidade");
  });

  it("records Chris's approved Proposal A while preserving the reconstruction and implementation block", () => {
    const intake = read("artifacts/intake/MDL-FACTNOGRAIN-019.json");
    const policy = read("docs/rules/MDL_FACTNOGRAIN_019_POLICY_PROPOSAL_001.md");
    const gate = read("docs/gates/MDL_FACTNOGRAIN_019_RECONSTRUCTION_AUTHORIZATION_001.md");

    expect(intake).toContain('"policy_approved": true');
    expect(intake).toContain("policy_authorized_pending_reconstruction_gate");
    expect(policy).toContain("Proposta A aprovada explicitamente por Chris");
    expect(gate).toContain("fact_without_defined_grain_candidate");
    expect(gate).toContain("Ele não autoriza escrever, integrar ou executar lógica da regra");
    expect(gate).toContain("produção permanece bloqueada");
  });
});
