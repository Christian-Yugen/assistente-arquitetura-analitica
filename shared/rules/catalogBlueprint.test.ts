import { describe, expect, it } from "vitest";
import {
  CATALOG_BLUEPRINT,
  CATALOG_BLUEPRINT_ID,
  CATALOG_BLUEPRINT_VERSION,
  buildCatalogBlueprint,
  summarizeCatalogBlueprint,
} from "./catalogBlueprint";

describe("catalogBlueprint", () => {
  it("freezes exactly 95 unique slots in the approved category distribution", () => {
    const slots = buildCatalogBlueprint();
    const summary = summarizeCatalogBlueprint(slots);

    expect(slots).toHaveLength(95);
    expect(new Set(slots.map(slot => slot.ruleId)).size).toBe(95);
    expect(summary).toEqual([
      { category: "QLT", total: 15, baseline: 6, authorized: 1, reserved: 8 },
      { category: "SEM", total: 15, baseline: 0, authorized: 0, reserved: 15 },
      { category: "FDM", total: 20, baseline: 0, authorized: 0, reserved: 20 },
      { category: "REL", total: 10, baseline: 0, authorized: 0, reserved: 10 },
      { category: "MET", total: 15, baseline: 0, authorized: 0, reserved: 15 },
      { category: "ALT", total: 10, baseline: 0, authorized: 0, reserved: 10 },
      { category: "GRN", total: 10, baseline: 0, authorized: 0, reserved: 10 },
    ]);
  });

  it("versions the canonical artifact and gives every slot a controlled definition structure", () => {
    expect(CATALOG_BLUEPRINT).toMatchObject({
      blueprintId: CATALOG_BLUEPRINT_ID,
      blueprintVersion: CATALOG_BLUEPRINT_VERSION,
      diagnosisContractVersion: "1.0.0",
      status: "frozen_structure",
    });

    for (const slot of CATALOG_BLUEPRINT.slots) {
      expect(slot.definition).toMatchObject({
        inputs: [],
        condition: null,
        exclusions: [],
        evidenceTemplates: [],
        outcomes: [],
        precedence: {
          executesAfterRuleIds: [],
          conflictsWithRuleIds: [],
          supersedesRuleIds: [],
        },
        dependencies: {
          requiresRuleLoadedIds: [],
          requiresRuleFiredIds: [],
          requiresStagesCompleted: [],
          requiresContextPaths: [],
        },
        tests: { unit: [], interaction: [], regression: [] },
        goldenDatasetExpectation: {
          datasetIds: [],
          expectedFindings: [],
          expectedSeverity: [],
          expectedQuestions: [],
        },
      });
    }
  });

  it("preserves the baseline and authorizes only QLT-007 for specification", () => {
    const slots = buildCatalogBlueprint();

    expect(slots.find(slot => slot.ruleId === "QLT-006")).toMatchObject({
      lifecycle: "baseline_draft",
      name: "Datas inválidas em coluna temporal",
    });
    expect(slots.find(slot => slot.ruleId === "QLT-007")).toMatchObject({
      lifecycle: "authorized_to_specify",
      name: "Valores numéricos armazenados como texto",
    });
    expect(slots.find(slot => slot.ruleId === "QLT-008")).toMatchObject({
      lifecycle: "reserved_definition",
      name: null,
    });
  });
});
