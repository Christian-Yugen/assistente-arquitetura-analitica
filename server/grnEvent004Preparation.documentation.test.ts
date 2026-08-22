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
const reconstructionGatePath = resolve(
  projectRoot,
  "docs/gates/GRN_EVENT_004_RECONSTRUCTION_AUTHORIZATION_001.md"
);
const calibrationGatePath = resolve(
  projectRoot,
  "docs/gates/GRN_EVENT_004_DRAFT_CALIBRATION_001.md"
);

describe("GRN-EVENT-004 — ativação governada draft", () => {
  it("preserva a Proposta A, os gates e a ativação exclusiva em draft", () => {
    const intake = JSON.parse(readFileSync(intakePath, "utf8"));
    const policy = readFileSync(policyPath, "utf8");
    const specification = readFileSync(specificationPath, "utf8");
    const reconstructionGate = readFileSync(reconstructionGatePath, "utf8");
    const calibrationGate = readFileSync(calibrationGatePath, "utf8");

    expect(intake.rule.rule_id).toBe("GRN-EVENT-004");
    expect(intake.rule.priority).toBe("P0");
    expect(intake.rule.scope).toBe("sheet");
    expect(intake.local_readiness).toBe("executable_draft");
    expect(intake.status).toBe("executable_draft");
    expect(intake.authorization.implementation_authorized).toBe(true);
    expect(intake.execution_blocked).toBe(false);
    expect(intake.policy_approval.approved_by).toBe("Chris");
    expect(intake.policy_approval.approved_proposal).toBe("A");
    expect(intake.missing_before_execution).toEqual([]);

    expect(policy).toContain("Proposta A — hipótese de evento por linha com marcador, chave e tempo");
    expect(policy).toContain("Alternativa B — pergunta guiada sem hipótese automática");
    expect(policy).toContain("`event_per_row_candidate`");
    expect(policy).toContain("A produção permanece bloqueada.");
    expect(policy).toContain("não confirma um evento de negócio");

    expect(specification).toContain("EventPerRowSheetProfile(");
    expect(specification).toContain("explicit_key_candidate_count == 1");
    expect(specification).toContain("não classifica tabela como fato");
    expect(specification).toContain('`{"tp": 3, "fp": 0, "fn": 0}`');

    expect(reconstructionGate).toContain("GRN-EVENT-004 — Gate de Reconstrução e Autorização 001");
    expect(reconstructionGate).toContain("Ele não autoriza escrever, integrar ou executar lógica da regra.");
    expect(reconstructionGate).toContain("`event_per_row_candidate`");
    expect(reconstructionGate).toContain("A produção permanece bloqueada.");

    expect(calibrationGate).toContain("GRN-EVENT-004@0.1.0-provisional.1");
    expect(calibrationGate).toContain("GD-GRN-EVENT-004-001");
    expect(calibrationGate).toContain("6ef71effd44ea955f96f434d15437242d1e45ce18dc9d43d3d12a9b9809e019a");
    expect(calibrationGate).toContain('`{"true_positives": 3, "false_positives": 0, "false_negatives": 0}`');
    expect(calibrationGate).toContain("Produção permanece bloqueada.");
  });
});
