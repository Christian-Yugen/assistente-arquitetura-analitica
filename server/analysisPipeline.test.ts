import { describe, expect, it } from "vitest";
import { buildWorkbookMetadata, UploadValidationError, validateWorkbookInspection, validateWorkbookUpload } from "./analysisPipeline";

const zipHeader = Buffer.from([0x50, 0x4b, 0x03, 0x04, 0x00, 0x00]);
const xlsxMime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";

describe("validateWorkbookUpload", () => {
  it("accepts an XLSX-shaped payload and returns a safe name and checksum", () => {
    const result = validateWorkbookUpload({ fileName: "../modelo.xlsx", mimeType: xlsxMime, dataBase64: zipHeader.toString("base64") });
    expect(result.originalName).toBe(".._modelo.xlsx");
    expect(result.mimeType).toBe(xlsxMime);
    expect(result.sha256).toMatch(/^[a-f0-9]{64}$/);
  });

  it.each([
    { label: "wrong extension", input: { fileName: "modelo.xls", mimeType: xlsxMime, dataBase64: zipHeader.toString("base64") } },
    { label: "invalid base64", input: { fileName: "modelo.xlsx", mimeType: xlsxMime, dataBase64: "%%%" } },
    { label: "not zip signature", input: { fileName: "modelo.xlsx", mimeType: xlsxMime, dataBase64: Buffer.from("not a zip").toString("base64") } },
    { label: "wrong mime", input: { fileName: "modelo.xlsx", mimeType: "text/csv", dataBase64: zipHeader.toString("base64") } },
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
