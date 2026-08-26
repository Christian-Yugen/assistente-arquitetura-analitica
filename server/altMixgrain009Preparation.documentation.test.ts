import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("ALT-MIXGRAIN-009 preparation", () => {
  it("preserves the aggregate-only authorization and production block", () => {
    const intake = readFileSync(resolve(root, "artifacts/intake/ALT-MIXGRAIN-009.json"), "utf8");
    const policy = readFileSync(resolve(root, "docs/rules/ALT_MIXGRAIN_009_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/ALT_MIXGRAIN_009_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");

    expect(intake).toContain('"execution_profile": "draft"');
    expect(intake).toContain('"implementation_authorized": true');
    expect(intake).toContain('"production_authorized": false');
    expect(policy).toContain("fonte independente, autorizada, opaca e agregada");
    expect(policy).toContain("não poderá inferir granularidade");
    expect(policy).toContain("Qualquer código executável requer uma autorização nova e explícita de Chris");
    expect(gate).toContain("ok. continue o desenvolvimento, autorizado");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
