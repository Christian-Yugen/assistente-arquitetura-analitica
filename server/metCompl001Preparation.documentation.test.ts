import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (relativePath: string) => fs.readFileSync(path.join(root, relativePath), "utf8");

describe("MET-COMPL-001 preparation governance", () => {
  it("reconciles the reference catalog entry and keeps local execution blocked", () => {
    const intake = read("artifacts/intake/MET-COMPL-001.json");
    const policy = read("docs/rules/MET_COMPL_001_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/MET_COMPL_001_LOGICAL_SPEC_PROPOSAL_001.md");
    const gate = read("docs/gates/MET_COMPL_001_RECONSTRUCTION_AUTHORIZATION_001.md");

    expect(intake).toContain('"source_implementation_status": "reference_implemented_draft"');
    expect(intake).toContain('"local_readiness": "intake_required"');
    expect(intake).toContain('"policy_approved": true');
    expect(intake).toContain("PROPOSAL-A-APPROVAL-DELEGATION-001");
    expect(intake).toContain('"implementation_authorized": false');
    expect(intake).toContain('"execution_blocked": true');
    expect(policy).toContain("não calcula percentual");
    expect(policy).toContain("não produz DAX");
    expect(specification).toContain("não executável");
    expect(specification).toContain("completion_rate_conceptual_metric_candidate");
    expect(gate).toContain("não autoriza escrever, integrar ou executar lógica da regra");
    expect(gate).toContain("Uma autorização explícita posterior de Chris");
  });

  it("preserves human definition, privacy and the production block", () => {
    const policy = read("docs/rules/MET_COMPL_001_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/MET_COMPL_001_LOGICAL_SPEC_PROPOSAL_001.md");
    const gate = read("docs/gates/MET_COMPL_001_RECONSTRUCTION_AUTHORIZATION_001.md");

    expect(policy).toContain("Quais estados contam como concluídos");
    expect(policy).toContain("SEM-SENS-015");
    expect(policy).toContain("produção permanece bloqueada");
    expect(specification).toContain("não deve conter valores, nomes, cabeçalhos, posições");
    expect(gate).toContain("sem gerar DAX");
    expect(gate).toContain("A produção permanece bloqueada");
  });
});
