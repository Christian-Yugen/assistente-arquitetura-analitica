import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (relativePath: string) => fs.readFileSync(path.join(root, relativePath), "utf8");

describe("REL-CONFORMED-010 preparation governance", () => {
  it("records the delegated Proposal A approval and keeps the rule non-executable", () => {
    const intake = read("artifacts/intake/REL-CONFORMED-010.json");
    const policy = read("docs/rules/REL_CONFORMED_010_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_CONFORMED_010_LOGICAL_SPEC_PROPOSAL_001.md");
    const gate = read("docs/gates/REL_CONFORMED_010_RECONSTRUCTION_AUTHORIZATION_001.md");

    expect(intake).toContain('"rule_id": "REL-CONFORMED-010"');
    expect(intake).toContain('"priority": "P1"');
    expect(intake).toContain('"policy_approved": true');
    expect(intake).toContain("PROPOSAL-A-APPROVAL-DELEGATION-001");
    expect(intake).toContain('"implementation_authorized": false');
    expect(intake).toContain('"execution_blocked": true');
    expect(intake).toContain("REL-CONFORMED-010-RECONSTRUCTION-AUTHORIZATION-001");
    expect(policy).toContain("Proposta A — alerta conservador de dimensão compartilhada");
    expect(policy).toContain("não cria dimensão compartilhada");
    expect(specification).toContain("não executável");
    expect(specification).toContain("conformed_dimension_review_candidate");
    expect(gate).toContain("não autoriza escrever, integrar ou executar lógica da regra");
    expect(gate).toContain("Uma autorização explícita posterior de Chris");
  });

  it("preserves opaque aggregation, human review and the production block", () => {
    const policy = read("docs/rules/REL_CONFORMED_010_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_CONFORMED_010_LOGICAL_SPEC_PROPOSAL_001.md");
    const gate = read("docs/gates/REL_CONFORMED_010_RECONSTRUCTION_AUTHORIZATION_001.md");

    expect(policy).toContain("par opaco dimensão–fato");
    expect(policy).toContain("SEM-SENS-015");
    expect(policy).toContain("pergunta bloqueante");
    expect(policy).toContain("produção permanece bloqueada");
    expect(specification).toContain("descartará a lista desses IDs");
    expect(specification).toContain("não deve identificar abas, colunas, valores, posições");
    expect(gate).toContain("contar os fatos conectados");
    expect(gate).toContain("A produção permanece bloqueada");
  });
});
