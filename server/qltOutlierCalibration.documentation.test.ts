import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const gatePath = resolve(import.meta.dirname, "../docs/gates/QLT_OUTLIER_012_DRAFT_CALIBRATION_001.md");

describe("QLT-OUTLIER-012-DRAFT-CALIBRATION-001", () => {
  it("preserva a decisão limitada ao draft, as métricas, o método fechado e a não intervenção", () => {
    const gate = readFileSync(gatePath, "utf8");

    expect(gate).toContain("QLT-OUTLIER-012");
    expect(gate).toContain("3 TP, 0 FP, 0 FN");
    expect(gate).toContain("produção bloqueada");
    expect(gate).toContain("Q1 − 1,5 × IQR");
    expect(gate).toContain("não remove, corrige, substitui, arredonda, winsoriza, transforma, move ou reordena");
  });
});
