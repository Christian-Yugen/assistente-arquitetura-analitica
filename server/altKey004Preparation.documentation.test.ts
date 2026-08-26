import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("ALT-KEY-004 draft activation", () => {
  it("preserves authorized aggregate-only policy and production block", () => {
    const intake = readFileSync(resolve(root, "artifacts/intake/ALT-KEY-004.json"), "utf8");
    const policy = readFileSync(resolve(root, "docs/rules/ALT_KEY_004_POLICY_PROPOSAL_001.md"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/ALT_KEY_004_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");
    expect(intake).toContain('"local_readiness": "executable_draft"');
    expect(intake).toContain('"implementation_authorized": true');
    expect(policy).toContain("sinais de chave já inferidos, independentes, opacos e agregados");
    expect(policy).toContain("não declarará qual campo deve ser uma chave do modelo");
    expect(gate).toContain("atutorizadocontinuar");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
