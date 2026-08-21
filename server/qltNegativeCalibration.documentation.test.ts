import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const gatePath = resolve(import.meta.dirname, "../docs/gates/QLT_NEGATIVE_011_DRAFT_CALIBRATION_001.md");

describe("QLT-NEGATIVE-011-DRAFT-CALIBRATION-001", () => {
  it("preserva a decisão limitada ao draft, as métricas, o vocabulário fechado e a não intervenção", () => {
    const gate = readFileSync(gatePath, "utf8");

    expect(gate).toContain("QLT-NEGATIVE-011");
    expect(gate).toContain("3 TP, 0 FP, 0 FN");
    expect(gate).toContain("produção bloqueada");
    expect(gate).toContain("`quantidade`, `qtd`, `estoque`, `volume` e `idade`");
    expect(gate).toContain("não corrige, converte, exclui, preenche, arredonda, move ou reordena");
  });
});
