export type ExportableDiagnostic = {
  id: string;
  projectId: string;
  version: number;
  contractVersion: string;
  payload: unknown;
};

export function buildDiagnosticJsonExport(diagnostic: ExportableDiagnostic) {
  const safeId = diagnostic.id.replace(/[^a-zA-Z0-9-]/g, "").slice(0, 64) || "diagnostico";
  const fileName = `diagnostico-v${diagnostic.version}-${safeId}.json`;
  const content = JSON.stringify({
    export_format: "assistente-arquitetura-analitica/json",
    contract_version: diagnostic.contractVersion,
    diagnostic_id: diagnostic.id,
    project_id: diagnostic.projectId,
    version: diagnostic.version,
    payload: diagnostic.payload,
  }, null, 2);
  return { fileName, content };
}

export function downloadDiagnosticJson(diagnostic: ExportableDiagnostic, documentRef: Document = document, urlRef: typeof URL = URL) {
  const { fileName, content } = buildDiagnosticJsonExport(diagnostic);
  const blob = new Blob([content], { type: "application/json;charset=utf-8" });
  const href = urlRef.createObjectURL(blob);
  const anchor = documentRef.createElement("a");
  anchor.href = href;
  anchor.download = fileName;
  anchor.style.display = "none";
  documentRef.body.appendChild(anchor);
  anchor.click();
  documentRef.body.removeChild(anchor);
  urlRef.revokeObjectURL(href);
  return { fileName, content };
}
