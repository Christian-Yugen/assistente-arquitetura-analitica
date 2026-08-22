import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (relativePath: string) => fs.readFileSync(path.join(root, relativePath), "utf8");

describe("MDL-FACTNOGRAIN-019 draft governance", () => {
  it("records the authorized draft activation while keeping production blocked", () => {
    const intake = read("artifacts/intake/MDL-FACTNOGRAIN-019.json");
    const policy = read("docs/rules/MDL_FACTNOGRAIN_019_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/MDL_FACTNOGRAIN_019_LOGICAL_SPEC_PROPOSAL_001.md");
    const calibrationGate = read("docs/gates/MDL_FACTNOGRAIN_019_DRAFT_CALIBRATION_001.md");
    const mvpGate = read("docs/gates/MVP_1_0_READINESS_001.md");

    expect(intake).toContain('"status": "executable_draft"');
    expect(intake).toContain('"implementation_authorized": true');
    expect(intake).toContain('"execution_blocked": false');
    expect(policy).toContain("Proposta A");
    expect(policy).toContain("Não autoriza perfil, classificador, registro, contrato, pipeline, catálogo, teste, dataset golden, calibração ou ativação");
    expect(specification).toContain("não executável");
    expect(specification).toContain("não deduz nem escolhe granularidade");
    expect(calibrationGate).toContain("3 verdadeiros positivos, 0 falsos positivos e 0 falsos negativos");
    expect(calibrationGate).toContain("produção permanece bloqueada");
    expect(mvpGate).toContain("BLOQUEADO para MVP 1.0 produtivo");
  });

  it("preserves the approved Proposal A and reconstruction traceability", () => {
    const intake = read("artifacts/intake/MDL-FACTNOGRAIN-019.json");
    const policy = read("docs/rules/MDL_FACTNOGRAIN_019_POLICY_PROPOSAL_001.md");
    const gate = read("docs/gates/MDL_FACTNOGRAIN_019_RECONSTRUCTION_AUTHORIZATION_001.md");

    expect(intake).toContain('"policy_approved": true');
    expect(intake).toContain("MDL-FACTNOGRAIN-019-RECONSTRUCTION-AUTHORIZATION-001");
    expect(policy).toContain("Proposta A aprovada explicitamente por Chris");
    expect(gate).toContain("fact_without_defined_grain_candidate");
    expect(gate).toContain("Ele não autoriza escrever, integrar ou executar lógica da regra");
    expect(gate).toContain("produção permanece bloqueada");
  });
});
