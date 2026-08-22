import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (relativePath: string) => fs.readFileSync(path.join(root, relativePath), "utf8");

describe("REL-ORPHAN-003 draft governance", () => {
  it("records Chris's authorized draft activation while keeping production blocked", () => {
    const intake = read("artifacts/intake/REL-ORPHAN-003.json");
    const policy = read("docs/rules/REL_ORPHAN_003_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_ORPHAN_003_LOGICAL_SPEC_PROPOSAL_001.md");
    const gate = read("docs/gates/REL_ORPHAN_003_RECONSTRUCTION_AUTHORIZATION_001.md");
    const calibrationGate = read("docs/gates/REL_ORPHAN_003_DRAFT_CALIBRATION_001.md");

    expect(intake).toContain('"status": "executable_draft"');
    expect(intake).toContain('"implementation_authorized": true');
    expect(intake).toContain('"execution_blocked": false');
    expect(intake).toContain('"policy_approved": true');
    expect(intake).toContain("REL-ORPHAN-003-RECONSTRUCTION-AUTHORIZATION-001");
    expect(policy).toContain("Proposta A — alerta conservador de cobertura referencial parcial");
    expect(policy).toContain("A Proposta A foi aprovada explicitamente por Chris");
    expect(policy).toContain("não cria perfil, classificador, registro, contrato, pipeline");
    expect(specification).toContain("não executável");
    expect(specification).toContain("uncovered_reference_distinct_count > 0");
    expect(specification).toContain("não confirma chave primária");
    expect(intake).toContain("REL-ORPHAN-003-DRAFT-CALIBRATION-001");
    expect(gate).toContain("Uma autorização explícita posterior de Chris será obrigatória");
    expect(calibrationGate).toContain("3 verdadeiros positivos, 0 falsos positivos e 0 falsos negativos");
    expect(calibrationGate).toContain("produção permanece bloqueada");
    expect(gate).toContain("produção permanece bloqueada");
  });

  it("preserves opaque-pair privacy and the production block", () => {
    const policy = read("docs/rules/REL_ORPHAN_003_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_ORPHAN_003_LOGICAL_SPEC_PROPOSAL_001.md");

    expect(policy).toContain("par opaco de abas distintas");
    expect(policy).toContain("Nenhum título de aba, cabeçalho, valor, posição");
    expect(policy).toContain("produção permanece bloqueada");
    expect(specification).toContain("descartada antes da construção do perfil");
    expect(specification).toContain("não deve emitir hipótese para identificar valores órfãos");
  });
});
