import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (relativePath: string) => fs.readFileSync(path.join(root, relativePath), "utf8");

describe("REL-ONEMANY-001 preparation governance", () => {
  it("keeps the policy proposal, implementation, and production blocked", () => {
    const intake = read("artifacts/intake/REL-ONEMANY-001.json");
    const policy = read("docs/rules/REL_ONEMANY_001_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_ONEMANY_001_LOGICAL_SPEC_PROPOSAL_001.md");

    expect(intake).toContain('"status": "intake_required"');
    expect(intake).toContain('"policy_approved": true');
    expect(intake).toContain('"policy_approved_by": "Chris"');
    expect(intake).toContain('"implementation_authorized": false');
    expect(intake).toContain('"execution_blocked": true');
    expect(intake).toContain('"scope": "sheet_pair"');
    expect(policy).toContain("Proposta A — hipótese conservadora de relacionamento um-para-muitos");
    expect(policy).toContain("Proposta A aprovada explicitamente por Chris");
    expect(policy).toContain("Não autoriza perfil, classificador, registro, contrato, pipeline, catálogo, testes, dataset golden, calibração, ativação draft ou produção");
    expect(specification).toContain("não executável");
    expect(specification).toContain("Uma aprovação de política não autoriza a escrita, integração ou execução de código");
  });

  it("preserves the approved privacy and non-overlap boundaries without adding executable integration", () => {
    const policy = read("docs/rules/REL_ONEMANY_001_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/REL_ONEMANY_001_LOGICAL_SPEC_PROPOSAL_001.md");
    const registry = read("engine/fact_dimension/registry.py");
    const pipeline = read("engine/pipeline/quality_diagnosis.py");
    const catalog = read("engine/catalog.py");

    expect(policy).toContain("títulos de abas, cabeçalhos, valores, posições, pares correspondentes");
    expect(policy).toContain("cardinalidade 1:1, muitos-para-muitos");
    expect(specification).toContain("referential_coverage_ratio = 1.0");
    expect(specification).toContain("dimensão calendário, fato sem granularidade definida, classificação indefinida");
    expect(registry).not.toContain("REL-ONEMANY-001");
    expect(pipeline).not.toContain("REL-ONEMANY-001");
    expect(catalog).not.toContain("REL-ONEMANY-001");
  });

  it("records the approved Proposal A and the reconstruction gate without releasing execution", () => {
    const intake = read("artifacts/intake/REL-ONEMANY-001.json");
    const policy = read("docs/rules/REL_ONEMANY_001_POLICY_PROPOSAL_001.md");
    const gate = read("docs/gates/REL_ONEMANY_001_RECONSTRUCTION_AUTHORIZATION_001.md");

    expect(intake).toContain("REL-ONEMANY-001-RECONSTRUCTION-AUTHORIZATION-001");
    expect(policy).toContain("Proposta A aprovada explicitamente por Chris");
    expect(gate).toContain("one_to_many_relationship_candidate");
    expect(gate).toContain("Ele não autoriza escrever, integrar ou executar lógica da regra");
    expect(gate).toContain("produção permanece bloqueada");
  });
});
