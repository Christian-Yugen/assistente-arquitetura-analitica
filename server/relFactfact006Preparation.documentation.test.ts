import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (relativePath: string) => fs.readFileSync(path.join(root, relativePath), "utf8");

describe("REL-FACTFACT-006 preparation governance", () => {
  it("records the official intake and keeps the rule non-executable", () => {
    const intake = read("artifacts/intake/REL-FACTFACT-006.json");
    const policy = read("docs/rules/REL_FACTFACT_006_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_FACTFACT_006_LOGICAL_SPEC_PROPOSAL_001.md");

    expect(intake).toContain('"rule_id": "REL-FACTFACT-006"');
    expect(intake).toContain('"priority": "P0"');
    expect(intake).toContain('"status": "intake_required"');
    expect(intake).toContain('"implementation_authorized": false');
    expect(intake).toContain('"execution_blocked": true');
    expect(intake).toContain("REL-FACTFACT-006-RECONSTRUCTION-AUTHORIZATION-001");
    expect(policy).toContain("Proposta A — alerta conservador de relacionamento direto entre fatos");
    expect(policy).toContain("não recomenda a criação de uma relação direta");
    expect(specification).toContain("não executável");
    expect(specification).toContain("direct_fact_to_fact_relationship_review_candidate");
  });

  it("preserves opaque-pair privacy, human review and the production block", () => {
    const policy = read("docs/rules/REL_FACTFACT_006_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_FACTFACT_006_LOGICAL_SPEC_PROPOSAL_001.md");

    expect(policy).toContain("par opaco de abas distintas");
    expect(policy).toContain("SEM-SENS-015");
    expect(policy).toContain("pergunta bloqueante");
    expect(policy).toContain("produção, que permanece bloqueado");
    expect(specification).toContain("devem ser descartados");
    expect(specification).toContain("não deve identificar abas, colunas, valores, posições");
    expect(specification).toContain("Produção continua bloqueada");
  });
});
