const MINIMUM_MODELING_SAMPLE_SIZE = 10;

type UnknownRecord = Record<string, unknown>;

export type SampleSufficiencyNotice = {
  minimumRequiredRows: number;
  countedSheetCount: number;
  insufficientSheetCount: number;
  minimumObservedRows: number;
  maximumObservedRows: number;
};

function record(value: unknown): UnknownRecord {
  return value && typeof value === "object" ? (value as UnknownRecord) : {};
}

function countArray(payload: UnknownRecord, key: string): number {
  return Array.isArray(payload[key]) ? payload[key].length : 0;
}

export function getSampleSufficiencyNotice(payload: UnknownRecord): SampleSufficiencyNotice | null {
  const sheets = Array.isArray(payload.sheets) ? payload.sheets.map(record) : [];
  const observedRows = sheets
    .map(sheet => sheet.row_count)
    .filter((value): value is number => typeof value === "number" && Number.isFinite(value) && value >= 0);

  const proposedModel = record(payload.proposed_model);
  const hasModelingOutput = countArray(payload, "questions") > 0
    || countArray(payload, "semantic_classifications") > 0
    || countArray(payload, "relationships") > 0
    || countArray(payload, "metrics") > 0
    || countArray(proposedModel, "tables") > 0;

  const insufficientSheetCount = observedRows.filter(rowCount => rowCount < MINIMUM_MODELING_SAMPLE_SIZE).length;
  if (hasModelingOutput || observedRows.length === 0 || insufficientSheetCount === 0) return null;

  return {
    minimumRequiredRows: MINIMUM_MODELING_SAMPLE_SIZE,
    countedSheetCount: observedRows.length,
    insufficientSheetCount,
    minimumObservedRows: Math.min(...observedRows),
    maximumObservedRows: Math.max(...observedRows),
  };
}
