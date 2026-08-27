/* @vitest-environment jsdom */
import React from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { DiagnosticActionPlan } from "./DiagnosticActionPlan";

describe("DiagnosticActionPlan", () => {
  it("guides the correction flow and records only an enumerated decision through the callback", () => {
    const onAnswer = vi.fn();
    render(<DiagnosticActionPlan
      findingCount={7}
      questions={[{ question_id: "opaque-q-1", text: "Pergunta segura", reason: "Motivo seguro" }]}
      answers={[]}
      onAnswer={onAnswer}
      isSubmitting={false}
    />);

    expect(screen.getByText("Como preparar este arquivo")).toBeTruthy();
    expect(screen.getByText(/7 achados de qualidade/)).toBeTruthy();
    expect(screen.getByText(/0 de 1 perguntas respondidas/)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Corrigir arquivo" }));
    expect(onAnswer).toHaveBeenCalledWith("opaque-q-1", "needs_data_correction");
  });

  it("shows the registered decision rather than storing or requesting free text", () => {
    render(<DiagnosticActionPlan
      findingCount={0}
      questions={[{ question_id: "opaque-q-2", text: "Pergunta segura" }]}
      answers={[{ questionId: "opaque-q-2", decision: "confirmed" }]}
      onAnswer={vi.fn()}
      isSubmitting={false}
    />);

    expect(screen.getByText("Estado: Confirmada")).toBeTruthy();
    expect(screen.queryByRole("textbox")).toBeNull();
  });
});
