const EMAIL_PATTERN = /[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/gi;
const CPF_PATTERN = /\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b/g;
const EXPLICIT_NAME_PATTERN = /\b(nome|name)\s*[:=-]\s*[^,;\n]+/gi;

export function sanitizeSensitiveText(value: string): string {
  return value
    .replace(EMAIL_PATTERN, "[e-mail mascarado]")
    .replace(CPF_PATTERN, "[CPF mascarado]")
    .replace(EXPLICIT_NAME_PATTERN, (_match, label: string) => `${label}: [nome mascarado]`)
    .trim();
}

export function sanitizeWorkbookFileName(value: string): string {
  const extension = value.toLowerCase().endsWith(".xlsx") ? ".xlsx" : "";
  const baseName = extension ? value.slice(0, -extension.length) : value;
  const sanitized = sanitizeSensitiveText(baseName).replace(/[\[\]]/g, "").trim() || "workbook";
  return `${sanitized.slice(0, Math.max(1, 255 - extension.length))}${extension}`;
}

function hasSensitiveText(value: string): boolean {
  EMAIL_PATTERN.lastIndex = 0;
  CPF_PATTERN.lastIndex = 0;
  EXPLICIT_NAME_PATTERN.lastIndex = 0;
  return EMAIL_PATTERN.test(value) || CPF_PATTERN.test(value) || EXPLICIT_NAME_PATTERN.test(value);
}

export function containsDetectedSensitiveData(value: unknown): boolean {
  if (typeof value === "string") return hasSensitiveText(value);
  if (Array.isArray(value)) return value.some(item => containsDetectedSensitiveData(item));
  if (value && typeof value === "object") return Object.values(value).some(item => containsDetectedSensitiveData(item));
  return false;
}

export function containsUnsafeDiagnosticContent(value: unknown): boolean {
  if (containsDetectedSensitiveData(value)) return true;
  if (!value || typeof value !== "object" || Array.isArray(value)) return false;
  const sheets = (value as { sheets?: unknown }).sheets;
  return Array.isArray(sheets) && sheets.some(sheet => {
    const name = sheet && typeof sheet === "object" ? (sheet as { name?: unknown }).name : undefined;
    return typeof name === "string" && !/^Aba [1-9]\d*$/.test(name);
  });
}
