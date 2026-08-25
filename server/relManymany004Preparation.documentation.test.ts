import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (relativePath: string) => fs.readFileSync(path.join(root, relativePath), "utf8");

describe("REL-MANYMANY-004 draft governance", () => {
  it("records the approved policy and controlled draft activation", () => {
    const intake = read("artifacts/intake/REL-MANYMANY-004.json");
    const policy = read("docs/rules/REL_MANYMANY_004_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_MANYMANY_004_LOGICAL_SPEC_PROPOSAL_001.md");
    const gate = read("docs/gates/REL_MANYMANY_004_RECONSTRUCTION_AUTHORIZATION_001.md");
    const calibration = read("docs/gates/REL_MANYMANY_004_DRAFT_CALIBRATION_001.md");

    expect(intake).toContain('"status": "executable_draft"');
    expect(intake).toContain('"implementation_authorized": true');
    expect(intake).toContain('"execution_blocked": false');
    expect(intake).toContain("REL-MANYMANY-004-RECONSTRUCTION-AUTHORIZATION-001");
    expect(intake).toContain("REL-MANYMANY-004-DRAFT-CALIBRATION-001");
    expect(policy).toContain("Proposta A — alerta conservador de cardinalidade muitos-para-muitos");
    expect(policy).toContain("A Proposta A foi aprovada explicitamente por Chris");
    expect(policy).toContain("não cria perfil, classificador, registro, contrato, pipeline");
    expect(specification).toContain("não executável");
    expect(specification).toContain("dimension_key_unique = false");
    expect(specification).toContain("não confirma chave primária");
    expect(gate).toContain("Ele não autoriza escrever, integrar ou executar lógica da regra");
    expect(gate).toContain("Uma autorização explícita posterior de Chris");
    expect(gate).toContain("produção permanece bloqueada");
    expect(calibration).toContain("executable_draft");
    expect(calibration).toContain("produção permanece bloqueada");
  });

  it("preserves opaque-pair privacy and the production block", () => {
    const policy = read("docs/rules/REL_MANYMANY_004_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_MANYMANY_004_LOGICAL_SPEC_PROPOSAL_001.md");

    expect(policy).toContain("par opaco de abas distintas");
    expect(policy).toContain("Nenhum título de aba, cabeçalho, valor, posição");
    expect(policy).toContain("produção permanece bloqueada");
    expect(specification).toContain("descartada antes da construção do perfil");
    expect(specification).toContain("não deve emitir hipótese para identificar valores repetidos");
  });
});
