import { describe, expect, it } from "vitest";
import { getSampleSufficiencyNotice } from "./sampleSufficiency";

describe("getSampleSufficiencyNotice", () => {
  it("explica de forma agregada quando nenhuma hipótese foi emitida por amostra curta", () => {
    expect(getSampleSufficiencyNotice({
      sheets: [{ row_count: 6 }, { row_count: 3 }, { row_count: 3 }, { row_count: 3 }],
      questions: [],
      semantic_classifications: [],
      relationships: [],
      metrics: [],
      proposed_model: { tables: [] },
    })).toEqual({
      minimumRequiredRows: 10,
      countedSheetCount: 4,
      insufficientSheetCount: 4,
      minimumObservedRows: 3,
      maximumObservedRows: 6,
    });
  });

  it("não substitui perguntas ou hipóteses já emitidas pelo motor", () => {
    expect(getSampleSufficiencyNotice({
      sheets: [{ row_count: 3 }],
      questions: [{ question_id: "opaque" }],
      semantic_classifications: [],
      relationships: [],
      metrics: [],
      proposed_model: { tables: [] },
    })).toBeNull();
  });

  it("não classifica como insuficiente uma amostra que atingiu o limiar", () => {
    expect(getSampleSufficiencyNotice({
      sheets: [{ row_count: 10 }, { row_count: 14 }],
      questions: [],
      semantic_classifications: [],
      relationships: [],
      metrics: [],
      proposed_model: { tables: [] },
    })).toBeNull();
  });
});
