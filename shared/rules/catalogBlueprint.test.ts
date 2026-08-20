import { describe, expect, it } from "vitest";
import { OFFICIAL_CATALOG_RULES } from "./officialCatalog";
import { CATALOG_BLUEPRINT, CATALOG_BLUEPRINT_ID, CATALOG_BLUEPRINT_VERSION, buildCatalogBlueprint, summarizeCatalogBlueprint } from "./catalogBlueprint";

describe("catalogBlueprint", () => {
  it("imports all 95 official IDs, titles, stages and source states without omission", () => {
    const slots = buildCatalogBlueprint();
    expect(slots).toHaveLength(95);
    expect(slots.map(slot => [slot.ruleId, slot.name, slot.stage, slot.sourceImplementationStatus])).toEqual(
      OFFICIAL_CATALOG_RULES.map(rule => [rule.ruleId, rule.title, rule.stage, rule.implementationStatus]),
    );
    expect(new Set(slots.map(slot => slot.ruleId)).size).toBe(95);
  });

  it("uses all official namespaces and preserves the 95-rule distribution", () => {
    expect(summarizeCatalogBlueprint()).toEqual([
      { category: "QLT", total: 15, baseline: 6, authorized: 1, references: 0, reserved: 8 },
      { category: "SEM", total: 15, baseline: 0, authorized: 0, references: 1, reserved: 14 },
      { category: "GRN", total: 10, baseline: 0, authorized: 0, references: 1, reserved: 9 },
      { category: "MDL", total: 20, baseline: 0, authorized: 0, references: 1, reserved: 19 },
      { category: "REL", total: 10, baseline: 0, authorized: 0, references: 1, reserved: 9 },
      { category: "MET", total: 15, baseline: 0, authorized: 0, references: 1, reserved: 14 },
      { category: "ALT", total: 10, baseline: 0, authorized: 0, references: 1, reserved: 9 },
    ]);
  });

  it("distinguishes current quality work from official reference rules without activating either silently", () => {
    const slots = buildCatalogBlueprint();
    expect(slots.find(slot => slot.ruleId === "QLT-CATVAR-008")).toMatchObject({
      name: "Variações de categoria", lifecycle: "reserved_definition", sourceImplementationStatus: "planned",
    });
    expect(slots.find(slot => slot.ruleId === "SEM-DATE-001")).toMatchObject({
      name: "Data genérica", lifecycle: "reference_catalog_draft", sourceImplementationStatus: "reference_implemented_draft",
    });
    expect(slots.find(slot => slot.ruleId === "MDL-FACTPER-001")).toMatchObject({
      name: "Fato periódica", lifecycle: "reference_catalog_draft", sourceImplementationStatus: "reference_implemented_draft",
    });
    expect(slots.find(slot => slot.ruleId === "QLT-NUMTEXT-007")).toMatchObject({
      lifecycle: "authorized_to_specify", name: "Números armazenados como texto",
    });
  });

  it("versions the projection and keeps every rule definition controlled", () => {
    expect(CATALOG_BLUEPRINT).toMatchObject({
      blueprintId: CATALOG_BLUEPRINT_ID, blueprintVersion: CATALOG_BLUEPRINT_VERSION, diagnosisContractVersion: "1.0.0", status: "frozen_structure",
    });
    for (const slot of CATALOG_BLUEPRINT.slots) {
      expect(slot.definition).toMatchObject({
        objective: slot.sourcePurpose,
        condition: null,
        inputs: [],
        exclusions: [],
        precedence: { executesAfterRuleIds: [], conflictsWithRuleIds: [], supersedesRuleIds: [] },
        tests: { unit: [], interaction: [], regression: [] },
      });
    }
  });
});
