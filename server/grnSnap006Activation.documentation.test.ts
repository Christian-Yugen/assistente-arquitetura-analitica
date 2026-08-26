import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("GRN-SNAP-006 draft activation", () => {
  it("vincula autorização, golden sintético, calibração, pipeline fail-closed e bloqueio produtivo", () => {
    const gate = readFileSync(resolve(root, "docs/gates/GRN_SNAP_006_DRAFT_CALIBRATION_001.md"), "utf8");
    const reconstruction = readFileSync(resolve(root, "docs/gates/GRN_SNAP_006_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");
    const intake = JSON.parse(readFileSync(resolve(root, "artifacts/intake/GRN-SNAP-006.json"), "utf8"));
    const manifest = JSON.parse(readFileSync(resolve(root, "artifacts/golden/grn-snap-draft-golden-v1.manifest.json"), "utf8"));

    expect(reconstruction).toContain("Chris — “sim”");
    expect(gate).toContain("tp=1");
    expect(gate).toContain("fp=0");
    expect(gate).toContain("fn=0");
    expect(gate).toContain("independent_snapshot_signal_count=0");
    expect(gate).toContain("Produção permanece bloqueada");
    expect(intake.authorization.implementation_authorized).toBe(true);
    expect(intake.execution_profile).toBe("draft");
    expect(intake.production_blocked).toBe(true);
    expect(manifest.calibration).toEqual({ tp: 1, fp: 0, fn: 0 });
    expect(manifest.production_authorized).toBe(false);
  });
});
