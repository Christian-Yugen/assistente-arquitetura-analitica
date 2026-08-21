import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const gatePath = resolve(import.meta.dirname, "../docs/gates/QLT_HEADERS_014_DRAFT_CALIBRATION_001.md");

describe("QLT-HEADERS-014-DRAFT-CALIBRATION-001", () => {
  it("preserva a decisão limitada ao draft, as métricas, os sinais fechados e a não intervenção", () => {
    const gate = readFileSync(gatePath, "utf8");

    expect(gate).toContain("QLT-HEADERS-014");
    expect(gate).toContain("3 TP, 0 FP, 0 FN");
    expect(gate).toContain("produção bloqueada");
    expect(gate).toContain("duplicidade textual normalizada");
    expect(gate).toContain("não renomeia, preenche, deduplica, desmescla, move, exclui, insere ou reordena");
  });
});
