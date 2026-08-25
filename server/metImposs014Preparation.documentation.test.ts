import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("MET-IMPOSS-014 preparation", () => {
  it("preserves non-executable intake, aggregate-only policy and production block", () => {
    const intake = readFileSync(resolve(root, "artifacts/intake/MET-IMPOSS-014.json"), "utf8");
    const policy = readFileSync(resolve(root, "docs/rules/MET_IMPOSS_014_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/MET_IMPOSS_014_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");

    expect(intake).toContain('"local_readiness": "intake_required"');
    expect(intake).toContain('"implementation_authorized": false');
    expect(intake).toContain('"production_authorized": false');
    expect(policy).toContain("flags e contagens agregadas");
    expect(policy).toContain("não gera DAX ou Power Query");
    expect(gate).toContain("continuam não autorizados");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
