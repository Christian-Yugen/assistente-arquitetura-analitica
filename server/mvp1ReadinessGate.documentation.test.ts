import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const gatePath = resolve(import.meta.dirname, "../docs/gates/MVP_1_0_READINESS_001.md");

describe("MVP-1.0-READINESS-001", () => {
  it("preserva o bloqueio produtivo e lista os impedimentos objetivos de promoção", () => {
    const gate = readFileSync(gatePath, "utf8");

    expect(gate).toContain("**BLOQUEADO para MVP 1.0 produtivo.**");
    expect(gate).toContain("MVP draft controlado");
    expect(gate).toContain("Somente 31 de 95 regras");
    expect(gate).toContain("SEM-DATE-001@0.1.0-provisional.1");
    expect(gate).toContain("SEM-COMP-002@0.1.0-provisional.1");
    expect(gate).toContain("SEM-DESC-004@0.1.0-provisional.1");
    expect(gate).toContain("SEM-DUR-008@0.1.0-provisional.1");
    expect(gate).toContain("SEM-ID-003@0.1.0-provisional.1");
    expect(gate).toContain("SEM-QTY-005@0.1.0-provisional.1");
    expect(gate).toContain("SEM-CURR-006@0.1.0-provisional.1");
    expect(gate).toContain("SEM-PCT-007@0.1.0-provisional.1");
    expect(gate).toContain("SEM-TARGET-013@0.1.0-provisional.1");
    expect(gate).toContain("SEM-ACTUAL-014@0.1.0-provisional.1");
    expect(gate).toContain("SEM-SENS-015@0.1.0-provisional.1");
    expect(gate).toContain("MDL-FACTTXN-002@0.1.0-provisional.1");
    expect(gate).toContain("MDL-DIMSTD-004@0.1.0-provisional.1");
    expect(gate).toContain("MDL-DIMCAL-006@0.1.0-provisional.1");
    expect(gate).toContain("exclusão física owner-scoped");
    expect(gate).toContain("Prova E2E produtiva ausente");
    expect(gate).toContain("não autoriza produção");
  });
});
