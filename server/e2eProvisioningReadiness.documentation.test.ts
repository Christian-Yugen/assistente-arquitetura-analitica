import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("E2E provisioning readiness", () => {
  it("define somente uma preparação sintética e mantém execução e produção bloqueadas", () => {
    const gate = readFileSync(resolve(root, "docs/gates/E2E_PROVISIONING_READINESS_001.md"), "utf8");
    const storage = readFileSync(resolve(root, "server/storage.ts"), "utf8");

    expect(gate).toContain("não autoriza provisionar ambiente, executar E2E");
    expect(gate).toContain("95 regras executáveis draft");
    expect(gate).toContain("workbooks gerados sinteticamente");
    expect(gate).toContain("sem dados pessoais, dados de clientes");
    expect(gate).toContain("E2E-SYN-001");
    expect(gate).toContain("E2E-SYN-006");
    expect(gate).toContain("Duas identidades de teste distintas");
    expect(gate).toContain("remoção de referência não equivale a deleção física");
    expect(gate).toContain("Autorização explícita de Chris");
    expect(gate).toContain("produção permanecerá bloqueada");
    expect(gate).toContain("Este documento não concede essa autorização");
    expect(storage).not.toContain("storageDelete");
  });
});
