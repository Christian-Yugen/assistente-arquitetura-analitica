import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("E2E execution authorization", () => {
  it("registra a autorização sintética e bloqueia a execução sem ambiente descartável verificável", () => {
    const authorization = readFileSync(resolve(root, "docs/gates/E2E_EXECUTION_AUTHORIZATION_001.md"), "utf8");
    const packageJson = readFileSync(resolve(root, "package.json"), "utf8");

    expect(authorization).toContain("Chris autorizou a preparação do ciclo de E2E");
    expect(authorization).toContain("identidades e XLSX sintéticos");
    expect(authorization).toContain("Playwright e Cypress não estão presentes");
    expect(authorization).toContain("nenhum cenário E2E será executado");
    expect(authorization).toContain("ambiente descartável com banco isolado");
    expect(authorization).toContain("Produção continua bloqueada");
    expect(packageJson).not.toContain('"@playwright/test"');
    expect(packageJson).not.toContain('"cypress"');
  });
});
