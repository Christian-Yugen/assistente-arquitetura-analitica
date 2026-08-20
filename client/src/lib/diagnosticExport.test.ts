import { describe, expect, it, vi } from "vitest";
import { buildDiagnosticJsonExport, downloadDiagnosticJson } from "./diagnosticExport";

const diagnostic = {
  id: "test-diagnostic-id",
  projectId: "test-project-id",
  version: 3,
  contractVersion: "1.0.0-reconstructed.1",
  payload: { sheets: [{ name: "Aba 1" }], findings: [] },
};

describe("diagnostic JSON export", () => {
  it("builds a structured file containing only the selected diagnostic contract", () => {
    const result = buildDiagnosticJsonExport(diagnostic);
    const parsed = JSON.parse(result.content);

    expect(result.fileName).toBe("diagnostico-v3-test-diagnostic-id.json");
    expect(parsed).toMatchObject({
      export_format: "assistente-arquitetura-analitica/json",
      contract_version: "1.0.0-reconstructed.1",
      diagnostic_id: "test-diagnostic-id",
      project_id: "test-project-id",
      version: 3,
      payload: diagnostic.payload,
    });
  });

  it("uses a temporary object URL and revokes it after the download action", () => {
    const click = vi.fn();
    const appendChild = vi.fn();
    const removeChild = vi.fn();
    const anchor = { href: "", download: "", style: { display: "" }, click } as unknown as HTMLAnchorElement;
    const documentRef = { createElement: vi.fn().mockReturnValue(anchor), body: { appendChild, removeChild } } as unknown as Document;
    const urlRef = { createObjectURL: vi.fn().mockReturnValue("blob:diagnostic"), revokeObjectURL: vi.fn() } as unknown as typeof URL;

    const result = downloadDiagnosticJson(diagnostic, documentRef, urlRef);

    expect(documentRef.createElement).toHaveBeenCalledWith("a");
    expect(anchor.download).toBe(result.fileName);
    expect(anchor.href).toBe("blob:diagnostic");
    expect(appendChild).toHaveBeenCalledWith(anchor);
    expect(click).toHaveBeenCalledOnce();
    expect(removeChild).toHaveBeenCalledWith(anchor);
    expect(urlRef.revokeObjectURL).toHaveBeenCalledWith("blob:diagnostic");
  });
});
