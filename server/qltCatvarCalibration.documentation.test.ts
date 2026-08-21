import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");
const gatePath = resolve(root, "docs/gates/QLT_CATVAR_008_DRAFT_CALIBRATION_001.md");
const policyPath = resolve(root, "docs/rules/QLT_CATVAR_008_POLICY_PROVISIONAL_001.md");
const goldenPath = resolve(root, "artifacts/golden/catvar-draft-golden-v1.json");
const goldenManifestPath = resolve(root, "artifacts/golden/catvar-draft-golden-v1.manifest.json");
const calibrationPath = resolve(root, "artifacts/golden/catvar-draft-golden-v1.calibration.json");
const dictionaryPath = resolve(root, "artifacts/rules/QLT-CATVAR-008/provisional-domain-dictionary-v1.json");
const catalogPath = resolve(root, "engine/catalog.py");

describe("QLT-CATVAR-008 provisional draft calibration gate", () => {
  it("connects Chris's authorization, aggregate calibration, empty dictionary and production block", () => {
    const gate = readFileSync(gatePath, "utf8");
    const policy = readFileSync(policyPath, "utf8");
    const golden = readFileSync(goldenPath);
    const manifest = JSON.parse(readFileSync(goldenManifestPath, "utf8")) as {
      dataset_id: string;
      sha256: string;
      scenario_count: number;
      status: string;
    };
    const calibration = JSON.parse(readFileSync(calibrationPath, "utf8")) as {
      report_id: string;
      mismatch_count: number;
      production_status: string;
      rules: Record<string, { true_positive: number; false_positive: number; false_negative: number }>;
    };
    const dictionary = JSON.parse(readFileSync(dictionaryPath, "utf8")) as {
      status: string;
      mappings: Record<string, unknown>;
    };
    const catalog = readFileSync(catalogPath, "utf8");

    expect(gate).toContain("Chris");
    expect(gate).toContain("4 TP, 0 FP, 0 FN");
    expect(gate).toContain("produção");
    expect(gate).toContain("não aprova produção");
    expect(policy).toContain("inicia vazio");
    expect(manifest.dataset_id).toBe("GD-QLT-CATVAR-008-001");
    expect(manifest.scenario_count).toBe(6);
    expect(manifest.status).toBe("approved_for_provisional_draft_calibration");
    expect(manifest.sha256).toBe(createHash("sha256").update(golden).digest("hex"));
    expect(calibration.report_id).toBe("CAL-QLT-CATVAR-008-001");
    expect(calibration.mismatch_count).toBe(0);
    expect(calibration.production_status).toBe("blocked");
    expect(calibration.rules["QLT-CATVAR-008"]).toEqual({
      true_positive: 4,
      false_positive: 0,
      false_negative: 0,
    });
    expect(dictionary.status).toBe("empty_pending_domain_approval");
    expect(dictionary.mappings).toEqual({});
    expect(catalog).toContain('"QLT-CATVAR-008": "QLT-CATVAR-008-DRAFT-CALIBRATION-001"');
  });
});
