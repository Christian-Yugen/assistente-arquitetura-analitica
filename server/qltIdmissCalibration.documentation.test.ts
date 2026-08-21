import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const gatePath = resolve(import.meta.dirname, "../docs/gates/QLT_IDMISS_015_DRAFT_CALIBRATION_001.md");

describe("QLT-IDMISS-015-DRAFT-CALIBRATION-001", () => {
  it("preserva a decisão limitada ao draft, as métricas, o vocabulário fechado e a não intervenção", () => {
    const gate = readFileSync(gatePath, "utf8");

    expect(gate).toContain("QLT-IDMISS-015");
    expect(gate).toContain("3 TP, 0 FP, 0 FN");
    expect(gate).toContain("produção bloqueada");
    expect(gate).toContain("`id`, `codigo`, `cod`, `chave`, `matricula`, `cpf`, `cnpj`, `numero` e `num`");
    expect(gate).toContain("não preenche, gera, corrige, deduplica, apaga, converte, normaliza, move ou reordena");
  });
});
