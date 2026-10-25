import { describe, expect, it } from "vitest";
import { getModelingGuidance } from "./modelingGuidance";

describe("getModelingGuidance", () => {
  it("converts only allowlisted structural types into safe modeling guidance", () => {
    const guidance = getModelingGuidance({
      sheets: [{ name: "Planilha confidencial", classification: { type: "dimension_standard_candidate", confidence: 0.8 }, grain: { type: "entity_per_row_candidate", confidence: 0.8 }, columns: [{ name: "Cliente privado" }] }, { classification: { type: "fact_transactional_candidate", confidence: 0.7 } }],
      relationships: [{ relationship_type: "one_to_many_relationship_candidate", confidence: 0.7, source: { entity_id: "segredo" } }],
      metrics: [{ metric_type: "sum_conceptual_metric_candidate", confidence: 0.6, conceptual_formula: "SUM([DADO_PRIVADO])" }],
      semantic_classifications: [{ semantic_type: "date_generic", confidence: 0.7, affected_entities: [{ entity_id: "segredo" }] }],
    });

    expect(guidance.dimensions[0]).toMatchObject({ label: "Dimensão candidata", count: 1, confidence: 0.8 });
    expect(guidance.facts[0]).toMatchObject({ label: "Fato transacional candidato", count: 1 });
    expect(guidance.relationships[0]).toMatchObject({ label: "Relação um-para-muitos candidata", count: 1 });
    expect(guidance.metrics[0]).toMatchObject({ label: "Soma candidata", formula: "SUM(eligible_measure)" });
    expect(guidance.grains[0]).toMatchObject({ label: "Uma entidade por linha" });
    expect(guidance.semanticSignals[0]).toMatchObject({ label: "Possível data" });
    expect(JSON.stringify(guidance)).not.toContain("Planilha confidencial");
    expect(JSON.stringify(guidance)).not.toContain("Cliente privado");
    expect(JSON.stringify(guidance)).not.toContain("DADO_PRIVADO");
  });

  it("keeps every category empty when the payload has no supported hypothesis", () => {
    const guidance = getModelingGuidance({ sheets: [{ classification: { type: "unknown", confidence: 1 } }], relationships: [{ relationship_type: "unknown" }], metrics: [{ metric_type: "unknown" }] });
    expect(guidance).toEqual({ dimensions: [], facts: [], structuralReviews: [], grains: [], relationships: [], metrics: [], semanticSignals: [] });
  });

  it("keeps a supported grain hypothesis when table classification remains undefined", () => {
    const guidance = getModelingGuidance({ sheets: [{ grain: { type: "event_per_row_candidate", confidence: 0.65 } }] });
    expect(guidance.grains).toMatchObject([{ label: "Um evento por linha", confidence: 0.65, count: 1 }]);
    expect(guidance.dimensions).toEqual([]);
    expect(guidance.facts).toEqual([]);
  });
});
