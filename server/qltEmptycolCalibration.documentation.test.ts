import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");
const gatePath = resolve(root, "docs/gates/QLT_EMPTYCOL_003_DRAFT_CALIBRATION_001.md");
const policyPath = resolve(root, "docs/rules/QLT_EMPTYCOL_003_POLICY_RECONSTRUCTED_001.md");
const goldenManifestPath = resolve(root, "artifacts/golden/emptycol-draft-golden-v1.manifest.json");
const calibrationPath = resolve(root, "artifacts/golden/emptycol-draft-golden-v1.calibration.json");
const catalogPath = resolve(root, "engine/catalog.py");

describe("QLT-EMPTYCOL-003 reconstructed draft calibration gate", () => {
  it("vincula a autorização de Chris, a calibração agregada, os limites de privacidade e o bloqueio produtivo", () => {
    const gate = readFileSync(gatePath, "utf8");
    const policy = readFileSync(policyPath, "utf8");
    const manifest = JSON.parse(readFileSync(goldenManifestPath, "utf8")) as { dataset_id: string; scope: string; production_release: string };
    const calibration = readFileSync(calibrationPath, "utf8");
    const catalog = readFileSync(catalogPath, "utf8");

    expect(gate).toContain("Alternativa A aprovada por Chris");
    expect(gate).toContain("4 TP, 0 FP, 0 FN");
    expect(gate).toContain("não autoriza excluir colunas");
    expect(policy).toContain("texto composto somente por espaços");
    expect(policy).toContain("Valores `0`, `false`, datas, números, booleanos");
    expect(policy).toContain("Valores de células, números de linha, títulos brutos de aba, fórmulas e amostras são proibidos");
    expect(manifest).toMatchObject({
      dataset_id: "GD-QLT-EMPTYCOL-003-001",
      scope: "aggregate_only_draft_calibration",
      production_release: "blocked",
    });
    expect(calibration).toContain('"calibration_id": "CAL-QLT-EMPTYCOL-003-001"');
    expect(calibration).toContain('"true_positive": 4');
    expect(calibration).toContain('"false_positive": 0');
    expect(calibration).toContain('"false_negative": 0');
    expect(catalog).toContain('"QLT-EMPTYCOL-003": "QLT-EMPTYCOL-003-DRAFT-CALIBRATION-001"');
  });
});
