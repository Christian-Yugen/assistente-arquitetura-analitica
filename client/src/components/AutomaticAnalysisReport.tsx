import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import type { ModelingGuidance } from "@/lib/modelingGuidance";
import { Download } from "lucide-react";
import React from "react";

type UnknownRecord = Record<string, unknown>;

type ReportCount = {
  label: string;
  value: number;
};

type ReportStep = {
  code: string;
  priority: "high" | "medium";
  title: string;
  action: string;
};

const STEP_CATALOG: Record<string, ReportStep> = {
  isolate_sensitive_fields: { code: "isolate_sensitive_fields", priority: "high", title: "Isolar campos pessoais da modelagem", action: "Mantenha campos pessoais fora de chaves, relações, medidas e DAX até haver política de uso aprovada." },
  review_duplicate_rows: { code: "review_duplicate_rows", priority: "high", title: "Revisar duplicidades", action: "Valide a chave de negócio antes de remover grupos repetidos no Power Query." },
  standardize_data_types: { code: "standardize_data_types", priority: "high", title: "Padronizar tipos de dados", action: "Separe ou converta tipos incompatíveis somente após confirmar a semântica de cada grupo." },
  resolve_missing_data: { code: "resolve_missing_data", priority: "high", title: "Tratar ausências antes do modelo", action: "Defina se cada ausência deve ser corrigida na origem, mantida como desconhecida ou excluída da análise." },
  confirm_table_purpose: { code: "confirm_table_purpose", priority: "medium", title: "Confirmar a finalidade da estrutura", action: "Defina o que cada linha representa antes de chamar a estrutura de fato ou dimensão." },
  confirm_relationship_keys: { code: "confirm_relationship_keys", priority: "medium", title: "Confirmar chaves de relacionamento", action: "Valide chaves únicas e referências antes de conectar tabelas no modelo." },
  implement_confirmed_hypotheses: { code: "implement_confirmed_hypotheses", priority: "medium", title: "Aplicar as hipóteses confirmadas", action: "Crie dimensões, fatos, relações e medidas somente após confirmar o grão e as regras de negócio." },
};

function asRecord(value: unknown): UnknownRecord {
  return value && typeof value === "object" && !Array.isArray(value) ? value as UnknownRecord : {};
}

function asCount(value: unknown): number {
  return typeof value === "number" && value >= 0 ? value : 0;
}

function getSteps(payload: UnknownRecord): ReportStep[] {
  const model = asRecord(payload.proposed_model);
  const rawSteps = Array.isArray(model.implementation_steps) ? model.implementation_steps : [];
  const unique = new Set<string>();
  return rawSteps.flatMap(rawStep => {
    const code = asRecord(rawStep).code;
    if (typeof code !== "string" || unique.has(code) || !STEP_CATALOG[code]) return [];
    unique.add(code);
    return [STEP_CATALOG[code]];
  });
}

function reportCards(guidance: ModelingGuidance) {
  return [guidance.dimensions, guidance.facts, guidance.grains, guidance.relationships, guidance.metrics]
    .flat()
    .map(card => `${card.label}: ${card.count}${card.formula ? ` — fórmula conceitual: ${card.formula}` : ""}`);
}

function downloadReport(counts: ReportCount[], steps: ReportStep[], guidance: ModelingGuidance) {
  const resultLines = counts.map(count => `- ${count.label}: ${count.value}`);
  const preparationLines = steps.length
    ? steps.map((step, index) => `${index + 1}. **${step.title}** (${step.priority === "high" ? "prioridade alta" : "prioridade média"}): ${step.action}`)
    : ["Nenhuma preparação adicional foi emitida para esta versão."];
  const modelingLines = reportCards(guidance);
  const content = [
    "# Relatório automático de arquitetura analítica",
    "",
    "> Perfil draft. Este relatório contém somente contagens e descrições sanitizadas; não inclui valores, cabeçalhos, identificadores ou dados pessoais do arquivo.",
    "",
    "## Resultados da leitura",
    ...resultLines,
    "",
    "## Hipóteses de modelagem e métricas conceituais",
    ...(modelingLines.length ? modelingLines.map(line => `- ${line}`) : ["- Nenhuma hipótese adicional foi emitida com evidência suficiente."]),
    "",
    "## Roteiro para Power Query",
    ...preparationLines,
    "",
    "## Limite de uso",
    "As hipóteses não criam consultas, relações ou DAX final automaticamente. Confirme o grão e as regras de negócio antes da implementação no Power BI.",
  ].join("\n");
  const url = URL.createObjectURL(new Blob([content], { type: "text/markdown;charset=utf-8" }));
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "relatorio-analise-draft.md";
  anchor.click();
  URL.revokeObjectURL(url);
}

export function AutomaticAnalysisReport({ payload, counts, guidance }: { payload: UnknownRecord; counts: ReportCount[]; guidance: ModelingGuidance }) {
  const steps = getSteps(payload);
  const model = asRecord(payload.proposed_model);
  const hasHypotheses = model.status === "hypothesis";

  return <section aria-labelledby="analysis-report-heading" className="rounded-2xl border border-[#b8d7a7]/35 bg-[#113329]/55 p-5">
    <div className="flex flex-wrap items-start justify-between gap-3">
      <div><p className="text-xs font-semibold tracking-[0.12em] text-[#c6e4bd] uppercase">Relatório automático</p><h3 id="analysis-report-heading" className="mt-1 font-serif text-xl text-white">Resultado da leitura e preparação</h3></div>
      <div className="flex items-center gap-2"><Badge className="border-[#b8d7a7]/30 bg-[#b8d7a7]/12 text-[#e5f4df]">Perfil draft</Badge><Button type="button" size="sm" variant="outline" onClick={() => downloadReport(counts, steps, guidance)} className="border-white/20 bg-white/8 text-white hover:bg-white/15 hover:text-white"><Download className="h-3.5 w-3.5" />Exportar relatório</Button></div>
    </div>
    <div className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-3">{counts.map(count => <div key={count.label} className="rounded-xl border border-white/10 bg-white/6 p-3"><p className="text-xs text-[#c0d8c3]">{count.label}</p><p className="mt-1 font-serif text-2xl text-white">{count.value}</p></div>)}</div>
    <p className="mt-4 text-sm leading-6 text-[#deedda]">{hasHypotheses ? "Há hipóteses automáticas para orientar o modelo. Elas não criam relações, DAX ou consultas no seu Power BI sem confirmação." : "Ainda não há hipótese suficiente de fato ou dimensão. O roteiro abaixo mostra o que preparar antes de uma nova leitura."}</p>
    <div className="mt-5"><h4 className="text-xs font-semibold tracking-[0.12em] text-[#c6e4bd] uppercase">Roteiro para Power Query</h4>{steps.length ? <ol className="mt-3 space-y-3">{steps.map((step, index) => <li key={step.code} className="rounded-xl border border-white/10 bg-white/6 p-4"><div className="flex items-center justify-between gap-3"><p className="text-sm font-semibold text-white">{index + 1}. {step.title}</p><Badge className={step.priority === "high" ? "border-[#f4d39d]/35 bg-[#f4d39d]/12 text-[#ffe8b7]" : "border-[#c4d8f7]/30 bg-[#c4d8f7]/10 text-[#dae9ff]"}>{step.priority === "high" ? "Prioridade alta" : "Prioridade média"}</Badge></div><p className="mt-2 text-xs leading-5 text-[#d4e4d5]">{step.action}</p></li>)}</ol> : <p className="mt-3 rounded-xl border border-dashed border-white/20 p-4 text-xs leading-5 text-[#d4e4d5]">Nenhuma preparação adicional foi emitida para esta versão.</p>}</div>
  </section>;
}
