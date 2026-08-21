import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const gatePath = resolve(import.meta.dirname, "../docs/gates/QLT_WHITESPACE_009_DRAFT_CALIBRATION_001.md");

describe("QLT-WHITESPACE-009-DRAFT-CALIBRATION-001", () => {
  it("preserva a decisão limitada ao draft, as métricas e a não intervenção", () => {
    const gate = readFileSync(gatePath, "utf8");

    expect(gate).toContain("QLT-WHITESPACE-009");
    expect(gate).toContain("3 TP, 0 FP, 0 FN");
    expect(gate).toContain("produção bloqueada");
    expect(gate).toContain("U+200B");
    expect(gate).toContain("não limpa, substitui, apara, normaliza, exclui ou reordena");
  });
});
