import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const projectRoot = resolve(import.meta.dirname, "..");
const intakePath = resolve(projectRoot, "artifacts/intake/SEM-CAT-010.json");
const policyPath = resolve(projectRoot, "docs/rules/SEM_CAT_010_POLICY_PROPOSAL_001.md");
const specificationPath = resolve(projectRoot, "docs/rules/SEM_CAT_010_LOGICAL_SPEC_PROPOSAL_001.md");
const calibrationGatePath = resolve(projectRoot, "docs/gates/SEM_CAT_010_DRAFT_CALIBRATION_001.md");

describe("SEM-CAT-010 — ativação draft governada", () => {
  it("preserva a rastreabilidade, a calibração e o bloqueio produtivo após a ativação draft", () => {
    const intake = JSON.parse(readFileSync(intakePath, "utf8"));
    const policy = readFileSync(policyPath, "utf8");
    const specification = readFileSync(specificationPath, "utf8");
    const calibrationGate = readFileSync(calibrationGatePath, "utf8");

    expect(intake.rule.rule_id).toBe("SEM-CAT-010");
    expect(intake.local_readiness).toBe("executable_draft");
    expect(intake.authorization.implementation_authorized).toBe(true);
    expect(intake.execution_blocked).toBe(false);
    expect(intake.missing_before_execution).toEqual([]);
    expect(intake.authorization.required_gate).toBe("SEM-CAT-010-RECONSTRUCTION-AUTHORIZATION-001");

    expect(policy).toContain("Esta é uma proposta **não executável**");
    expect(policy).toContain("exatamente `categoria`");
    expect(policy).toContain("`category_candidate`");
    expect(policy).toContain("A produção permanece bloqueada.");

    expect(specification).toContain("Especificação não executável.");
    expect(specification).toContain("SemanticCategoryProfile(");
    expect(specification).toContain("confidence = 0.70");
    expect(specification).toContain('`{"tp": 3, "fp": 0, "fn": 0}`');
    expect(calibrationGate).toContain("SEM-CAT-010@0.1.0-provisional.1");
    expect(calibrationGate).toContain("62dd2c4af50ff6b9562e188c38fb44038eb46b09ad39ca1b0438a7f54d69e774");
    expect(calibrationGate).toContain("produção, taxonomia de negócio");
  });
});
