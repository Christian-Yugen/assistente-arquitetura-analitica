import { describe, expect, it, vi } from "vitest";

const calls = vi.hoisted(() => ({
  createProject: vi.fn(), updateProject: vi.fn(), createFile: vi.fn(), nextVersion: vi.fn(), createDiagnostic: vi.fn(), removeReference: vi.fn(),
}));

vi.mock("./db", () => ({
  createAnalysisProject: calls.createProject,
  updateAnalysisProjectStatus: calls.updateProject,
  createAnalysisFile: calls.createFile,
  getNextDiagnosticVersion: calls.nextVersion,
  createAnalysisDiagnostic: calls.createDiagnostic,
  markFileReferenceRemoved: calls.removeReference,
  listAnalysisProjectsForOwner: vi.fn(),
  getAnalysisDiagnosticForOwner: vi.fn(),
}));
vi.mock("./storage", () => ({ storagePut: vi.fn().mockResolvedValue({ key: "private/generated.xlsx", url: "/manus-storage/private/generated.xlsx" }) }));
vi.mock("./analysisPipeline", () => ({
  UploadValidationError: class UploadValidationError extends Error {},
  validateWorkbookUpload: vi.fn().mockReturnValue({ buffer: Buffer.from([0x50, 0x4b, 0x03, 0x04]), originalName: "arquivo.xlsx", mimeType: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", sha256: "a".repeat(64) }),
  inspectWorkbookBeforePersistence: vi.fn().mockResolvedValue({ sheetCount: 1 }),
  buildWorkbookMetadata: vi.fn().mockReturnValue({}),
  executeWorkbookEngine: vi.fn().mockResolvedValue({ analysis: { status: "completed_with_warnings" }, execution: { engine_version: "0.1.0", ruleset_version: "0.7.0-draft" } }),
}));

import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";

describe("analysis router flow", () => {
  it("persists every resource with the authenticated owner and removes the private reference after diagnosis", async () => {
    calls.nextVersion.mockResolvedValue(1);
    const user = { id: 77, openId: "owner-77", email: null, name: null, loginMethod: "manus", role: "user" as const, createdAt: new Date(), updatedAt: new Date(), lastSignedIn: new Date() };
    const caller = appRouter.createCaller({ user, req: {} as TrpcContext["req"], res: {} as TrpcContext["res"] });
    const result = await caller.analysis.analyzeWorkbook({ projectName: "Projeto", objective: "Objetivo", fileName: "arquivo.xlsx", mimeType: "application/octet-stream", dataBase64: "UEsDBA==" });

    expect(result.version).toBe(1);
    expect(calls.createProject.mock.calls[0][0]).toMatchObject({ ownerId: 77, name: "Projeto" });
    expect(calls.createFile.mock.calls[0][0]).toMatchObject({ ownerId: 77, retentionStatus: "private_active" });
    expect(calls.createDiagnostic.mock.calls[0][0]).toMatchObject({ ownerId: 77, version: 1 });
    expect(calls.removeReference).toHaveBeenCalledWith(expect.any(String), 77);
    expect(calls.updateProject).toHaveBeenLastCalledWith(expect.any(String), 77, "completed");
  });
});
