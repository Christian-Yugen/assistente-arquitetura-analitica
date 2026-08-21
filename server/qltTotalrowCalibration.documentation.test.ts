import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const gatePath = resolve(import.meta.dirname, "../docs/gates/QLT_TOTALROW_010_DRAFT_CALIBRATION_001.md");

describe("QLT-TOTALROW-010-DRAFT-CALIBRATION-001", () => {
  it("preserva a decisão limitada ao draft, as métricas, o vocabulário e a não intervenção", () => {
    const gate = readFileSync(gatePath, "utf8");

    expect(gate).toContain("QLT-TOTALROW-010");
    expect(gate).toContain("3 TP, 0 FP, 0 FN");
    expect(gate).toContain("produção bloqueada");
    expect(gate).toContain("`total`, `subtotal` ou `total geral`");
    expect(gate).toContain("não altera, exclui, cria, move ou reordena");
  });
});
