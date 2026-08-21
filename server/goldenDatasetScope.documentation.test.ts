import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const scopePath = resolve(import.meta.dirname, "../docs/gates/GOLDEN_DATASET_SCOPE_001.md");

describe("golden dataset calibration scope", () => {
  it("limits calibration to the two governed draft rules and records positive, negative and privacy criteria", () => {
    const scope = readFileSync(scopePath, "utf8");

    expect(scope).toContain("QLT-NUMTEXT-007");
    expect(scope).toContain("QLT-NULL-001@0.1.0-reconstructed.1");
    expect(scope).toContain("Verdadeiro positivo");
    expect(scope).toContain("Verdadeiro negativo");
    expect(scope).toContain("Falso positivo conhecido");
    expect(scope).toContain("Falso negativo conhecido");
    expect(scope).toContain("não contém valores de células");
    expect(scope).toContain("não autoriza promoção de ambiente");
  });
});
