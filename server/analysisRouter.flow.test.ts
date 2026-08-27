import { beforeEach, describe, expect, it, vi } from "vitest";

const calls = vi.hoisted(() => {
  const files = new Map<string, Record<string, unknown>>();
  return {
    files,
    createProject: vi.fn(),
    updateProject: vi.fn().mockResolvedValue(undefined),
    createFile: vi.fn(async (input: Record<string, unknown>) => { files.set(String(input.id), { ...input }); }),
    nextVersion: vi.fn(),
    createDiagnostic: vi.fn(),
    removeReference: vi.fn(async (fileId: string, ownerId: number) => {
      const file = files.get(fileId);
      if (!file || file.ownerId !== ownerId) return;
      files.set(fileId, { ...file, storageKey: null, retentionStatus: "reference_removed", referenceRemovedAt: new Date() });
    }),
    executeEngine: vi.fn(),
  };
});

const safeDiagnosis = {
  analysis: { status: "completed_with_warnings" },
  execution: { engine_version: "0.1.0", ruleset_version: "0.7.0-draft" },
  sheets: [{ sheet_id: "sheet-1", name: "Aba 1", position: 0, visibility: "visible" }],
};

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
vi.mock("./analysisPipeline", async importOriginal => {
  const actual = await importOriginal<typeof import("./analysisPipeline")>();
  return {
    ...actual,
    inspectWorkbookBeforePersistence: vi.fn().mockResolvedValue({ sheetCount: 1 }),
    executeWorkbookEngine: calls.executeEngine,
  };
});

import { appRouter } from "./routers";
import { WorkbookEngineError } from "./analysisPipeline";
import type { TrpcContext } from "./_core/context";

describe("analysis router flow", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    calls.files.clear();
    calls.executeEngine.mockResolvedValue(safeDiagnosis);
  });

  it("persists every resource with the authenticated owner and removes the private reference after diagnosis", async () => {
    calls.nextVersion.mockResolvedValue(1);
    const user = { id: 77, openId: "owner-77", email: null, name: null, loginMethod: "manus", role: "user" as const, createdAt: new Date(), updatedAt: new Date(), lastSignedIn: new Date() };
    const caller = appRouter.createCaller({ user, req: {} as TrpcContext["req"], res: {} as TrpcContext["res"] });
    const result = await caller.analysis.analyzeWorkbook({ projectName: "Nome: Ana Maria; CPF 123.456.789-09", objective: "Contatar ana.maria@example.com", fileName: "cliente.ana@example.com.xlsx", mimeType: "application/octet-stream", dataBase64: "UEsDBA==" });

    expect(result.version).toBe(1);
    const persistedProject = calls.createProject.mock.calls[0][0];
    const persistedFile = calls.createFile.mock.calls[0][0];
    const engineMetadata = calls.executeEngine.mock.calls[0][1];
    const persistedDiagnostic = calls.createDiagnostic.mock.calls[0][0];
    expect(persistedProject).toMatchObject({ ownerId: 77, name: "Nome: [nome mascarado]; CPF [CPF mascarado]" });
    expect(persistedFile).toMatchObject({ ownerId: 77, retentionStatus: "private_active" });
    expect(persistedFile.originalName).not.toContain("ana@example.com");
    expect(JSON.stringify(engineMetadata)).not.toContain("Ana Maria");
    expect(JSON.stringify(engineMetadata)).not.toContain("ana.maria@example.com");
    expect(JSON.stringify(engineMetadata)).not.toContain("123.456.789-09");
    expect(persistedDiagnostic).toMatchObject({ ownerId: 77, version: 1 });
    const persistedPayload = JSON.stringify(persistedDiagnostic.payload);
    for (const rawValue of ["Ana Maria", "123.456.789-09", "ana.maria@example.com", "Nome: Ana Maria", "Vendas RH"]) {
      expect(persistedPayload).not.toContain(rawValue);
    }
    expect(calls.removeReference).toHaveBeenCalledWith(expect.any(String), 77);
    expect(calls.updateProject).toHaveBeenLastCalledWith(expect.any(String), 77, "completed");
    const retainedFile = calls.files.get(String(persistedFile.id));
    expect(retainedFile).toMatchObject({ ownerId: 77, storageKey: null, retentionStatus: "reference_removed" });
    expect(retainedFile?.referenceRemovedAt).toBeInstanceOf(Date);
  });

  it("uses a private CSV key when an authenticated owner submits a CSV", async () => {
    calls.nextVersion.mockResolvedValue(1);
    const user = { id: 77, openId: "owner-77", email: null, name: null, loginMethod: "manus", role: "user" as const, createdAt: new Date(), updatedAt: new Date(), lastSignedIn: new Date() };
    const caller = appRouter.createCaller({ user, req: {} as TrpcContext["req"], res: {} as TrpcContext["res"] });
    await caller.analysis.analyzeWorkbook({ projectName: "Projeto", objective: "Objetivo", fileName: "modelo.csv", mimeType: "text/csv", dataBase64: "aWQsdmFsb3IKMSwxMAo=" });

    const storage = await import("./storage");
    expect(storage.storagePut).toHaveBeenCalledWith(expect.stringMatching(/^analysis\/77\/[^/]+\/[^/]+\.csv$/), expect.any(Buffer), "text/csv");
    expect(calls.createFile.mock.calls[0][0]).toMatchObject({ ownerId: 77, mimeType: "text/csv" });
  });

  it("returns a generic error when the engine fails with internal details", async () => {
    calls.executeEngine.mockRejectedValueOnce(new Error("CPF 123.456.789-09 in temporary file"));
    const user = { id: 77, openId: "owner-77", email: null, name: null, loginMethod: "manus", role: "user" as const, createdAt: new Date(), updatedAt: new Date(), lastSignedIn: new Date() };
    const caller = appRouter.createCaller({ user, req: {} as TrpcContext["req"], res: {} as TrpcContext["res"] });

    const error = await caller.analysis.analyzeWorkbook({ projectName: "Projeto", objective: "Objetivo", fileName: "arquivo.xlsx", mimeType: "application/octet-stream", dataBase64: "UEsDBA==" })
      .catch(error => error);

    expect(error).toMatchObject({ code: "INTERNAL_SERVER_ERROR" });
    expect(error.message).toBe("Não foi possível concluir a análise. Código seguro: engine_failed.");
    expect(calls.removeReference).toHaveBeenCalledWith(expect.any(String), 77);
    const persistedFile = calls.createFile.mock.calls[0][0];
    expect(calls.files.get(String(persistedFile.id))).toMatchObject({ storageKey: null, retentionStatus: "reference_removed" });
  });

  it("returns only a sanitized engine code when execution reaches its time limit", async () => {
    calls.executeEngine.mockRejectedValueOnce(new WorkbookEngineError("engine_timeout"));
    const user = { id: 77, openId: "owner-77", email: null, name: null, loginMethod: "manus", role: "user" as const, createdAt: new Date(), updatedAt: new Date(), lastSignedIn: new Date() };
    const caller = appRouter.createCaller({ user, req: {} as TrpcContext["req"], res: {} as TrpcContext["res"] });

    const error = await caller.analysis.analyzeWorkbook({ projectName: "Projeto", objective: "Objetivo", fileName: "arquivo.xlsx", mimeType: "application/octet-stream", dataBase64: "UEsDBA==" })
      .catch(error => error);

    expect(error).toMatchObject({ code: "INTERNAL_SERVER_ERROR" });
    expect(error.message).toBe("Não foi possível concluir o processamento do arquivo. Código seguro: engine_timeout.");
    expect(error.message).not.toContain("arquivo.xlsx");
    expect(calls.removeReference).toHaveBeenCalledWith(expect.any(String), 77);
  });

  it("persists a failed diagnostic with reference removal and marks the project as failed", async () => {
    calls.nextVersion.mockResolvedValue(1);
    calls.executeEngine.mockResolvedValueOnce({ ...safeDiagnosis, analysis: { status: "failed" } });
    const user = { id: 77, openId: "owner-77", email: null, name: null, loginMethod: "manus", role: "user" as const, createdAt: new Date(), updatedAt: new Date(), lastSignedIn: new Date() };
    const caller = appRouter.createCaller({ user, req: {} as TrpcContext["req"], res: {} as TrpcContext["res"] });

    const result = await caller.analysis.analyzeWorkbook({ projectName: "Projeto", objective: "Objetivo", fileName: "arquivo.xlsx", mimeType: "application/octet-stream", dataBase64: "UEsDBA==" });

    expect(result.version).toBe(1);
    expect(calls.createDiagnostic.mock.calls[0][0]).toMatchObject({ ownerId: 77, status: "failed" });
    expect(calls.removeReference).toHaveBeenCalledWith(expect.any(String), 77);
    expect(calls.updateProject).toHaveBeenLastCalledWith(expect.any(String), 77, "failed");
  });

  it.each([
    ["CPF", { ...safeDiagnosis, evidence: "CPF 123.456.789-09" }],
    ["e-mail", { ...safeDiagnosis, evidence: "ana.maria@example.com" }],
    ["nome rotulado", { ...safeDiagnosis, evidence: "Nome: Ana Maria" }],
    ["título bruto de aba", { ...safeDiagnosis, sheets: [{ name: "Vendas RH" }] }],
  ])("blocks a diagnosis with %s before diagnostic persistence", async (_label, diagnosis) => {
    calls.nextVersion.mockResolvedValue(1);
    calls.executeEngine.mockResolvedValueOnce(diagnosis);
    const user = { id: 77, openId: "owner-77", email: null, name: null, loginMethod: "manus", role: "user" as const, createdAt: new Date(), updatedAt: new Date(), lastSignedIn: new Date() };
    const caller = appRouter.createCaller({ user, req: {} as TrpcContext["req"], res: {} as TrpcContext["res"] });
    const error = await caller.analysis.analyzeWorkbook({ projectName: "Projeto", objective: "Objetivo", fileName: "arquivo.xlsx", mimeType: "application/octet-stream", dataBase64: "UEsDBA==" })
      .catch(error => error);

    expect(error.message).toBe("Não foi possível concluir a análise. Código seguro: privacy_failed.");
    expect(calls.createDiagnostic).not.toHaveBeenCalled();
    expect(calls.removeReference).toHaveBeenCalledWith(expect.any(String), 77);
  });
});
