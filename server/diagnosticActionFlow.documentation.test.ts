import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

describe("diagnostic action flow contract", () => {
  it("permite somente decisões enumeradas e preserva o bloqueio de produção", () => {
    const document = readFileSync(resolve(import.meta.dirname, "../docs/gates/DIAGNOSTIC_ACTION_FLOW_001.md"), "utf8");
    expect(document).toContain("`confirmed`");
    expect(document).toContain("`needs_data_correction`");
    expect(document).toContain("`needs_business_review`");
    expect(document).toContain("`not_applicable`");
    expect(document).toContain("Não haverá campo livre");
    expect(document).toContain("ID da pergunta existe no payload daquele diagnóstico");
    expect(document).toContain("não torna um arquivo automaticamente utilizável para produção");
  });
});
