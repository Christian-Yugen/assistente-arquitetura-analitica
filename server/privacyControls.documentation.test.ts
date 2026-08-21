import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const controlsPath = resolve(import.meta.dirname, "../docs/security/PRIVACY_CONTROLS_001.md");

describe("PRIVACY-CONTROLS-001 audit trail", () => {
  it("documents real XLSX validation and the bounded retention exception", () => {
    const controls = readFileSync(controlsPath, "utf8");

    expect(controls).toContain("`inspectWorkbookBeforePersistence`");
    expect(controls).toContain("`engine.workbook_validator`");
    expect(controls).toContain("`openpyxl.load_workbook");
    expect(controls).toContain("ZIP com extensão e MIME de XLSX, mas não legível como workbook, é rejeitado");
    expect(controls).toContain("`RETENTION-EXCEPTION-001`");
    expect(controls).toContain("aceita por Chris exclusivamente para o MVP draft");
    expect(controls).toContain("não autoriza produção");
    expect(controls).toContain("operação oficial de exclusão física");
  });
});
