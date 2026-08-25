import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (relativePath: string) => fs.readFileSync(path.join(root, relativePath), "utf8");

describe("REL-ONEMANY-001 draft activation governance", () => {
  it("records Chris's authorization, calibration evidence, and controlled draft status", () => {
    const intake = read("artifacts/intake/REL-ONEMANY-001.json");
    const manifest = read("artifacts/golden/rel-onemany-draft-golden-v1.manifest.json");
    const calibrationGate = read("docs/gates/REL_ONEMANY_001_DRAFT_CALIBRATION_001.md");

    expect(intake).toContain('"status": "executable_draft"');
    expect(intake).toContain('"implementation_authorized": true');
    expect(intake).toContain('"implementation_authorized_by": "Chris"');
    expect(intake).toContain('"calibration_gate": "REL-ONEMANY-001-DRAFT-CALIBRATION-001"');
    expect(manifest).toContain('"synthetic_only": true');
    expect(manifest).toContain('"expected_positive_count": 3');
    expect(calibrationGate).toContain("3 verdadeiros positivos, 0 falsos positivos e 0 falsos negativos");
    expect(calibrationGate).toContain("produção permanece bloqueada");
  });

  it("preserves opacity, independent privacy controls, and human confirmation", () => {
    const policy = read("docs/rules/REL_ONEMANY_001_POLICY_PROPOSAL_001.md");
    const calibrationGate = read("docs/gates/REL_ONEMANY_001_DRAFT_CALIBRATION_001.md");
    const catalog = read("engine/catalog.py");
    const pipeline = read("engine/pipeline/quality_diagnosis.py");

    expect(policy).toContain("títulos de abas, cabeçalhos, valores, posições, pares correspondentes");
    expect(policy).toContain("cardinalidade 1:1, muitos-para-muitos");
    expect(calibrationGate).toContain("SEM-SENS-015");
    expect(calibrationGate).toContain("confirmação humana continua obrigatória");
    expect(catalog).toContain('"REL-ONEMANY-001": "REL-ONEMANY-001-DRAFT-CALIBRATION-001"');
    expect(pipeline).toContain("REL-ONEMANY-001");
  });
});
