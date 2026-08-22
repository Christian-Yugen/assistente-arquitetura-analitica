import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const projectRoot = resolve(import.meta.dirname, "..");
const intakePath = resolve(projectRoot, "artifacts/intake/SEM-RESP-012.json");
const policyPath = resolve(projectRoot, "docs/rules/SEM_RESP_012_POLICY_PROPOSAL_001.md");
const specificationPath = resolve(projectRoot, "docs/rules/SEM_RESP_012_LOGICAL_SPEC_PROPOSAL_001.md");
const reconstructionGatePath = resolve(projectRoot, "docs/gates/SEM_RESP_012_RECONSTRUCTION_AUTHORIZATION_001.md");
const calibrationGatePath = resolve(projectRoot, "docs/gates/SEM_RESP_012_DRAFT_CALIBRATION_001.md");

describe("SEM-RESP-012 — ativação governada", () => {
  it("preserva a política aprovada, as evidências de calibração e a limitação ao perfil draft", () => {
    const intake = JSON.parse(readFileSync(intakePath, "utf8"));
    const policy = readFileSync(policyPath, "utf8");
    const specification = readFileSync(specificationPath, "utf8");
    const reconstructionGate = readFileSync(reconstructionGatePath, "utf8");
    const calibrationGate = readFileSync(calibrationGatePath, "utf8");

    expect(intake.rule.rule_id).toBe("SEM-RESP-012");
    expect(intake.local_readiness).toBe("executable_draft");
    expect(intake.authorization.implementation_authorized).toBe(true);
    expect(intake.authorization.required_gate).toBe("SEM-RESP-012-RECONSTRUCTION-AUTHORIZATION-001");
    expect(intake.execution_blocked).toBe(false);
    expect(intake.missing_before_execution).toEqual([]);

    expect(policy).toContain("Esta é uma proposta **não executável**");
    expect(policy).toContain("exatamente `responsavel`");
    expect(policy).toContain("`responsible_candidate`");
    expect(policy).toContain("não identificará pessoas, áreas, equipes, cargos");
    expect(policy).toContain("A produção permanece bloqueada.");

    expect(specification).toContain("SemanticResponsibleProfile(");
    expect(specification).toContain("confidence = 0.70");
    expect(specification).toContain('`{"tp": 3, "fp": 0, "fn": 0}`');

    expect(reconstructionGate).toContain("Chris aprovou explicitamente a Proposta A");
    expect(reconstructionGate).toContain("`responsible_candidate`");
    expect(reconstructionGate).toContain("produção permanece bloqueada");

    expect(calibrationGate).toContain("SEM-RESP-012@0.1.0-provisional.1");
    expect(calibrationGate).toContain("a5a2b4a7ade69ed6bad2936238f43fe879fc28de13267fe73ded3a704496db65");
    expect(calibrationGate).toContain("python3 -m engine.calibration.evaluate_sem_resp_draft_golden");
    expect(calibrationGate).toContain('{"tp": 3, "fp": 0, "fn": 0}');
    expect(calibrationGate).toContain("executable_draft");
  });
});
