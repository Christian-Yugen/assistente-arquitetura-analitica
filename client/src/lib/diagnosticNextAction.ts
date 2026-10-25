export type RecordedDecision = "confirmed" | "needs_data_correction" | "needs_business_review" | "not_applicable";

export type DiagnosticNextAction = {
  kind: "correct_file" | "answer_questions" | "business_review" | "keep_current_version" | "no_action";
  title: string;
  description: string;
};

export function getDiagnosticNextAction(input: {
  findingCount: number;
  questionCount: number;
  answers: Array<{ decision: string }>;
}): DiagnosticNextAction {
  const corrections = input.answers.filter(answer => answer.decision === "needs_data_correction").length;
  const businessReviews = input.answers.filter(answer => answer.decision === "needs_business_review").length;
  const unanswered = Math.max(0, input.questionCount - input.answers.length);

  if (corrections > 0) {
    return {
      kind: "correct_file",
      title: "Próxima ação: corrigir o arquivo e enviar uma nova versão",
      description: `${corrections} escolha${corrections === 1 ? " indica" : "s indicam"} que alguma informação deveria existir. Corrija somente o que for necessário na fonte e faça uma nova análise.`,
    };
  }

  if (unanswered > 0) {
    return {
      kind: "answer_questions",
      title: "Próxima ação: concluir as escolhas pendentes",
      description: `Ainda há ${unanswered} pergunta${unanswered === 1 ? " para responder" : "s para responder"}. Escolha a opção que melhor descreve cada situação antes de decidir se o arquivo deve mudar.`,
    };
  }

  if (businessReviews > 0) {
    return {
      kind: "business_review",
      title: "Próxima ação: alinhar a decisão com o negócio",
      description: `${businessReviews} escolha${businessReviews === 1 ? " depende" : "s dependem"} do contexto do negócio. O arquivo não precisa ser reenviado enquanto ele não mudar; registre a decisão com a pessoa responsável antes de modelar.`,
    };
  }

  if (input.findingCount > 0) {
    return {
      kind: "keep_current_version",
      title: "Próxima ação: manter esta versão como referência",
      description: "As escolhas indicam que o arquivo representa a situação atual. Não há reenvio obrigatório; use os achados como apoio para a revisão draft e envie uma nova versão somente se a fonte mudar.",
    };
  }

  return {
    kind: "no_action",
    title: "Próxima ação: nenhuma mudança necessária agora",
    description: "Não há achados ou decisões pendentes nesta versão. Continue a revisão draft antes de usar qualquer hipótese de modelagem.",
  };
}
