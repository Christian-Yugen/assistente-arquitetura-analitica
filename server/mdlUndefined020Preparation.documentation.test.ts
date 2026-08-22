import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (relativePath: string) => fs.readFileSync(path.join(root, relativePath), "utf8");

describe("MDL-UNDEFINED-020 preparation governance", () => {
  it("records a non-executable Proposal A with the residual classification bounded by human review", () => {
    const intake = read("artifacts/intake/MDL-UNDEFINED-020.json");
    const policy = read("docs/rules/MDL_UNDEFINED_020_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/MDL_UNDEFINED_020_LOGICAL_SPEC_PROPOSAL_001.md");

    expect(intake).toContain('"status": "reconstruction_gate_recorded"');
    expect(intake).toContain('"policy_approved": true');
    expect(intake).toContain('"policy_approved_by": "Chris"');
    expect(intake).toContain('"implementation_authorized": false');
    expect(intake).toContain('"execution_blocked": true');
    expect(intake).toContain('"draft_catalog_authorization"');
    expect(policy).toContain("table_classification_undefined_candidate");
    expect(policy).toContain("não prova");
    expect(policy).toContain("Proposta A aprovada explicitamente por Chris");
    expect(policy).toContain("Esta política não autoriza perfil, classificador, registro, versão de contrato, integração de pipeline, catálogo, testes executáveis, golden dataset, calibração ou produção");
    expect(specification).toContain("avaliados");
    expect(specification).toContain("0.60");
    expect(specification).toContain("Não há implementação autorizada");
  });

  it("keeps the rule absent from all executable surfaces until a future authorization chain is complete", () => {
    const registry = read("engine/fact_dimension/registry.py");
    const catalog = read("engine/catalog.py");
    const contracts = read("engine/contracts/diagnosis.py");
    const pipeline = read("engine/pipeline/quality_diagnosis.py");

    expect(registry).not.toContain("MDL-UNDEFINED-020");
    expect(catalog).not.toContain("MDL-UNDEFINED-020");
    expect(contracts).not.toContain("MDL-UNDEFINED-020");
    expect(pipeline).not.toContain("MDL-UNDEFINED-020");
  });

  it("records the reconstruction gate without granting implementation authorization", () => {
    const intake = read("artifacts/intake/MDL-UNDEFINED-020.json");
    const gate = read("docs/gates/MDL_UNDEFINED_020_RECONSTRUCTION_AUTHORIZATION_001.md");

    expect(intake).toContain("MDL-UNDEFINED-020-RECONSTRUCTION-AUTHORIZATION-001");
    expect(intake).toContain('"implementation_authorized": false');
    expect(gate).toContain("table_classification_undefined_candidate");
    expect(gate).toContain("Ele não autoriza escrever, integrar ou executar lógica da regra");
    expect(gate).toContain("produção permanece bloqueada");
  });
});
