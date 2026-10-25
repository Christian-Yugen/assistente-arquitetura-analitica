import { renderToStaticMarkup } from "react-dom/server";
import React from "react";
import { describe, expect, it } from "vitest";
import { AutomaticAnalysisReport } from "./AutomaticAnalysisReport";

describe("AutomaticAnalysisReport", () => {
  it("renders only allowlisted Power Query actions and does not render raw payload text", () => {
    const markup = renderToStaticMarkup(<AutomaticAnalysisReport
      payload={{ proposed_model: { status: "hypothesis", implementation_steps: [{ code: "review_duplicate_rows", title: "Cabeçalho privado", action: "Valor privado" }, { code: "unapproved_step", title: "Não renderizar" }] } }}
      counts={[{ label: "Dimensões", value: 1 }, { label: "Fatos", value: 0 }]}
      guidance={{ dimensions: [], facts: [], structuralReviews: [], grains: [], relationships: [], metrics: [], semanticSignals: [] }}
    />);

    expect(markup).toContain("Relatório automático");
    expect(markup).toContain("Exportar relatório");
    expect(markup).toContain("Revisar duplicidades");
    expect(markup).toContain("Valide a chave de negócio");
    expect(markup).toContain("Dimensões");
    expect(markup).not.toContain("Cabeçalho privado");
    expect(markup).not.toContain("Valor privado");
    expect(markup).not.toContain("Não renderizar");
  });
});
