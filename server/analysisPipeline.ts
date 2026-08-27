import { createHash, randomUUID } from "node:crypto";
import { spawn } from "node:child_process";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { sanitizeSensitiveText, sanitizeWorkbookFileName } from "./privacy";

const MAX_BYTES = 25 * 1024 * 1024;
const XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
const CSV_MIME = "text/csv";
const ACCEPTED_CSV_MIMES = new Set([CSV_MIME, "application/csv", "application/vnd.ms-excel", "application/octet-stream"]);

export class UploadValidationError extends Error {}

export type WorkbookInspectionFailureCode =
  | "inspection_workbook_invalid"
  | "inspection_csv_invalid"
  | "inspection_process_failed";

const INSPECTION_FAILURE_CODES = new Set<WorkbookInspectionFailureCode>([
  "inspection_workbook_invalid",
  "inspection_csv_invalid",
  "inspection_process_failed",
]);

export class WorkbookInspectionError extends UploadValidationError {
  constructor(public readonly failureCode: WorkbookInspectionFailureCode) {
    super(`Não foi possível validar a estrutura do workbook. Código seguro: ${failureCode}.`);
  }
}

export type WorkbookEngineFailureCode =
  | "engine_timeout"
  | "engine_process_failed"
  | "engine_output_invalid"
  | "engine_workbook_invalid"
  | "engine_value_error"
  | "engine_type_error"
  | "engine_key_error"
  | "engine_assertion_error"
  | "engine_unexpected_error";

const ENGINE_FAILURE_CODES = new Set<WorkbookEngineFailureCode>([
  "engine_timeout",
  "engine_process_failed",
  "engine_output_invalid",
  "engine_workbook_invalid",
  "engine_value_error",
  "engine_type_error",
  "engine_key_error",
  "engine_assertion_error",
  "engine_unexpected_error",
]);

export class WorkbookEngineError extends Error {
  constructor(public readonly failureCode: WorkbookEngineFailureCode) {
    super("O motor de análise não concluiu o workbook.");
  }
}

async function readSafeEngineFailureCode(path: string): Promise<WorkbookEngineFailureCode> {
  try {
    const output = JSON.parse(await readFile(path, "utf8")) as { failure_code?: unknown };
    return typeof output.failure_code === "string" && ENGINE_FAILURE_CODES.has(output.failure_code as WorkbookEngineFailureCode)
      ? output.failure_code as WorkbookEngineFailureCode
      : "engine_process_failed";
  } catch {
    return "engine_process_failed";
  }
}

async function readSafeInspectionFailureCode(path: string): Promise<WorkbookInspectionFailureCode> {
  try {
    const output = JSON.parse(await readFile(path, "utf8")) as { failure_code?: unknown };
    return typeof output.failure_code === "string" && INSPECTION_FAILURE_CODES.has(output.failure_code as WorkbookInspectionFailureCode)
      ? output.failure_code as WorkbookInspectionFailureCode
      : "inspection_process_failed";
  } catch {
    return "inspection_process_failed";
  }
}

export type ValidatedWorkbook = { buffer: Buffer; originalName: string; mimeType: string; sha256: string; format: "xlsx" | "csv"; extension: "xlsx" | "csv" };
export { sanitizeSensitiveText } from "./privacy";
export type WorkbookInspection = { sheetCount: number };

const PROJECT_ROOT = fileURLToPath(new URL("../", import.meta.url));
const WORKBOOK_VALIDATOR_PATH = fileURLToPath(new URL("../engine/workbook_validator.py", import.meta.url));

function contractUuid(seed: string): string {
  const hex = createHash("sha256").update(seed).digest("hex");
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-4${hex.slice(13, 16)}-8${hex.slice(17, 20)}-${hex.slice(20, 32)}`;
}

export function validateWorkbookUpload(input: { fileName: string; mimeType: string; dataBase64: string }): ValidatedWorkbook {
  const requestedName = input.fileName.trim().replace(/[\\/\0]/g, "_").slice(0, 255);
  const lowerName = requestedName.toLowerCase();
  const format = lowerName.endsWith(".xlsx") ? "xlsx" : lowerName.endsWith(".csv") ? "csv" : null;
  if (!format) throw new UploadValidationError("Envie arquivos .xlsx ou .csv.");
  const originalName = sanitizeWorkbookFileName(requestedName);
  if (format === "xlsx" && input.mimeType && input.mimeType !== XLSX_MIME && input.mimeType !== "application/octet-stream") {
    throw new UploadValidationError("O tipo informado não corresponde a uma planilha XLSX.");
  }
  if (format === "csv" && input.mimeType && !ACCEPTED_CSV_MIMES.has(input.mimeType)) {
    throw new UploadValidationError("O tipo informado não corresponde a um arquivo CSV.");
  }
  if (!/^[A-Za-z0-9+/]+={0,2}$/.test(input.dataBase64) || input.dataBase64.length % 4 !== 0) {
    throw new UploadValidationError("O conteúdo do upload não está codificado em base64 válido.");
  }
  const buffer = Buffer.from(input.dataBase64, "base64");
  if (!buffer.length || buffer.length > MAX_BYTES) throw new UploadValidationError("O arquivo deve ter entre 1 byte e 25 MB.");
  if (format === "xlsx") {
    const isZip = buffer.length >= 4 && buffer[0] === 0x50 && buffer[1] === 0x4b && [0x03, 0x05, 0x07].includes(buffer[2]) && [0x04, 0x06, 0x08].includes(buffer[3]);
    if (!isZip) throw new UploadValidationError("O conteúdo não possui a assinatura ZIP esperada para XLSX.");
  }
  return { buffer, originalName, mimeType: format === "xlsx" ? XLSX_MIME : CSV_MIME, sha256: createHash("sha256").update(buffer).digest("hex"), format, extension: format };
}

export function validateWorkbookInspection(input: { sheet_count: unknown }): WorkbookInspection {
  if (!Number.isInteger(input.sheet_count) || (input.sheet_count as number) < 1 || (input.sheet_count as number) > 10) {
    throw new UploadValidationError("O workbook deve ter entre 1 e 10 abas antes de ser armazenado.");
  }
  return { sheetCount: input.sheet_count as number };
}

export async function inspectWorkbookBeforePersistence(workbook: ValidatedWorkbook): Promise<WorkbookInspection> {
  const workDir = await mkdtemp(join(tmpdir(), "analytical-workbook-inspection-"));
  const inputPath = join(workDir, `input.${workbook.extension}`);
  const errorPath = join(workDir, "inspection-error.json");
  try {
    await writeFile(inputPath, workbook.buffer);
    const stdout = await new Promise<string>((resolve, reject) => {
      const child = spawn("python3", [WORKBOOK_VALIDATOR_PATH, "--input", inputPath, "--format", workbook.format, "--error-output", errorPath], {
        cwd: PROJECT_ROOT,
        env: { ...process.env, PYTHONPATH: PROJECT_ROOT },
      });
      let output = "";
      const timer = setTimeout(() => child.kill("SIGKILL"), 30_000);
      child.stdout.on("data", chunk => { output += chunk.toString(); });
      child.once("error", () => reject(new WorkbookInspectionError("inspection_process_failed")));
      child.once("close", code => {
        clearTimeout(timer);
        if (code === 0) resolve(output);
        else void readSafeInspectionFailureCode(errorPath).then(failureCode => reject(new WorkbookInspectionError(failureCode)));
      });
    });
    return validateWorkbookInspection(JSON.parse(stdout) as { sheet_count: unknown });
  } finally {
    await rm(workDir, { recursive: true, force: true });
  }
}

export async function executeWorkbookEngine(workbook: ValidatedWorkbook, metadata: Record<string, unknown>) {
  const workDir = await mkdtemp(join(tmpdir(), "analytical-workbook-"));
  const inputPath = join(workDir, `input.${workbook.extension}`);
  const metadataPath = join(workDir, "metadata.json");
  const outputPath = join(workDir, "diagnosis.json");
  const errorPath = join(workDir, "engine-error.json");
  try {
    await Promise.all([writeFile(inputPath, workbook.buffer), writeFile(metadataPath, JSON.stringify(metadata))]);
    await new Promise<void>((resolve, reject) => {
      const child = spawn("python3", ["-m", "engine.workbook_runner", "--input", inputPath, "--metadata", metadataPath, "--output", outputPath, "--error-output", errorPath, "--format", workbook.format], { cwd: process.cwd(), env: { ...process.env, PYTHONPATH: process.cwd() } });
      let timedOut = false;
      const timer = setTimeout(() => {
        timedOut = true;
        child.kill("SIGKILL");
      }, 120_000);
      child.once("error", () => reject(new WorkbookEngineError("engine_process_failed")));
      child.once("close", code => {
        clearTimeout(timer);
        if (code === 0) resolve();
        else if (timedOut) reject(new WorkbookEngineError("engine_timeout"));
        else void readSafeEngineFailureCode(errorPath).then(failureCode => reject(new WorkbookEngineError(failureCode)));
      });
    });
    try {
      const diagnosis = JSON.parse(await readFile(outputPath, "utf8")) as unknown;
      if (!diagnosis || typeof diagnosis !== "object" || Array.isArray(diagnosis)) {
        throw new Error("Diagnóstico inválido.");
      }
      return diagnosis as Record<string, unknown>;
    } catch {
      throw new WorkbookEngineError("engine_output_invalid");
    }
  } finally {
    await rm(workDir, { recursive: true, force: true });
  }
}

export function buildWorkbookMetadata(input: {
  analysisId: string; projectId: string; ownerNumericId: number; projectName: string; objective: string; fileId: string; workbook: ValidatedWorkbook;
}) {
  const timestamp = new Date().toISOString();
  return {
    analysis_id: input.analysisId,
    project_id: input.projectId,
    owner_user_id: contractUuid(`owner:${input.ownerNumericId}`),
    project_name: sanitizeSensitiveText(input.projectName),
    objective: sanitizeSensitiveText(input.objective),
    file_id: input.fileId,
    original_name: input.workbook.originalName,
    file_size_bytes: input.workbook.buffer.length,
    file_sha256: input.workbook.sha256,
    file_mime_type: input.workbook.mimeType,
    workbook_readable: true,
    consented_at: timestamp,
    created_at: timestamp,
    uploaded_at: timestamp,
    retention_delete_at: timestamp,
    retention_status: "reference_removed",
    correlation_id: randomUUID(),
    terms_version: "1.0",
    domain: "generic",
    business_questions: [],
    analysis_version: 1,
    supersedes_analysis_id: null,
  };
}
