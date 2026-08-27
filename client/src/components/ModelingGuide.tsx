import { type GuidanceCard, type ModelingGuidance } from "@/lib/modelingGuidance";
import { Badge } from "@/components/ui/badge";
import { ArrowRight, Database, Link2, Sigma, Table2 } from "lucide-react";
import React from "react";

type Question = Record<string, unknown>;
type ActionAnswer = { questionId: string; decision: string };
type ValidationStatus = { total: number; answered: number; needsCorrection: boolean; needsBusinessReview: boolean };

function confidenceText(value: number | null) {
  return value === null ? "Confirmação necessária" : `${Math.round(value * 100)}% de confiança draft`;
}

function validationForModule(questions: Question[], answers: ActionAnswer[], module: string): ValidationStatus {
  const answersByQuestion = new Map(answers.map(answer => [answer.questionId, answer.decision]));
  const questionIds = questions.flatMap(question => {
    const impact = question.impact && typeof question.impact === "object" ? question.impact as Record<string, unknown> : {};
    const modules = Array.isArray(impact.affected_modules) ? impact.affected_modules : [];
    return modules.includes(module) && typeof question.question_id === "string" ? [question.question_id] : [];
  });
  const decisions = questionIds.map(questionId => answersByQuestion.get(questionId)).filter((decision): decision is string => Boolean(decision));
  return { total: questionIds.length, answered: decisions.length, needsCorrection: decisions.includes("needs_data_correction"), needsBusinessReview: decisions.includes("needs_business_review") };
}

function validationText(status: ValidationStatus) {
  if (!status.total) return "Sem decisão de validação pendente nesta seção.";
  if (status.needsCorrection) return "Há uma decisão de corrigir o arquivo antes de usar esta hipótese.";
  if (status.answered < status.total) return `${status.answered} de ${status.total} decisões registradas. Conclua as opções abaixo antes de finalizar o modelo.`;
  if (status.needsBusinessReview) return "As decisões foram registradas; alinhe a regra de negócio antes de finalizar o modelo.";
  return "As decisões de validação desta seção foram registradas.";
}

function GuidanceSection({ title, description, cards, emptyText, icon: Icon, validation, showFormula = false }: { title: string; description: string; cards: GuidanceCard[]; emptyText: string; icon: typeof Database; validation: ValidationStatus; showFormula?: boolean }) {
  return <section className="rounded-xl border border-white/10 bg-white/8 p-4" aria-label={title}>
    <div className="flex gap-3"><span className="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-[#b8d7a7]/12 text-[#b8d7a7]"><Icon className="h-4 w-4" /></span><div><h3 className="text-sm font-semibold text-white">{title}</h3><p className="mt-0.5 text-xs leading-5 text-[#c7d8c8]">{description}</p></div></div>
    {cards.length ? <><div className="mt-4 grid gap-3">{cards.map(card => <article key={card.label} className="rounded-lg border border-white/10 bg-[#0d2e26]/35 p-3"><div className="flex flex-wrap items-start justify-between gap-2"><p className="text-sm font-semibold text-[#eef8ed]">{card.label}{card.count > 1 ? ` · ${card.count} hipóteses` : ""}</p><Badge className="border border-[#b8d7a7]/20 bg-[#b8d7a7]/10 text-[10px] text-[#d8edd5] hover:bg-[#b8d7a7]/10">{confidenceText(card.confidence)}</Badge></div><p className="mt-2 text-xs leading-5 text-[#c7d8c8]">{card.definition}</p>{showFormula && card.formula ? <code className="mt-3 block overflow-x-auto rounded-md border border-[#b8d7a7]/15 bg-black/15 px-2.5 py-2 text-[11px] text-[#e3f1df]">{card.formula}</code> : null}<p className="mt-3 flex gap-2 text-xs leading-5 text-[#e0efdc]"><ArrowRight className="mt-0.5 h-3.5 w-3.5 shrink-0 text-[#b8d7a7]" /><span><strong>Agora:</strong> {card.nextStep}</span></p></article>)}</div><p className="mt-3 rounded-lg border border-[#b8d7a7]/15 bg-[#b8d7a7]/8 px-3 py-2 text-[11px] leading-4 text-[#d8e9d6]"><strong>Validação desta seção:</strong> {validationText(validation)}</p></> : <p className="mt-4 rounded-lg border border-dashed border-white/20 px-3 py-3 text-xs leading-5 text-[#c7d8c8]">{emptyText}</p>}
  </section>;
}

export function ModelingGuide({ guidance, questions, answers }: { guidance: ModelingGuidance; questions: Question[]; answers: ActionAnswer[] }) {
  const hasModelingHypothesis = guidance.dimensions.length + guidance.facts.length + guidance.structuralReviews.length + guidance.grains.length + guidance.relationships.length + guidance.metrics.length + guidance.semanticSignals.length > 0;
  const factDimensionValidation = validationForModule(questions, answers, "fact_dimension");
  const grainValidation = validationForModule(questions, answers, "granularity");
  const relationshipValidation = validationForModule(questions, answers, "relationships");
  const metricValidation = validationForModule(questions, answers, "metric_suggestion");
  const semanticValidation = validationForModule(questions, answers, "semantic_typing");
  return <section aria-labelledby="modeling-guide-heading" className="space-y-4"><div className="rounded-xl border border-[#b8d7a7]/25 bg-[#b8d7a7]/10 p-4"><p className="text-xs font-semibold tracking-[0.12em] text-[#b8d7a7] uppercase">Guia de modelagem</p><h3 id="modeling-guide-heading" className="mt-1 text-base font-semibold text-white">O que você pode começar a desenhar no Power BI</h3><p className="mt-2 text-xs leading-5 text-[#d8e9d6]">{hasModelingHypothesis ? "As sugestões abaixo são hipóteses do perfil draft. Confirme-as pelas perguntas antes de criar relações ativas ou medidas finais." : "Esta versão não trouxe evidência suficiente para sugerir estruturas de modelo. Isso não é erro: inclua mais registros reais e reenvie quando houver dados adicionais."}</p></div>
    <ol aria-label="Percurso para usar o diagnóstico" className="grid gap-2 sm:grid-cols-2 xl:grid-cols-4">{[
      ["1", "Defina o grão", "Confirme o que uma linha representa."],
      ["2", "Separe fatos e dimensões", "Transforme somente hipóteses confirmadas."],
      ["3", "Valide relações", "Confira chaves, cardinalidade e direção do filtro."],
      ["4", "Finalize medidas", "Aplique o modelo DAX após confirmar campos e regras."],
    ].map(([step, title, description]) => <li key={step} className="rounded-lg border border-white/10 bg-white/6 p-3"><span className="text-[10px] font-semibold text-[#b8d7a7]">PASSO {step}</span><p className="mt-1 text-xs font-semibold text-white">{title}</p><p className="mt-1 text-[11px] leading-4 text-[#c7d8c8]">{description}</p></li>)}</ol>
    <div className="grid gap-4 xl:grid-cols-2"><GuidanceSection title="Dimensões" description="Entidades que ajudam a filtrar e explicar os fatos." cards={guidance.dimensions} emptyText="Nenhuma dimensão foi sugerida com evidência suficiente nesta versão." icon={Table2} validation={factDimensionValidation} /><GuidanceSection title="Fatos" description="Eventos, movimentos ou valores que normalmente viram medidas." cards={guidance.facts} emptyText="Nenhum fato foi sugerido com evidência suficiente nesta versão." icon={Database} validation={factDimensionValidation} /><GuidanceSection title="Grão da tabela" description="A regra que define o que representa uma linha antes de criar medidas." cards={guidance.grains} emptyText="Nenhuma hipótese de grão foi sugerida com evidência suficiente nesta versão." icon={Table2} validation={grainValidation} /><GuidanceSection title="Relações" description="Possíveis conexões a validar antes de configurar cardinalidade e filtros." cards={guidance.relationships} emptyText="Nenhuma relação foi sugerida com evidência suficiente nesta versão." icon={Link2} validation={relationshipValidation} /><GuidanceSection title="Medidas e modelos DAX" description="Fórmulas conceituais; não são DAX pronto porque campos e regras ainda precisam ser confirmados." cards={guidance.metrics} emptyText="Nenhuma medida foi sugerida com evidência suficiente nesta versão." icon={Sigma} validation={metricValidation} showFormula /></div>
    {guidance.structuralReviews.length || guidance.semanticSignals.length ? <div className="grid gap-4 xl:grid-cols-2"><GuidanceSection title="Estruturas que pedem revisão" description="Situações que podem alterar a forma correta de modelar." cards={guidance.structuralReviews} emptyText="Nenhuma revisão estrutural adicional foi sugerida." icon={Table2} validation={factDimensionValidation} /><GuidanceSection title="Sinais de campos" description="Classificações agregadas que ajudam a validar chaves, datas e medidas." cards={guidance.semanticSignals} emptyText="Nenhum sinal semântico adicional foi emitido nesta versão." icon={Database} validation={semanticValidation} /></div> : null}
    <p className="rounded-xl border border-white/10 bg-white/8 p-4 text-xs leading-5 text-[#d5e5d4]">As perguntas abaixo não editam sua planilha nem criam relações ou DAX automaticamente. Elas servem para decidir se a hipótese está correta, se o arquivo precisa ser corrigido ou se a regra depende do negócio. Para gerar uma nova análise, envie uma nova versão quando o arquivo tiver sido ajustado ou ampliado.</p>
  </section>;
}
