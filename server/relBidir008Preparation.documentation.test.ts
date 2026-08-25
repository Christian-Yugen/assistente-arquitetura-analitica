import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (relativePath: string) => fs.readFileSync(path.join(root, relativePath), "utf8");

describe("REL-BIDIR-008 preparation governance", () => {
  it("records the delegated Proposal A approval and keeps the rule non-executable", () => {
    const intake = read("artifacts/intake/REL-BIDIR-008.json");
    const policy = read("docs/rules/REL_BIDIR_008_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_BIDIR_008_LOGICAL_SPEC_PROPOSAL_001.md");
    const gate = read("docs/gates/REL_BIDIR_008_RECONSTRUCTION_AUTHORIZATION_001.md");

    expect(intake).toContain('"rule_id": "REL-BIDIR-008"');
    expect(intake).toContain('"priority": "P0"');
    expect(intake).toContain('"policy_approved": true');
    expect(intake).toContain("PROPOSAL-A-APPROVAL-DELEGATION-001");
    expect(intake).toContain('"implementation_authorized": false');
    expect(intake).toContain('"execution_blocked": true');
    expect(intake).toContain("REL-BIDIR-008-RECONSTRUCTION-AUTHORIZATION-001");
    expect(policy).toContain("Proposta A — alerta conservador de revisão de filtro");
    expect(policy).toContain("não detecta nem afirma que um filtro bidirecional esteja configurado");
    expect(specification).toContain("não executável");
    expect(specification).toContain("bidirectional_filter_review_candidate");
    expect(gate).toContain("não autoriza escrever, integrar ou executar lógica da regra");
    expect(gate).toContain("Uma autorização explícita posterior de Chris");
  });

  it("preserves opaque-pair privacy, human review and the production block", () => {
    const policy = read("docs/rules/REL_BIDIR_008_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_BIDIR_008_LOGICAL_SPEC_PROPOSAL_001.md");

    expect(policy).toContain("par opaco de abas distintas");
    expect(policy).toContain("SEM-SENS-015");
    expect(policy).toContain("pergunta bloqueante");
    expect(policy).toContain("produção permanece bloqueada");
    expect(specification).toContain("devem ser descartados");
    expect(specification).toContain("não deve identificar abas, colunas, valores, posições");
    expect(specification).toContain("Produção continua bloqueada");
  });
});
