import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const docsRoot = resolve(import.meta.dirname, "../docs");

const documentationSet = [
  ["README.md", "MVP draft"],
  ["architecture/MVP_DRAFT_ARCHITECTURE_001.md", "engine.workbook_validator"],
  ["architecture/CONTRACT_AND_EXECUTOR_001.md", "PM-MVP-PBI-CON-001"],
  ["governance/RULE_DEVELOPMENT_LIFECYCLE_001.md", "QLT-NUMTEXT-007"],
  ["api/ANALYSIS_TRPC_API_001.md", "analysis.analyzeWorkbook"],
  ["testing/TEST_STRATEGY_001.md", "pnpm test:engine"],
  ["user/MANUAL_DO_USUARIO_MVP_DRAFT_001.md", "Exportação JSON"],
] as const;

describe("conjunto documental do MVP draft", () => {
  it("mantém a referência verificável de arquitetura, contrato, regras, API, testes e uso", () => {
    for (const [relativePath, requiredText] of documentationSet) {
      const documentPath = resolve(docsRoot, relativePath);
      expect(existsSync(documentPath), relativePath).toBe(true);
      expect(readFileSync(documentPath, "utf8"), relativePath).toContain(requiredText);
    }
  });
});
