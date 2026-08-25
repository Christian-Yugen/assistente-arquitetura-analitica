import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (relativePath: string) => fs.readFileSync(path.join(root, relativePath), "utf8");

describe("REL-AMBIG-007 preparation governance", () => {
  it("records the official intake and keeps the rule non-executable", () => {
    const intake = read("artifacts/intake/REL-AMBIG-007.json");
    const policy = read("docs/rules/REL_AMBIG_007_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_AMBIG_007_LOGICAL_SPEC_PROPOSAL_001.md");
    const gate = read("docs/gates/REL_AMBIG_007_RECONSTRUCTION_AUTHORIZATION_001.md");

    expect(intake).toContain('"rule_id": "REL-AMBIG-007"');
    expect(intake).toContain('"priority": "P0"');
    expect(intake).toContain('"status": "intake_required"');
    expect(intake).toContain('"policy_approved": true');
    expect(intake).toContain('"implementation_authorized": false');
    expect(intake).toContain('"execution_blocked": true');
    expect(intake).toContain("REL-AMBIG-007-RECONSTRUCTION-AUTHORIZATION-001");
    expect(policy).toContain("Proposta A — alerta conservador de direções candidatas concorrentes");
    expect(policy).toContain("não detecta caminhos existentes em um modelo Power BI");
    expect(specification).toContain("não executável");
    expect(specification).toContain("ambiguous_relationship_path_review_candidate");
    expect(gate).toContain("PROPOSAL-A-APPROVAL-DELEGATION-001");
    expect(gate).toContain("não autoriza escrever, integrar ou executar lógica da regra");
    expect(gate).toContain("Uma autorização explícita posterior de Chris");
    expect(gate).toContain("A produção permanece bloqueada");
  });

  it("preserves opaque-pair privacy, human review and the production block", () => {
    const policy = read("docs/rules/REL_AMBIG_007_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_AMBIG_007_LOGICAL_SPEC_PROPOSAL_001.md");

    expect(policy).toContain("par opaco de abas distintas");
    expect(policy).toContain("SEM-SENS-015");
    expect(policy).toContain("pergunta bloqueante");
    expect(policy).toContain("produção permanece bloqueada");
    expect(specification).toContain("devem ser descartados");
    expect(specification).toContain("não deve identificar abas, colunas, valores, posições");
    expect(specification).toContain("Produção continua bloqueada");
  });
});
