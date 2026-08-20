import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const projectRoot = resolve(import.meta.dirname, "..");

function source(relativePath: string) {
  return readFileSync(resolve(projectRoot, relativePath), "utf8");
}

describe("privacy-safe operational logging", () => {
  it("does not emit workbook content or raw errors from the analysis path", () => {
    for (const relativePath of ["server/routers.ts", "server/analysisPipeline.ts", "server/privacy.ts"]) {
      expect(source(relativePath)).not.toMatch(/console\.(?:log|warn|error)\s*\(/);
    }
  });

  it("keeps database operational messages generic when connection or user persistence fails", () => {
    const databaseSource = source("server/db.ts");
    expect(databaseSource).toContain('console.warn("[Database] Failed to initialize connection.")');
    expect(databaseSource).toContain('console.error("[Database] Failed to upsert user.")');
    expect(databaseSource).not.toMatch(/console\.(?:warn|error)\([^\n]*,\s*(?:error|err)\b/);
  });
});
