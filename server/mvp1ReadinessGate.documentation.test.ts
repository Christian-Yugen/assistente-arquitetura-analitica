import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const gatePath = resolve(import.meta.dirname, "../docs/gates/MVP_1_0_READINESS_001.md");

describe("MVP-1.0-READINESS-001", () => {
  it("preserva o bloqueio produtivo e lista os impedimentos objetivos de promoção", () => {
    const gate = readFileSync(gatePath, "utf8");

    expect(gate).toContain("**BLOQUEADO para MVP 1.0 produtivo.**");
    expect(gate).toContain("MVP draft controlado");
    expect(gate).toContain("Somente 44 de 95 regras");
    expect(gate).toContain("As quinze regras de Qualidade");
    expect(gate).toContain("regras semânticas, de granularidade e de modelagem previamente habilitadas");
    expect(gate).toContain("REL-ONEMANY-001@0.1.0-provisional.1");
    expect(gate).toContain("REL-NONUNIQ-002@0.1.0-provisional.1");
    expect(gate).toContain("REL-ORPHAN-003@0.1.0-provisional.1");
    expect(gate).toContain("REL-MANYMANY-004@0.1.0-provisional.1");
    expect(gate).toContain("exclusão física owner-scoped");
    expect(gate).toContain("Prova E2E produtiva ausente");
    expect(gate).toContain("não autoriza produção");
  });
});
