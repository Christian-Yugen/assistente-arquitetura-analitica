import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");
const gatePath = resolve(root, "docs/gates/QLT_DUP_002_DRAFT_CALIBRATION_001.md");
const policyPath = resolve(root, "docs/rules/QLT_DUP_002_POLICY_RECONSTRUCTED_001.md");
const goldenPath = resolve(root, "artifacts/golden/dup-draft-golden-v1.json");
const goldenManifestPath = resolve(root, "artifacts/golden/dup-draft-golden-v1.manifest.json");
const calibrationPath = resolve(root, "artifacts/golden/dup-draft-golden-v1.calibration.json");
const catalogPath = resolve(root, "engine/catalog.py");

describe("QLT-DUP-002 reconstructed draft calibration gate", () => {
  it("connects Chris's authorization, aggregate calibration, privacy limits and production block", () => {
    const gate = readFileSync(gatePath, "utf8");
    const policy = readFileSync(policyPath, "utf8");
    const golden = readFileSync(goldenPath);
    const manifest = JSON.parse(readFileSync(goldenManifestPath, "utf8")) as {
      dataset_id: string;
      sha256: string;
      contains_raw_workbook_values: boolean;
      contains_row_signatures: boolean;
      contains_row_indices: boolean;
    };
    const calibration = JSON.parse(readFileSync(calibrationPath, "utf8")) as {
      calibration_id: string;
      scope: string;
      production_release: string;
      metrics: { true_positive: number; false_positive: number; false_negative: number };
    };
    const catalog = readFileSync(catalogPath, "utf8");

    expect(gate).toContain("Chris");
    expect(gate).toContain("5 TP, 0 FP, 0 FN");
    expect(gate).toContain("não autoriza exclusão");
    expect(policy).toContain("assinatura técnica integral");
    expect(policy).toContain("Inferência de chave | Proibida");
    expect(manifest.dataset_id).toBe("GD-QLT-DUP-002-001");
    expect(manifest.contains_raw_workbook_values).toBe(false);
    expect(manifest.contains_row_signatures).toBe(false);
    expect(manifest.contains_row_indices).toBe(false);
    expect(manifest.sha256).toBe(createHash("sha256").update(golden).digest("hex"));
    expect(calibration.calibration_id).toBe("CAL-QLT-DUP-002-001");
    expect(calibration.scope).toBe("draft_only");
    expect(calibration.production_release).toBe("blocked");
    expect(calibration.metrics).toEqual({ true_positive: 5, false_positive: 0, false_negative: 0 });
    expect(catalog).toContain('"QLT-DUP-002": "QLT-DUP-002-DRAFT-CALIBRATION-001"');
  });
});
