import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const read = (file: string) => readFileSync(resolve(process.cwd(), file), "utf8");

describe("MET-SUM-002 preparation governance", () => {
  it("records delegated policy approval while keeping local execution blocked", () => {
    const intake = read("artifacts/intake/MET-SUM-002.json");
    const policy = read("docs/rules/MET_SUM_002_POLICY_PROPOSAL_001.md");
    const gate = read("docs/gates/MET_SUM_002_RECONSTRUCTION_AUTHORIZATION_001.md");
    expect(intake).toContain('"policy_approved": true');
    expect(intake).toContain('"implementation_authorized": false');
    expect(intake).toContain('"execution_blocked": true');
    expect(policy).toContain("não calcula resultados");
    expect(policy).toContain("SUM(eligible_measure)");
    expect(gate).toContain("Não autoriza perfil, classificador");
    expect(gate).toContain("produção permanece bloqueada");
  });
});
