export const ANSWER_DECISIONS = ["confirmed", "needs_data_correction", "needs_business_review", "not_applicable"] as const;
export type AnswerDecision = (typeof ANSWER_DECISIONS)[number];

export function questionIdsFromDiagnostic(payload: unknown): string[] {
  if (!payload || typeof payload !== "object") return [];
  const questions = (payload as { questions?: unknown }).questions;
  if (!Array.isArray(questions)) return [];
  return questions.flatMap(question => {
    if (!question || typeof question !== "object") return [];
    const id = (question as { question_id?: unknown }).question_id;
    return typeof id === "string" && id.length > 0 && id.length <= 80 ? [id] : [];
  });
}

export function answerDecisionFromStoredValue(value: unknown): AnswerDecision | null {
  if (!value || typeof value !== "object") return null;
  const decision = (value as { decision?: unknown }).decision;
  return typeof decision === "string" && (ANSWER_DECISIONS as readonly string[]).includes(decision) ? decision as AnswerDecision : null;
}
