import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("GRN-ASSOC-007 draft activation", () => {
  it("vincula autorização, golden sintético, calibração, pipeline fail-closed e bloqueio produtivo", () => {
    const gate = readFileSync(resolve(root, "docs/gates/GRN_ASSOC_007_DRAFT_CALIBRATION_001.md"), "utf8");
    const reconstruction = readFileSync(resolve(root, "docs/gates/GRN_ASSOC_007_RECONSTRUCTION_AUTHORIZATION_001.md"), "utf8");
    const intake = JSON.parse(readFileSync(resolve(root, "artifacts/intake/GRN-ASSOC-007.json"), "utf8"));
    const manifest = JSON.parse(readFileSync(resolve(root, "artifacts/golden/grn-assoc-draft-golden-v1.manifest.json"), "utf8"));

    expect(reconstruction).toContain("Chris — “autorizado”");
    expect(gate).toContain("tp=1");
    expect(gate).toContain("fp=0");
    expect(gate).toContain("fn=0");
    expect(gate).toContain("independent_association_signal_count=0");
    expect(gate).toContain("Produção permanece bloqueada");
    expect(intake.authorization.implementation_authorized).toBe(true);
    expect(intake.execution_profile).toBe("draft");
    expect(intake.production_blocked).toBe(true);
    expect(manifest.calibration).toEqual({ tp: 1, fp: 0, fn: 0 });
    expect(manifest.production_authorized).toBe(false);
  });
});

