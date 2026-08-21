import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const retentionPath = resolve(import.meta.dirname, "../docs/security/RETENTION_LIMITATION_001.md");

describe("RETENTION-EXCEPTION-001 acceptance record", () => {
  it("records Chris's MVP draft approval while retaining the production block and re-evaluation trigger", () => {
    const record = readFileSync(retentionPath, "utf8");

    expect(record).toContain("`RETENTION-EXCEPTION-001`");
    expect(record).toContain("Responsável pelo aceite:** proprietário do produto, Chris");
    expect(record).toContain("aprovada exclusivamente para o MVP draft; produção permanece bloqueada");
    expect(record).toContain("não autoriza a produção");
    expect(record).toContain("Gatilho de reavaliação");
    expect(record).toContain("operação oficial de exclusão");
  });
});
