import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { AnalysisAuthNotice, AnalysisProcessingPanel, AnalysisSubmitButton, AnalysisSuccessNotice } from "./AnalysisFlowState";

describe("AnalysisFlowState", () => {
  const login = () => undefined;
  it("renders authentication loading, sign-in action and authentication error", () => {
    expect(renderToStaticMarkup(<AnalysisAuthNotice state="auth_loading" onLogin={login} />)).toContain("Verificando sua sessão segura");
    const signIn = renderToStaticMarkup(<AnalysisAuthNotice state="sign_in_required" onLogin={login} />);
    expect(signIn).toContain("Faça login para iniciar uma análise privada");
    expect(signIn).toContain("Entrar no workspace");
    expect(renderToStaticMarkup(<AnalysisAuthNotice state="auth_error" onLogin={login} />)).toContain("Tentar login novamente");
  });

  it("renders a disabled pending submit control and a successful diagnosis confirmation", () => {
    const pending = renderToStaticMarkup(<AnalysisSubmitButton isPending />);
    expect(pending).toContain("disabled");
    expect(pending).toContain("Analisando estrutura");
    expect(renderToStaticMarkup(<AnalysisSuccessNotice version={3} onView={login} />)).toContain("Versão 3 criada com sucesso");
  });

  it("renders an honest accessible processing notice without simulated percentage", () => {
    const pending = renderToStaticMarkup(<AnalysisProcessingPanel fileName="estrutura.xlsx" />);
    expect(pending).toContain('role="status"');
    expect(pending).toContain("Análise em andamento no servidor");
    expect(pending).toContain("estrutura.xlsx");
    expect(pending).toContain("Nenhum percentual é estimado");
  });
});
