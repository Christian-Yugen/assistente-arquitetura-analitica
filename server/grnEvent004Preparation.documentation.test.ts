import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const projectRoot = resolve(import.meta.dirname, "..");
const intakePath = resolve(projectRoot, "artifacts/intake/GRN-EVENT-004.json");
const policyPath = resolve(projectRoot, "docs/rules/GRN_EVENT_004_POLICY_PROPOSAL_001.md");
const specificationPath = resolve(
  projectRoot,
  "docs/rules/GRN_EVENT_004_LOGICAL_SPEC_PROPOSAL_001.md"
);

describe("GRN-EVENT-004 — preparação governada", () => {
  it("preserva o intake, a política não executável e o bloqueio de implementação", () => {
    const intake = JSON.parse(readFileSync(intakePath, "utf8"));
    const policy = readFileSync(policyPath, "utf8");
    const specification = readFileSync(specificationPath, "utf8");

    expect(intake.rule.rule_id).toBe("GRN-EVENT-004");
    expect(intake.rule.priority).toBe("P0");
    expect(intake.rule.scope).toBe("sheet");
    expect(intake.local_readiness).toBe("intake_required");
    expect(intake.status).toBe("intake_required");
    expect(intake.authorization.implementation_authorized).toBe(false);
    expect(intake.execution_blocked).toBe(true);
    expect(intake.missing_before_execution).toContain(
      "Aprovação explícita de Chris para uma política de inferência de evento por linha"
    );

    expect(policy).toContain("Proposta A — hipótese de evento por linha com marcador, chave e tempo");
    expect(policy).toContain("Alternativa B — pergunta guiada sem hipótese automática");
    expect(policy).toContain("`event_per_row_candidate`");
    expect(policy).toContain("A produção permanece bloqueada.");
    expect(policy).toContain("não confirma um evento de negócio");

    expect(specification).toContain("EventPerRowSheetProfile(");
    expect(specification).toContain("explicit_key_candidate_count == 1");
    expect(specification).toContain("não classifica tabela como fato");
    expect(specification).toContain('`{"tp": 3, "fp": 0, "fn": 0}`');
  });
});
