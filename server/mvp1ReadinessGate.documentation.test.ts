import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const gatePath = resolve(import.meta.dirname, "../docs/gates/MVP_1_0_READINESS_001.md");

describe("MVP-1.0-READINESS-001", () => {
  it("preserva o bloqueio produtivo e lista os impedimentos objetivos de promoção", () => {
    const gate = readFileSync(gatePath, "utf8");

    expect(gate).toContain("**BLOQUEADO para MVP 1.0 produtivo.**");
    expect(gate).toContain("MVP draft controlado");
    expect(gate).toContain("Somente 2 de 95 regras");
    expect(gate).toContain("exclusão física owner-scoped");
    expect(gate).toContain("Prova E2E produtiva ausente");
    expect(gate).toContain("não autoriza produção");
  });
});
