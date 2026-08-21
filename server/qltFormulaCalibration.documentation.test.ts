import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const gatePath = resolve(import.meta.dirname, "../docs/gates/QLT_FORMULA_013_DRAFT_CALIBRATION_001.md");

describe("QLT-FORMULA-013-DRAFT-CALIBRATION-001", () => {
  it("preserva a decisão limitada ao draft, as métricas, o sinal fechado e a não intervenção", () => {
    const gate = readFileSync(gatePath, "utf8");

    expect(gate).toContain("QLT-FORMULA-013");
    expect(gate).toContain("3 TP, 0 FP, 0 FN");
    expect(gate).toContain("produção bloqueada");
    expect(gate).toContain("presença versus ausência de tipo de célula `f`");
    expect(gate).toContain("não cria, copia, corrige, preenche, apaga, recalcula, move ou reordena");
  });
});
