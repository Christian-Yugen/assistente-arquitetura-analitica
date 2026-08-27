import { Button } from "@/components/ui/button";
import { CheckCircle2, CircleAlert, ClipboardCheck, RefreshCw } from "lucide-react";
import React from "react";

type Question = Record<string, unknown>;

export type ActionAnswer = { questionId: string; decision: string };

const decisions = [
  { value: "confirmed", label: "Confirmar" },
  { value: "needs_data_correction", label: "Corrigir arquivo" },
  { value: "needs_business_review", label: "Revisar negócio" },
  { value: "not_applicable", label: "Não se aplica" },
] as const;

const decisionLabels: Record<string, string> = {
  confirmed: "Confirmada",
  needs_data_correction: "Correção do arquivo necessária",
  needs_business_review: "Revisão de negócio necessária",
  not_applicable: "Marcada como não aplicável",
};

export function DiagnosticActionPlan({
  findingCount,
  questions,
  answers,
  onAnswer,
  isSubmitting,
}: {
  findingCount: number;
  questions: Question[];
  answers: ActionAnswer[];
  onAnswer: (questionId: string, decision: (typeof decisions)[number]["value"]) => void;
  isSubmitting: boolean;
}) {
  const answersByQuestion = new Map(answers.map(answer => [answer.questionId, answer.decision]));
  const answeredCount = questions.filter(question => typeof question.question_id === "string" && answersByQuestion.has(question.question_id)).length;

  return <section aria-labelledby="action-plan-heading" className="rounded-xl border border-[#b8d7a7]/30 bg-[#b8d7a7]/10 p-4">
    <div className="flex gap-3"><ClipboardCheck className="mt-0.5 h-5 w-5 shrink-0 text-[#d0efc1]" /><div className="min-w-0"><h3 id="action-plan-heading" className="text-sm font-semibold text-[#eff9e9]">Como preparar este arquivo</h3><p className="mt-1 text-xs leading-5 text-[#d5e7d5]">Use este plano no perfil draft. Ele organiza correções e decisões humanas, mas não altera automaticamente o arquivo nem promove o modelo.</p></div></div>
    <ol className="mt-4 space-y-3 text-xs leading-5 text-[#dcebdc]">
      <li className="flex gap-3"><CircleAlert className="mt-0.5 h-4 w-4 shrink-0 text-[#f4d39d]" /><span><strong>{findingCount} achado{findingCount === 1 ? "" : "s"} de qualidade:</strong> corrija primeiro ausências, inconsistências ou estrutura incompleta que possam afetar a modelagem.</span></li>
      <li className="flex gap-3"><CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-[#cde9bb]" /><span><strong>{answeredCount} de {questions.length} perguntas respondidas:</strong> registre a decisão de negócio ou a necessidade de correção para cada pergunta abaixo.</span></li>
      <li className="flex gap-3"><RefreshCw className="mt-0.5 h-4 w-4 shrink-0 text-[#b9d8cf]" /><span><strong>Depois de corrigir o arquivo:</strong> envie uma nova versão para obter um diagnóstico atualizado. As respostas não modificam o XLSX ou CSV.</span></li>
    </ol>
    {questions.length ? <div className="mt-4 grid gap-3 sm:grid-cols-2">{questions.map((question, index) => {
      const questionId = typeof question.question_id === "string" ? question.question_id : "";
      const decision = questionId ? answersByQuestion.get(questionId) : undefined;
      return <article key={questionId || index} className="rounded-lg border border-white/10 bg-[#14382f]/45 p-3"><p className="text-xs font-semibold text-[#e9f6e7]">DECISÃO HUMANA</p><p className="mt-1 text-sm font-medium text-white">{String(question.text ?? "Pergunta de validação")}</p><p className="mt-1 text-xs leading-5 text-[#d5e7d5]">{String(question.reason ?? "A resposta influencia a próxima revisão do arquivo.")}</p>{decision ? <p className="mt-3 text-xs font-semibold text-[#d2edc5]">Estado: {decisionLabels[decision] ?? "Registrada"}</p> : null}<div className="mt-3 flex flex-wrap gap-2">{decisions.map(option => <Button key={option.value} type="button" size="sm" variant={decision === option.value ? "default" : "outline"} disabled={!questionId || isSubmitting} aria-pressed={decision === option.value} onClick={() => questionId && onAnswer(questionId, option.value)} className="h-8 border-white/20 bg-white/6 px-2 text-xs text-white hover:bg-white/15 hover:text-white disabled:opacity-60">{option.label}</Button>)}</div></article>;
    })}</div> : <p className="mt-4 rounded-lg border border-dashed border-white/20 p-3 text-xs leading-5 text-[#d5e7d5]">Não há perguntas pendentes nesta versão. Revise os achados e envie uma nova versão apenas se corrigir o arquivo.</p>}
  </section>;
}
