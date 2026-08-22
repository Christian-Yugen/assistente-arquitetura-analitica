import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { beforeEach, describe, expect, it, vi } from "vitest";

type DiagnosticMock = {
  id: string;
  projectId: string;
  version: number;
  contractVersion: string;
  payload: Record<string, unknown>;
};

const state = vi.hoisted(() => ({
  auth: { loading: false, isAuthenticated: true, error: null as Error | null },
  mutation: { isPending: false, isSuccess: false, data: undefined as { diagnosticId: string; version: number } | undefined },
  projects: { data: [], isLoading: false, isError: false },
  diagnostic: { data: undefined as DiagnosticMock | undefined, isFetching: false, isError: false },
}));

vi.mock("@/_core/hooks/useAuth", () => ({ useAuth: () => state.auth }));
vi.mock("@/const", () => ({ startLogin: vi.fn() }));
vi.mock("@/components/DashboardLayout", async () => {
  const ReactModule = await import("react");
  return { default: ({ children }: { children: React.ReactNode }) => ReactModule.createElement("div", { "data-layout": "workspace" }, children) };
});
vi.mock("@/lib/trpc", () => ({
  trpc: {
    useUtils: () => ({ analysis: { listProjects: { invalidate: vi.fn() } } }),
    analysis: {
      listProjects: { useQuery: () => state.projects },
      getDiagnostic: { useQuery: () => state.diagnostic },
      analyzeWorkbook: { useMutation: () => ({ ...state.mutation, mutate: vi.fn() }) },
    },
  },
}));

import Home from "./Home";

function renderHome() {
  return renderToStaticMarkup(<Home />);
}

function tagWith(markup: string, marker: string) {
  const markerIndex = markup.indexOf(marker);
  return markup.slice(markup.lastIndexOf("<", markerIndex), markup.indexOf(">", markerIndex) + 1);
}

describe("Home workspace flow", () => {
  beforeEach(() => {
    state.auth = { loading: false, isAuthenticated: true, error: null };
    state.mutation = { isPending: false, isSuccess: false, data: undefined };
    state.projects = { data: [], isLoading: false, isError: false };
    state.diagnostic = { data: undefined, isFetching: false, isError: false };
  });

  it("renders loading, sign-in and session-error workspace states", () => {
    state.auth = { loading: true, isAuthenticated: false, error: null };
    expect(renderHome()).toContain("Verificando sua sessão segura");

    state.auth = { loading: false, isAuthenticated: false, error: null };
    const signIn = renderHome();
    expect(signIn).toContain("Entrar no workspace");
    expect(signIn).not.toContain("Nome do projeto");

    state.auth = { loading: false, isAuthenticated: true, error: new Error("session") };
    expect(renderHome()).toContain("Tentar login novamente");
  });

  it("shows the forty rules authorized for the current draft profile", () => {
    const workspace = renderHome();
    expect(workspace).toContain("Regras executáveis");
    expect(workspace).toContain(">40<");
    expect(workspace).toContain("QLT-001 a QLT-015 + SEM-DATE-001 + SEM-COMP-002 + SEM-DESC-004 + SEM-DUR-008 + SEM-STATUS-009 + SEM-CAT-010 + SEM-LOC-011 + SEM-RESP-012 + SEM-ID-003 + SEM-QTY-005 + SEM-CURR-006 + SEM-PCT-007 + SEM-TARGET-013 + SEM-ACTUAL-014 + SEM-SENS-015 + GRN-COMP-001 + GRN-EXPL-002 + GRN-EVENT-004 + GRN-ENTITY-003 + MDL-FACTPER-001 + MDL-FACTTXN-002 + MDL-FACTNOGRAIN-019 + MDL-UNDEFINED-020 + MDL-DIMSTD-004 + MDL-DIMCAL-006");
  });

  it("renders the pending processing panel and blocks all workbook edits during the real mutation state", () => {
    expect(renderHome()).toContain("Nome do projeto");
    state.mutation = { isPending: true, isSuccess: false, data: undefined };
    const pending = renderHome();
    expect(pending).toContain("Analisando estrutura");
    expect(pending).toContain("Análise em andamento no servidor");
    expect(pending).toContain("Nenhum percentual é estimado");
    expect(tagWith(pending, 'id="projectName"')).toContain('disabled=""');
    expect(tagWith(pending, 'id="objective"')).toContain('disabled=""');
    expect(tagWith(pending, 'accept=".xlsx,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"')).toContain('disabled=""');
  });

  it("renders the created version confirmation when the mutation succeeds", () => {
    state.mutation = { isPending: false, isSuccess: true, data: { diagnosticId: "diag-5", version: 5 } };
    const success = renderHome();
    expect(success).toContain("Versão 5 criada com sucesso");
    expect(success).toContain("Ver diagnóstico");
  });

  it("shows the JSON export action only for a loaded diagnostic version", () => {
    expect(renderHome()).not.toContain("Exportar JSON");
    expect(renderHome()).not.toContain("Exportar PDF");
    state.diagnostic = {
      data: {
        id: "11111111-1111-4111-8111-111111111111",
        projectId: "22222222-2222-4222-8222-222222222222",
        version: 2,
        contractVersion: "1.0.0-reconstructed.1",
        payload: { summary: { counts: { sheets: 1, risks: 0 } }, findings: [], questions: [], file: { retention: { status: "reference_removed" } } },
      },
      isFetching: false,
      isError: false,
    };

    const loadedDiagnostic = renderHome();
    expect(loadedDiagnostic).toContain("Exportar JSON");
    expect(loadedDiagnostic).not.toContain("Exportar PDF");
  });

  it("renders every finding and validation question from the selected diagnostic", () => {
    state.diagnostic = {
      data: {
        id: "11111111-1111-4111-8111-111111111111",
        projectId: "22222222-2222-4222-8222-222222222222",
        version: 3,
        contractVersion: "1.0.0-reconstructed.1",
        payload: {
          summary: { counts: { sheets: 1, risks: 3 } },
          findings: [
            { finding_id: "f-1", title: "Achado um", description: "Evidência um" },
            { finding_id: "f-2", title: "Achado dois", description: "Evidência dois" },
            { finding_id: "f-3", title: "Achado três", description: "Evidência três", recommendation: "Recomendação três" },
          ],
          questions: [
            { question_id: "q-1", text: "Pergunta um", reason: "Motivo um" },
            { question_id: "q-2", text: "Pergunta dois", reason: "Motivo dois" },
            { question_id: "q-3", text: "Pergunta três", reason: "Motivo três" },
          ],
          file: { retention: { status: "reference_removed" } },
        },
      },
      isFetching: false,
      isError: false,
    };

    const diagnostic = renderHome();
    expect(diagnostic).toContain("Achado três");
    expect(diagnostic).toContain("Recomendação três");
    expect(diagnostic).toContain("Pergunta três");
  });
});
