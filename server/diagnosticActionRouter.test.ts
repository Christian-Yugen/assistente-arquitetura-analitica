import { beforeEach, describe, expect, it, vi } from "vitest";

const calls = vi.hoisted(() => ({
  getDiagnostic: vi.fn(),
  listAnswers: vi.fn(),
  upsertAnswer: vi.fn(),
}));

vi.mock("./db", () => ({
  getAnalysisDiagnosticForOwner: calls.getDiagnostic,
  listAnalysisAnswersForDiagnostic: calls.listAnswers,
  upsertAnalysisAnswer: calls.upsertAnswer,
  listAnalysisProjectsForOwner: vi.fn(),
  getAnalysisProjectForOwner: vi.fn(),
  createAnalysisProject: vi.fn(),
  updateAnalysisProjectStatus: vi.fn(),
  createAnalysisFile: vi.fn(),
  markFileReferenceRemoved: vi.fn(),
  getNextDiagnosticVersion: vi.fn(),
  createAnalysisDiagnostic: vi.fn(),
}));

import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";

const diagnosticId = "11111111-1111-4111-8111-111111111111";
const projectId = "22222222-2222-4222-8222-222222222222";

function caller(ownerId = 71) {
  return appRouter.createCaller({ user: { id: ownerId, openId: `owner-${ownerId}`, email: null, name: null, loginMethod: "test", role: "user", createdAt: new Date(), updatedAt: new Date(), lastSignedIn: new Date() }, req: {} as TrpcContext["req"], res: {} as TrpcContext["res"] });
}

describe("diagnostic action router", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    calls.getDiagnostic.mockResolvedValue({ id: diagnosticId, projectId, ownerId: 71, payload: { questions: [{ question_id: "q-1" }] } });
    calls.listAnswers.mockResolvedValue([{ questionId: "q-1", answer: { decision: "confirmed" } }]);
    calls.upsertAnswer.mockResolvedValue(undefined);
  });

  it("returns decisions only after owner-scoped diagnostic lookup", async () => {
    const result = await caller().analysis.getActionState({ diagnosticId });
    expect(calls.getDiagnostic).toHaveBeenCalledWith(diagnosticId, 71);
    expect(calls.listAnswers).toHaveBeenCalledWith(diagnosticId, 71);
    expect(result.answers).toEqual([{ questionId: "q-1", decision: "confirmed" }]);
  });

  it("persists only an allowed decision for a question present in the owner diagnostic", async () => {
    const result = await caller().analysis.answerQuestion({ diagnosticId, questionId: "q-1", decision: "needs_data_correction" });
    expect(result).toEqual({ questionId: "q-1", decision: "needs_data_correction" });
    expect(calls.upsertAnswer).toHaveBeenCalledWith(expect.objectContaining({ projectId, ownerId: 71, sourceDiagnosticId: diagnosticId, questionId: "q-1", answer: { decision: "needs_data_correction" } }));
  });

  it("rejects a question that is absent from the owner diagnostic", async () => {
    const error = await caller().analysis.answerQuestion({ diagnosticId, questionId: "q-other", decision: "confirmed" }).catch(error => error);
    expect(error).toMatchObject({ code: "BAD_REQUEST" });
    expect(calls.upsertAnswer).not.toHaveBeenCalled();
  });

  it("rejects an identifier that exceeds the storage contract", async () => {
    const error = await caller().analysis.answerQuestion({ diagnosticId, questionId: "q".repeat(37), decision: "confirmed" }).catch(error => error);
    expect(error).toMatchObject({ code: "BAD_REQUEST" });
    expect(calls.upsertAnswer).not.toHaveBeenCalled();
  });
});
