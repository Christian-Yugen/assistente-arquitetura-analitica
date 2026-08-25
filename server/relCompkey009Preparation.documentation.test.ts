import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (relativePath: string) => fs.readFileSync(path.join(root, relativePath), "utf8");

describe("REL-COMPKEY-009 preparation governance", () => {
  it("records the delegated Proposal A approval and keeps the rule non-executable", () => {
    const intake = read("artifacts/intake/REL-COMPKEY-009.json");
    const policy = read("docs/rules/REL_COMPKEY_009_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_COMPKEY_009_LOGICAL_SPEC_PROPOSAL_001.md");
    const gate = read("docs/gates/REL_COMPKEY_009_RECONSTRUCTION_AUTHORIZATION_001.md");

    expect(intake).toContain('"rule_id": "REL-COMPKEY-009"');
    expect(intake).toContain('"priority": "P1"');
    expect(intake).toContain('"policy_approved": true');
    expect(intake).toContain("PROPOSAL-A-APPROVAL-DELEGATION-001");
    expect(intake).toContain('"implementation_authorized": false');
    expect(intake).toContain('"execution_blocked": true');
    expect(intake).toContain("REL-COMPKEY-009-RECONSTRUCTION-AUTHORIZATION-001");
    expect(policy).toContain("Proposta A — alerta conservador de chave composta");
    expect(policy).toContain("não concatena colunas");
    expect(specification).toContain("não executável");
    expect(specification).toContain("composite_relationship_key_review_candidate");
    expect(gate).toContain("não autoriza escrever, integrar ou executar lógica da regra");
    expect(gate).toContain("Uma autorização explícita posterior de Chris");
  });

  it("preserves opaque composite privacy, human review and the production block", () => {
    const policy = read("docs/rules/REL_COMPKEY_009_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_COMPKEY_009_LOGICAL_SPEC_PROPOSAL_001.md");
    const gate = read("docs/gates/REL_COMPKEY_009_RECONSTRUCTION_AUTHORIZATION_001.md");

    expect(policy).toContain("par opaco de abas distintas");
    expect(policy).toContain("SEM-SENS-015");
    expect(policy).toContain("pergunta bloqueante");
    expect(policy).toContain("produção permanece bloqueada");
    expect(specification).toContain("devem ser descartadas");
    expect(specification).toContain("não deve identificar abas, colunas, valores, posições");
    expect(gate).toContain("assinaturas transitórias");
    expect(gate).toContain("A produção permanece bloqueada");
  });
});
