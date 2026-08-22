import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const projectRoot = resolve(import.meta.dirname, "..");
const intakePath = resolve(projectRoot, "artifacts/intake/GRN-ENTITY-003.json");
const policyPath = resolve(projectRoot, "docs/rules/GRN_ENTITY_003_POLICY_PROPOSAL_001.md");
const specificationPath = resolve(
  projectRoot,
  "docs/rules/GRN_ENTITY_003_LOGICAL_SPEC_PROPOSAL_001.md"
);

describe("GRN-ENTITY-003 — preparação governada", () => {
  it("preserva o bloqueio de execução e a política ainda não aprovada", () => {
    const intake = JSON.parse(readFileSync(intakePath, "utf8"));
    const policy = readFileSync(policyPath, "utf8");
    const specification = readFileSync(specificationPath, "utf8");

    expect(intake.rule.rule_id).toBe("GRN-ENTITY-003");
    expect(intake.rule.priority).toBe("P1");
    expect(intake.rule.scope).toBe("sheet");
    expect(intake.local_readiness).toBe("intake_required");
    expect(intake.status).toBe("intake_required");
    expect(intake.authorization.implementation_authorized).toBe(false);
    expect(intake.execution_blocked).toBe(true);
    expect(intake.missing_before_execution).toContain("authorization_gate");

    expect(policy).toContain("Proposta A — hipótese conservadora de entidade estável por linha");
    expect(policy).toContain("Alternativa B — pergunta guiada sem hipótese automática");
    expect(policy).toContain("`entity_per_row_candidate`");
    expect(policy).toContain("A produção permanece bloqueada.");
    expect(policy).toContain("não confirma entidade de negócio");

    expect(specification).toContain("EntityPerRowSheetProfile(");
    expect(specification).toContain("explicit_key_candidate_count == 1");
    expect(specification).toContain("não classifica dimensão");
    expect(specification).toContain('`{"tp": 3, "fp": 0, "fn": 0}`');
  });
});
