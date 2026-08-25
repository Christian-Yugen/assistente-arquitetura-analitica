import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("MET-DAX-015 preparation", () => {
  it("preserves the option-B scope authorization while blocking executable DAX work", () => {
    const intake = readFileSync(resolve(root, "artifacts/intake/MET-DAX-015.json"), "utf8");
    const policy = readFileSync(resolve(root, "docs/rules/MET_DAX_015_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/MET_DAX_015_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");

    expect(intake).toContain('"scope_option_b_authorized": true');
    expect(intake).toContain('"policy_approved": false');
    expect(intake).toContain('"implementation_authorized": false');
    expect(policy).toContain("template DAX abstrato e não executável");
    expect(policy).toContain("não aceitará texto DAX arbitrário como entrada");
    expect(gate).toContain("continuam bloqueados");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
