import { createHash, randomUUID } from "node:crypto";
import { spawn } from "node:child_process";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

const MAX_BYTES = 25 * 1024 * 1024;
const XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";

export class UploadValidationError extends Error {}

export type ValidatedWorkbook = { buffer: Buffer; originalName: string; mimeType: string; sha256: string };
export type WorkbookInspection = { sheetCount: number };

function contractUuid(seed: string): string {
  const hex = createHash("sha256").update(seed).digest("hex");
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-4${hex.slice(13, 16)}-8${hex.slice(17, 20)}-${hex.slice(20, 32)}`;
}

export function validateWorkbookUpload(input: { fileName: string; mimeType: string; dataBase64: string }): ValidatedWorkbook {
  const originalName = input.fileName.trim().replace(/[\\/\0]/g, "_").slice(0, 255);
  if (!originalName.toLowerCase().endsWith(".xlsx")) throw new UploadValidationError("Envie somente arquivos .xlsx.");
  if (input.mimeType && input.mimeType !== XLSX_MIME && input.mimeType !== "application/octet-stream") {
    throw new UploadValidationError("O tipo informado não corresponde a uma planilha XLSX.");
  }
  if (!/^[A-Za-z0-9+/]+={0,2}$/.test(input.dataBase64) || input.dataBase64.length % 4 !== 0) {
    throw new UploadValidationError("O conteúdo do upload não está codificado em base64 válido.");
  }
  const buffer = Buffer.from(input.dataBase64, "base64");
  if (!buffer.length || buffer.length > MAX_BYTES) throw new UploadValidationError("O arquivo deve ter entre 1 byte e 25 MB.");
  const isZip = buffer.length >= 4 && buffer[0] === 0x50 && buffer[1] === 0x4b && [0x03, 0x05, 0x07].includes(buffer[2]) && [0x04, 0x06, 0x08].includes(buffer[3]);
  if (!isZip) throw new UploadValidationError("O conteúdo não possui a assinatura ZIP esperada para XLSX.");
  return { buffer, originalName, mimeType: XLSX_MIME, sha256: createHash("sha256").update(buffer).digest("hex") };
}

export function validateWorkbookInspection(input: { sheet_count: unknown }): WorkbookInspection {
  if (!Number.isInteger(input.sheet_count) || (input.sheet_count as number) < 1 || (input.sheet_count as number) > 10) {
    throw new UploadValidationError("O workbook deve ter entre 1 e 10 abas antes de ser armazenado.");
  }
  return { sheetCount: input.sheet_count as number };
}

export async function inspectWorkbookBeforePersistence(workbook: ValidatedWorkbook): Promise<WorkbookInspection> {
  const workDir = await mkdtemp(join(tmpdir(), "analytical-workbook-inspection-"));
  const inputPath = join(workDir, "input.xlsx");
  try {
    await writeFile(inputPath, workbook.buffer);
    const stdout = await new Promise<string>((resolve, reject) => {
      const child = spawn("python3", ["-m", "engine.workbook_validator", "--input", inputPath], {
        cwd: process.cwd(),
        env: { ...process.env, PYTHONPATH: process.cwd() },
      });
      let output = "";
      let stderr = "";
      const timer = setTimeout(() => child.kill("SIGKILL"), 30_000);
      child.stdout.on("data", chunk => { output += chunk.toString(); });
      child.stderr.on("data", chunk => { stderr += chunk.toString(); });
      child.once("error", reject);
      child.once("close", code => {
        clearTimeout(timer);
        if (code === 0) resolve(output);
        else reject(new UploadValidationError(`Não foi possível validar as abas do workbook: ${stderr.slice(0, 300) || `código ${code}`}`));
      });
    });
    return validateWorkbookInspection(JSON.parse(stdout) as { sheet_count: unknown });
  } finally {
    await rm(workDir, { recursive: true, force: true });
  }
}

export async function executeWorkbookEngine(workbook: ValidatedWorkbook, metadata: Record<string, unknown>) {
  const workDir = await mkdtemp(join(tmpdir(), "analytical-workbook-"));
  const inputPath = join(workDir, "input.xlsx");
  const metadataPath = join(workDir, "metadata.json");
  const outputPath = join(workDir, "diagnosis.json");
  try {
    await Promise.all([writeFile(inputPath, workbook.buffer), writeFile(metadataPath, JSON.stringify(metadata))]);
    await new Promise<void>((resolve, reject) => {
      const child = spawn("python3", ["-m", "engine.workbook_runner", "--input", inputPath, "--metadata", metadataPath, "--output", outputPath], { cwd: process.cwd(), env: { ...process.env, PYTHONPATH: process.cwd() } });
      let stderr = "";
      const timer = setTimeout(() => child.kill("SIGKILL"), 120_000);
      child.stderr.on("data", chunk => { stderr += chunk.toString(); });
      child.once("error", reject);
      child.once("close", code => {
        clearTimeout(timer);
        if (code === 0) resolve();
        else reject(new Error(`O motor de análise não concluiu o workbook: ${stderr.slice(0, 500) || `código ${code}`}`));
      });
    });
    return JSON.parse(await readFile(outputPath, "utf8")) as Record<string, unknown>;
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
    project_name: input.projectName,
    objective: input.objective,
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
