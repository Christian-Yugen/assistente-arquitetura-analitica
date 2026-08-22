import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (relativePath: string) => fs.readFileSync(path.join(root, relativePath), "utf8");

describe("REL-ORPHAN-003 preparation governance", () => {
  it("keeps the rule non-executable pending Chris's explicit policy approval", () => {
    const intake = read("artifacts/intake/REL-ORPHAN-003.json");
    const policy = read("docs/rules/REL_ORPHAN_003_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_ORPHAN_003_LOGICAL_SPEC_PROPOSAL_001.md");

    expect(intake).toContain('"status": "pending_policy_authorization"');
    expect(intake).toContain('"implementation_authorized": false');
    expect(intake).toContain('"execution_blocked": true');
    expect(intake).toContain("REL-ORPHAN-003-RECONSTRUCTION-AUTHORIZATION-001");
    expect(policy).toContain("Proposta A — alerta conservador de cobertura referencial parcial");
    expect(policy).toContain("A Proposta A ainda não foi aprovada por Chris");
    expect(policy).toContain("não cria perfil, classificador, registro, contrato, pipeline");
    expect(specification).toContain("não executável");
    expect(specification).toContain("uncovered_reference_distinct_count > 0");
    expect(specification).toContain("não confirma chave primária");
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
