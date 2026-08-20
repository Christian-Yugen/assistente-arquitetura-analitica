import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const inventoryPath = resolve(import.meta.dirname, "../docs/checkpoints/INVENTARIO_QLT_001_006.md");

describe("inventário QLT-001 a QLT-006", () => {
  it("mantém IDs, versões, dependências, outcomes e a ressalva de linhagem da regra de nulos", () => {
    const inventory = readFileSync(inventoryPath, "utf8");

    for (const ruleId of ["QLT-NULL-001", "QLT-DUP-002", "QLT-EMPTYCOL-003", "QLT-EMPTYROW-004", "QLT-MIXTYPE-005", "QLT-BADDATE-006"]) {
      expect(inventory).toContain(ruleId);
    }
    expect(inventory).toContain("Versão lógica no ruleset");
    expect(inventory).toContain("Dependência de estágio");
    expect(inventory).toContain("Outcomes verificados");
    expect(inventory).toContain("não serve para comprovar os outcomes ou as dependências da baseline v0.6.0");
  });
});
