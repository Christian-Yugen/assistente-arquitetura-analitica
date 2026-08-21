import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const gatePath = resolve(import.meta.dirname, "../docs/gates/QLT_MIXTYPE_005_DRAFT_CALIBRATION_001.md");

describe("QLT-MIXTYPE-005-DRAFT-CALIBRATION-001", () => {
  it("preserva a decisão limitada ao draft, as métricas e a proibição produtiva", () => {
    const gate = readFileSync(gatePath, "utf8");

    expect(gate).toContain("QLT-MIXTYPE-005");
    expect(gate).toContain("3 TP, 0 FP, 0 FN");
    expect(gate).toContain("produção bloqueada");
    expect(gate).toContain("Cadeias numéricas canônicas");
    expect(gate).toContain("não converte, exclui, preenche ou reordena");
  });
});
