import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");
const gatePath = resolve(root, "docs/gates/QLT_EMPTYROW_004_DRAFT_CALIBRATION_001.md");
const policyPath = resolve(root, "docs/rules/QLT_EMPTYROW_004_POLICY_RECONSTRUCTED_001.md");
const goldenPath = resolve(root, "artifacts/golden/emptyrow-draft-golden-v1.json");
const manifestPath = resolve(root, "artifacts/golden/emptyrow-draft-golden-v1.manifest.json");
const calibrationPath = resolve(root, "artifacts/golden/emptyrow-draft-golden-v1.calibration.json");
const catalogPath = resolve(root, "engine/catalog.py");

describe("QLT-EMPTYROW-004 draft calibration evidence", () => {
  it("encadeia decisão humana, política conservadora, dataset íntegro, calibração e allowlist draft", () => {
    const gate = readFileSync(gatePath, "utf8");
    const policy = readFileSync(policyPath, "utf8");
    const goldenBytes = readFileSync(goldenPath);
    const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
    const calibration = JSON.parse(readFileSync(calibrationPath, "utf8"));
    const catalog = readFileSync(catalogPath, "utf8");

    expect(gate).toContain("decisão de Chris pela opção A");
    expect(gate).toContain("**Produção:** bloqueada.");
    expect(policy).toContain("entre linhas com conteúdo");
    expect(manifest.dataset_id).toBe("GD-QLT-EMPTYROW-004-001");
    expect(manifest.privacy.contains_raw_workbook_values).toBe(false);
    expect(manifest.privacy.contains_cell_positions).toBe(false);
    expect(manifest.privacy.contains_sheet_titles).toBe(false);
    expect(manifest.sha256).toBe(createHash("sha256").update(goldenBytes).digest("hex"));
    expect(calibration).toMatchObject({
      calibration_id: "CAL-QLT-EMPTYROW-004-001",
      rule_id: "QLT-EMPTYROW-004",
      scope: "draft_only",
      production_release: "blocked",
      metrics: { true_positive: 3, false_positive: 0, false_negative: 0 },
    });
    expect(catalog).toContain('"QLT-EMPTYROW-004": "QLT-EMPTYROW-004-DRAFT-CALIBRATION-001"');
  });
});
