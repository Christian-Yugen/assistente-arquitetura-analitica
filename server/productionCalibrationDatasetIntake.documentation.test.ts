import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("production calibration dataset intake", () => {
  it("registra somente autorização de intake e bloqueia qualquer operação de dados", () => {
    const intake = JSON.parse(readFileSync(resolve(root, "artifacts/intake/PROD-CALIBRATION-DATASET-001.json"), "utf8"));
    expect(intake.status).toBe("intake_open_no_data");
    expect(intake.authorization.intake_authorized).toBe(true);
    expect(intake.authorization.data_processing_authorized).toBe(false);
    expect(intake.authorization.production_authorized).toBe(false);
    expect(intake.data_receipt.received).toBe(false);
    expect(intake.data_receipt.origin).toBeNull();
    expect(intake.data_receipt.pii_inventory).toBeNull();
    expect(intake.data_receipt.human_label_source).toBeNull();
    expect(intake.data_receipt.physical_deletion_available).toBe(false);
    expect(Object.values(intake.operations)).toEqual([false, false, false, false, false, false]);
    expect(intake.production_blocked).toBe(true);
  });
});
