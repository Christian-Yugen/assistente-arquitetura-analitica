import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("production calibration readiness", () => {
  it("preserva o escopo sintético draft e bloqueia coleta, execução e promoção", () => {
    const gate = readFileSync(resolve(root, "docs/gates/PRODUCTION_CALIBRATION_READINESS_001.md"), "utf8");
    const intakeTemplate = readFileSync(resolve(root, "docs/gates/PRODUCTION_CALIBRATION_DATA_INTAKE_TEMPLATE_001.md"), "utf8");
    const qualityCalibration = readFileSync(resolve(root, "engine/tests/test_golden_quality_calibration.py"), "utf8");
    expect(qualityCalibration).toContain('"calibrated_for_draft"');
    expect(qualityCalibration).toContain('"production_status"');
    expect(gate).toContain("75 manifestos");
    expect(gate).toContain("38");
    expect(gate).toContain("54");
    expect(gate).toContain("não autoriza executar calibração produtiva");
    expect(gate).toContain("desidentificado, owner-scoped e aprovado");
    expect(gate).toContain("TP, FP e FN por regra");
    expect(gate).toContain("Chris deverá autorizar explicitamente");
    expect(gate).toContain("Esta proposta não concede nenhuma dessas autorizações");
    expect(intakeTemplate).toContain("template vazio e não executável");
    expect(intakeTemplate).toContain("Nenhum conjunto está autorizado");
    expect(intakeTemplate).toContain("TP, FP e FN por regra");
    expect(intakeTemplate).toContain("A remoção de referência não deverá ser declarada como exclusão física");
    expect(intakeTemplate).toContain("não autoriza executar calibragem, alterar regras ou promover ambiente");
  });
});
