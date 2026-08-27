import { describe, expect, it } from "vitest";
import { buildWorkbookMetadata, executeWorkbookEngine, inspectWorkbookBeforePersistence, UploadValidationError, validateWorkbookInspection, validateWorkbookUpload, WorkbookInspectionError } from "./analysisPipeline";

const zipHeader = Buffer.from([0x50, 0x4b, 0x03, 0x04, 0x00, 0x00]);
const xlsxMime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
const csvBuffer = Buffer.from("id,valor\n1,10\n2,20\n", "utf8");

describe("validateWorkbookUpload", () => {
  it("accepts an XLSX-shaped payload and returns a safe name and checksum", () => {
    const result = validateWorkbookUpload({ fileName: "../modelo.xlsx", mimeType: xlsxMime, dataBase64: zipHeader.toString("base64") });
    expect(result.originalName).toBe(".._modelo.xlsx");
    expect(result.mimeType).toBe(xlsxMime);
    expect(result.format).toBe("xlsx");
    expect(result.sha256).toMatch(/^[a-f0-9]{64}$/);
  });

  it("accepts an UTF-8 CSV and inspects it as one logical sheet", async () => {
    const result = validateWorkbookUpload({ fileName: "../modelo.csv", mimeType: "text/csv", dataBase64: csvBuffer.toString("base64") });
    expect(result.originalName).toBe(".._modelo.csv");
    expect(result.mimeType).toBe("text/csv");
    expect(result.format).toBe("csv");
    await expect(inspectWorkbookBeforePersistence(result)).resolves.toEqual({ sheetCount: 1 });
  });

  it("accepts a Windows-1252 CSV exported by local spreadsheet software", async () => {
    const cp1252Csv = Buffer.from([0x69, 0x64, 0x3b, 0x64, 0x65, 0x73, 0x63, 0x72, 0x69, 0xe7, 0xe3, 0x6f, 0x0a, 0x31, 0x3b, 0x61, 0x74, 0x69, 0x76, 0x6f, 0x0a]);
    const result = validateWorkbookUpload({ fileName: "modelo.csv", mimeType: "text/csv", dataBase64: cp1252Csv.toString("base64") });

    await expect(inspectWorkbookBeforePersistence(result)).resolves.toEqual({ sheetCount: 1 });
  });

  it("executes CSV through temporary normalization and returns only a sanitized diagnosis", async () => {
    const workbook = validateWorkbookUpload({ fileName: "modelo.csv", mimeType: "text/csv", dataBase64: csvBuffer.toString("base64") });
    const diagnosis = await executeWorkbookEngine(workbook, buildWorkbookMetadata({
      analysisId: "00000000-0000-4000-8000-000000000001", projectId: "00000000-0000-4000-8000-000000000002", ownerNumericId: 42,
      projectName: "Projeto", objective: "Objetivo", fileId: "00000000-0000-4000-8000-000000000003", workbook,
    }));
    expect((diagnosis.file as Record<string, unknown>).sheet_count).toBe(1);
    expect((diagnosis.analysis as Record<string, unknown>).status).toBeDefined();
    expect(JSON.stringify(diagnosis)).not.toContain("id,valor");
  });

  it.each([
    { label: "wrong extension", input: { fileName: "modelo.xls", mimeType: xlsxMime, dataBase64: zipHeader.toString("base64") } },
    { label: "invalid base64", input: { fileName: "modelo.xlsx", mimeType: xlsxMime, dataBase64: "%%%" } },
    { label: "not zip signature", input: { fileName: "modelo.xlsx", mimeType: xlsxMime, dataBase64: Buffer.from("not a zip").toString("base64") } },
    { label: "wrong mime", input: { fileName: "modelo.xlsx", mimeType: "text/csv", dataBase64: zipHeader.toString("base64") } },
    { label: "CSV with XLSX MIME", input: { fileName: "modelo.csv", mimeType: xlsxMime, dataBase64: csvBuffer.toString("base64") } },
  ])("rejects $label", ({ input }) => {
    expect(() => validateWorkbookUpload(input)).toThrow(UploadValidationError);
  });

  it("rejects files larger than 25 MB before the engine is invoked", () => {
    const oversized = Buffer.concat([zipHeader, Buffer.alloc(25 * 1024 * 1024)]);
    expect(() => validateWorkbookUpload({ fileName: "modelo.xlsx", mimeType: xlsxMime, dataBase64: oversized.toString("base64") })).toThrow("25 MB");
  });

  it("requires between one and ten sheets before persistence", () => {
    expect(validateWorkbookInspection({ sheet_count: 10 })).toEqual({ sheetCount: 10 });
    expect(() => validateWorkbookInspection({ sheet_count: 0 })).toThrow(UploadValidationError);
    expect(() => validateWorkbookInspection({ sheet_count: 11 })).toThrow(UploadValidationError);
    expect(() => validateWorkbookInspection({ sheet_count: "2" })).toThrow(UploadValidationError);
  });

  it("rejects a ZIP-shaped payload that is not a readable XLSX before persistence", async () => {
    const zipButNotWorkbook = validateWorkbookUpload({
      fileName: "arquivo.xlsx",
      mimeType: xlsxMime,
      dataBase64: zipHeader.toString("base64"),
    });

    await expect(inspectWorkbookBeforePersistence(zipButNotWorkbook)).rejects.toMatchObject({
      failureCode: "inspection_workbook_invalid",
    } satisfies Partial<WorkbookInspectionError>);
  });

  it("returns a sanitized workbook failure code when a ZIP-shaped XLSX cannot be processed", async () => {
    const zipButNotWorkbook = validateWorkbookUpload({
      fileName: "arquivo.xlsx",
      mimeType: xlsxMime,
      dataBase64: zipHeader.toString("base64"),
    });

    await expect(executeWorkbookEngine(zipButNotWorkbook, buildWorkbookMetadata({
      analysisId: "00000000-0000-4000-8000-000000000011", projectId: "00000000-0000-4000-8000-000000000012", ownerNumericId: 42,
      projectName: "Projeto", objective: "Objetivo", fileId: "00000000-0000-4000-8000-000000000013", workbook: zipButNotWorkbook,
    }))).rejects.toMatchObject({ failureCode: "engine_workbook_invalid" });
  });

  it("rejects CSV with invalid encoding or divergent fields before persistence", async () => {
    const nonUtf8 = validateWorkbookUpload({ fileName: "arquivo.csv", mimeType: "text/csv", dataBase64: Buffer.from([0x69, 0x64, 0x2c, 0x81]).toString("base64") });
    const divergent = validateWorkbookUpload({ fileName: "arquivo.csv", mimeType: "text/csv", dataBase64: Buffer.from("id,valor\n1,2,3\n").toString("base64") });
    await expect(inspectWorkbookBeforePersistence(nonUtf8)).rejects.toMatchObject({ failureCode: "inspection_csv_invalid" } satisfies Partial<WorkbookInspectionError>);
    await expect(inspectWorkbookBeforePersistence(divergent)).rejects.toMatchObject({ failureCode: "inspection_csv_invalid" } satisfies Partial<WorkbookInspectionError>);
  });

  it("builds deterministic pseudonymous metadata that separates owners", () => {
    const workbook = validateWorkbookUpload({ fileName: "modelo.xlsx", mimeType: xlsxMime, dataBase64: zipHeader.toString("base64") });
    const metadata = buildWorkbookMetadata({ analysisId: "a", projectId: "p", ownerNumericId: 42, projectName: "Projeto", objective: "Objetivo", fileId: "f", workbook });
    const sameOwner = buildWorkbookMetadata({ analysisId: "a", projectId: "p", ownerNumericId: 42, projectName: "Projeto", objective: "Objetivo", fileId: "f", workbook });
    const anotherOwner = buildWorkbookMetadata({ analysisId: "a", projectId: "p", ownerNumericId: 43, projectName: "Projeto", objective: "Objetivo", fileId: "f", workbook });
    expect(metadata.owner_user_id).toMatch(/^[0-9a-f-]{36}$/);
    expect(metadata.owner_user_id).toBe(sameOwner.owner_user_id);
    expect(metadata.owner_user_id).not.toBe(anotherOwner.owner_user_id);
    expect(metadata.retention_status).toBe("reference_removed");
  });

  it("masks sensitive text in workbook-facing metadata and filename labels", () => {
    const workbook = validateWorkbookUpload({
      fileName: "cliente.ana@example.com.xlsx",
      mimeType: xlsxMime,
      dataBase64: zipHeader.toString("base64"),
    });
    const metadata = buildWorkbookMetadata({
      analysisId: "a",
      projectId: "p",
      ownerNumericId: 42,
      projectName: "Nome: Ana Maria; CPF 123.456.789-09",
      objective: "Contatar ana.maria@example.com para validar o modelo",
      fileId: "f",
      workbook,
    });

    expect(workbook.originalName).not.toContain("ana@example.com");
    expect(metadata.project_name).toContain("[nome mascarado]");
    expect(metadata.project_name).not.toContain("Ana Maria");
    expect(metadata.project_name).not.toContain("123.456.789-09");
    expect(metadata.objective).toContain("[e-mail mascarado]");
    expect(metadata.objective).not.toContain("ana.maria@example.com");
  });
});
