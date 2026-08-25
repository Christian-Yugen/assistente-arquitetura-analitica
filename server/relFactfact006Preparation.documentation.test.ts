import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (relativePath: string) => fs.readFileSync(path.join(root, relativePath), "utf8");

describe("REL-FACTFACT-006 draft governance", () => {
  it("records the controlled draft activation", () => {
    const intake = read("artifacts/intake/REL-FACTFACT-006.json");
    const policy = read("docs/rules/REL_FACTFACT_006_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_FACTFACT_006_LOGICAL_SPEC_PROPOSAL_001.md");
    const gate = read("docs/gates/REL_FACTFACT_006_RECONSTRUCTION_AUTHORIZATION_001.md");
    const calibration = read("docs/gates/REL_FACTFACT_006_DRAFT_CALIBRATION_001.md");

    expect(intake).toContain('"rule_id": "REL-FACTFACT-006"');
    expect(intake).toContain('"priority": "P0"');
    const catalog = read("engine/catalog.py");
    const pipeline = read("engine/pipeline/quality_diagnosis.py");

    expect(intake).toContain('"status": "executable_draft"');
    expect(intake).toContain('"policy_approved": true');
    expect(intake).toContain('"implementation_authorized": true');
    expect(intake).toContain('"execution_blocked": false');
    expect(intake).toContain("REL-FACTFACT-006-RECONSTRUCTION-AUTHORIZATION-001");
    expect(intake).toContain("REL-FACTFACT-006-DRAFT-CALIBRATION-001");
    expect(policy).toContain("Proposta A — alerta conservador de relacionamento direto entre fatos");
    expect(policy).toContain("não recomenda a criação de uma relação direta");
    expect(specification).toContain("não executável");
    expect(specification).toContain("direct_fact_to_fact_relationship_review_candidate");
    expect(gate).toContain("Chris aprovou explicitamente a **Proposta A**");
    expect(gate).toContain("não autoriza escrever, integrar ou executar lógica da regra");
    expect(gate).toContain("Uma autorização explícita posterior de Chris");
    expect(gate).toContain("A produção permanece bloqueada");
    expect(calibration).toContain("3 verdadeiros positivos, 0 falsos positivos e 0 falsos negativos");
    expect(calibration).toContain("a produção permanece bloqueada");
    expect(catalog).toContain('"REL-FACTFACT-006": "REL-FACTFACT-006-DRAFT-CALIBRATION-001"');
    expect(pipeline).toContain('"REL-FACTFACT-006": get_rule_execution_record("REL-FACTFACT-006").status');
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
