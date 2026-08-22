import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const projectRoot = resolve(import.meta.dirname, "..");
const intakePath = resolve(projectRoot, "artifacts/intake/SEM-LOC-011.json");
const policyPath = resolve(projectRoot, "docs/rules/SEM_LOC_011_POLICY_PROPOSAL_001.md");
const specificationPath = resolve(projectRoot, "docs/rules/SEM_LOC_011_LOGICAL_SPEC_PROPOSAL_001.md");
const reconstructionGatePath = resolve(projectRoot, "docs/gates/SEM_LOC_011_RECONSTRUCTION_AUTHORIZATION_001.md");
const calibrationGatePath = resolve(projectRoot, "docs/gates/SEM_LOC_011_DRAFT_CALIBRATION_001.md");

describe("SEM-LOC-011 — ativação governada", () => {
  it("preserva os limites aprovados, a evidência de calibração e o bloqueio de produção", () => {
    const intake = JSON.parse(readFileSync(intakePath, "utf8"));
    const policy = readFileSync(policyPath, "utf8");
    const specification = readFileSync(specificationPath, "utf8");
    const reconstructionGate = readFileSync(reconstructionGatePath, "utf8");
    const calibrationGate = readFileSync(calibrationGatePath, "utf8");

    expect(intake.rule.rule_id).toBe("SEM-LOC-011");
    expect(intake.local_readiness).toBe("executable_draft");
    expect(intake.authorization.implementation_authorized).toBe(true);
    expect(intake.execution_blocked).toBe(false);
    expect(intake.missing_before_execution).toEqual([]);

    expect(policy).toContain("Esta é uma proposta **não executável**");
    expect(policy).toContain("`cidade`, `municipio`, `pais`, `regiao` ou `localizacao`");
    expect(policy).toContain("`location_candidate`");
    expect(policy).toContain("A produção permanece bloqueada.");
    expect(policy).toContain("não interpreta, grava, geocodifica ou valida rótulos");

    expect(specification).toContain("Especificação não executável.");
    expect(specification).toContain("SemanticLocationProfile(");
    expect(specification).toContain("confidence = 0.75");
    expect(specification).toContain('{"tp": 3, "fp": 0, "fn": 0}');
    expect(reconstructionGate).toContain("produção permanece bloqueada");
    expect(reconstructionGate).toContain("Não são autorizadas inspeção ou retenção de valores");
    expect(calibrationGate).toContain("SEM-LOC-011@0.1.0-provisional.1");
    expect(calibrationGate).toContain('{"tp": 3, "fp": 0, "fn": 0}');
  });
});
