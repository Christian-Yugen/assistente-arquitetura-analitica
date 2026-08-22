import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (relativePath: string) => fs.readFileSync(path.join(root, relativePath), "utf8");

describe("MDL-UNDEFINED-020 draft governance", () => {
  it("records the approved policy, reconstruction chain and calibration gate for controlled draft execution", () => {
    const intake = read("artifacts/intake/MDL-UNDEFINED-020.json");
    const policy = read("docs/rules/MDL_UNDEFINED_020_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/MDL_UNDEFINED_020_LOGICAL_SPEC_PROPOSAL_001.md");
    const gate = read("docs/gates/MDL_UNDEFINED_020_DRAFT_CALIBRATION_001.md");

    expect(intake).toContain('"status": "executable_draft"');
    expect(intake).toContain('"policy_approved": true');
    expect(intake).toContain('"implementation_authorized": true');
    expect(intake).toContain('"calibration_gate": "MDL-UNDEFINED-020-DRAFT-CALIBRATION-001"');
    expect(intake).toContain('"missing_before_execution": []');
    expect(policy).toContain("table_classification_undefined_candidate");
    expect(policy).toContain("não prova");
    expect(specification).toContain("0.60");
    expect(gate).toContain("3 verdadeiros positivos, 0 falsos positivos e 0 falsos negativos");
    expect(gate).toContain("produção permanece bloqueada");
  });

  it("exposes only the controlled draft surfaces and preserves the residual privacy boundary", () => {
    const registry = read("engine/fact_dimension/registry.py");
    const catalog = read("engine/catalog.py");
    const contracts = read("engine/contracts/diagnosis.py");
    const pipeline = read("engine/pipeline/quality_diagnosis.py");
    const gate = read("docs/gates/MDL_UNDEFINED_020_DRAFT_CALIBRATION_001.md");

    expect(registry).toContain('"MDL-UNDEFINED-020"');
    expect(catalog).toContain('"MDL-UNDEFINED-020": "MDL-UNDEFINED-020-DRAFT-CALIBRATION-001"');
    expect(contracts).toContain('"MDL-UNDEFINED-020": "0.1.0-provisional.1"');
    expect(pipeline).toContain("UndefinedTableClassificationSheetProfile");
    expect(gate).toContain("não retêm ou expõem cabeçalhos, valores, posições, frequências individuais, exemplos, títulos de abas ou identidades dos classificadores individuais");
  });

  it("keeps production blocked and requires human confirmation", () => {
    const gate = read("docs/gates/MDL_UNDEFINED_020_DRAFT_CALIBRATION_001.md");
    const reconstructionGate = read("docs/gates/MDL_UNDEFINED_020_RECONSTRUCTION_AUTHORIZATION_001.md");

    expect(gate).toContain("pergunta humana continua bloqueante");
    expect(gate).toContain("produção permanece bloqueada");
    expect(reconstructionGate).toContain("Ele não autoriza escrever, integrar ou executar lógica da regra");
  });
});
