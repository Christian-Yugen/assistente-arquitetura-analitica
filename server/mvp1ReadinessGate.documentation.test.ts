import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const gatePath = resolve(import.meta.dirname, "../docs/gates/MVP_1_0_READINESS_001.md");

describe("MVP-1.0-READINESS-001", () => {
  it("preserva o bloqueio produtivo e lista os impedimentos objetivos de promoção", () => {
    const gate = readFileSync(gatePath, "utf8");

    expect(gate).toContain("**BLOQUEADO para MVP 1.0 produtivo.**");
    expect(gate).toContain("MVP draft controlado");
    expect(gate).toContain("Somente 6 de 95 regras");
    expect(gate).toContain("QLT-EMPTYCOL-003@0.1.0-reconstructed.1");
    expect(gate).toContain("QLT-EMPTYROW-004@0.1.0-reconstructed.1");
    expect(gate).toContain("QLT-CATVAR-008@0.1.0-provisional.1");
    expect(gate).toContain("QLT-DUP-002@0.1.0-reconstructed.1");
    expect(gate).toContain("exclusão física owner-scoped");
    expect(gate).toContain("Prova E2E produtiva ausente");
    expect(gate).toContain("não autoriza produção");
  });
});
