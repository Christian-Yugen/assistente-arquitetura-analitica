import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

describe("ANALYSIS-PROCESSING-STATE-001", () => {
  it("preserva a explicação do estado pendente, a ausência de estimativas e os controles bloqueados", () => {
    const document = readFileSync(resolve(process.cwd(), "docs/architecture/ANALYSIS_PROCESSING_STATE_001.md"), "utf8");
    expect(document).toContain("mutation síncrona `analysis.analyzeWorkbook`");
    expect(document).toContain("não apresenta percentual, tempo estimado ou etapas concluídas");
    expect(document).toContain("seria uma simulação enganosa");
    expect(document).toContain("Nome do projeto");
    expect(document).toContain("Seletor de workbook");
    expect(document).toContain("Analisando estrutura…");
  });
});
