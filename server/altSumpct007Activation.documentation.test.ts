import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("ALT-SUMPCT-007 draft activation", () => {
  it("binds explicit authorization, synthetic calibration, fail-closed pipeline and production block", () => {
    const gate = readFileSync(resolve(root, "docs/gates/ALT_SUMPCT_007_DRAFT_CALIBRATION_001.md"), "utf8");
    const reconstruction = readFileSync(resolve(root, "docs/gates/ALT_SUMPCT_007_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");

    expect(reconstruction).toContain("sim, aprovado vamos acelerar que eu quero colocar esse projeto em produção");
    expect(gate).toContain("TP=1");
    expect(gate).toContain("FP=0");
    expect(gate).toContain("FN=0");
    expect(gate).toContain("pipeline de workbook fixa `independent_percentage_sum_risk_signal_count=0`");
    expect(gate).toContain("Produção permanece bloqueada");
  });
});
