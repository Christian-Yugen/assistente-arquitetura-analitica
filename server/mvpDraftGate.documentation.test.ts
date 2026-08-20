import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const gatePath = resolve(import.meta.dirname, "../docs/gates/MVP_DRAFT_CONSOLIDATION_001.md");

describe("MVP draft consolidation gate record", () => {
  it("records the decision, executed evidence, pending work and production blockers", () => {
    const gate = readFileSync(gatePath, "utf8");

    expect(gate).toContain("aprovado **somente como MVP draft controlado**");
    expect(gate).toContain("43 testes Vitest");
    expect(gate).toContain("30 testes Python");
    expect(gate).toContain("`pnpm check`: aprovado");
    expect(gate).toContain("## Bloqueios de promoção");
    expect(gate).toContain("## Pendências");
    expect(gate).toContain("## Próximos passos");
    expect(gate).toContain("Exclusão física");
    expect(gate).toContain("Artefato QLT-NULL-001");
    expect(gate).toContain("Banco provisionado");
  });
});
