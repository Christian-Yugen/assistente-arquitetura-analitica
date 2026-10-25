import { type ModelingGuidance } from "@/lib/modelingGuidance";
import { Database, Link2, Sigma, Table2 } from "lucide-react";
import React from "react";

function hypothesisCount(cards: { count: number }[]) {
  return cards.reduce((total, card) => total + card.count, 0);
}

export function ModelingResultSummary({ guidance }: { guidance: ModelingGuidance }) {
  const dimensions = hypothesisCount(guidance.dimensions);
  const facts = hypothesisCount(guidance.facts);
  const grains = hypothesisCount(guidance.grains);
  const relationships = hypothesisCount(guidance.relationships);
  const metrics = hypothesisCount(guidance.metrics);
  const resultCount = dimensions + facts + grains + relationships + metrics;
  const results = [
    { label: "Dimensões", value: dimensions, icon: Table2 },
    { label: "Fatos", value: facts, icon: Database },
    { label: "Grãos", value: grains, icon: Table2 },
    { label: "Relações", value: relationships, icon: Link2 },
    { label: "Medidas/DAX", value: metrics, icon: Sigma },
  ];

  return <section aria-labelledby="modeling-results-heading" className="rounded-xl border border-[#b8d7a7]/30 bg-[#0d2e26]/45 p-4">
    <p className="text-xs font-semibold tracking-[0.12em] text-[#b8d7a7] uppercase">Resultado da leitura</p>
    <h3 id="modeling-results-heading" className="mt-1 text-base font-semibold text-white">Proposta de modelagem encontrada</h3>
    <div className="mt-4 grid grid-cols-2 gap-2 sm:grid-cols-5">
      {results.map(result => <div key={result.label} className="rounded-lg border border-white/10 bg-white/8 p-3"><result.icon className="h-4 w-4 text-[#b8d7a7]" /><p className="mt-2 font-serif text-2xl text-white">{result.value}</p><p className="text-[11px] text-[#c7d8c8]">{result.label}</p></div>)}
    </div>
    <p className="mt-4 text-xs leading-5 text-[#d8e9d6]">{resultCount ? `${resultCount} hipótese${resultCount === 1 ? "" : "s"} de modelagem foi${resultCount === 1 ? "" : "ram"} emitida${resultCount === 1 ? "" : "s"} pela leitura e aparece${resultCount === 1 ? "" : "m"} detalhada${resultCount === 1 ? "" : "s"} abaixo.` : "A leitura foi concluída, mas nenhuma hipótese de dimensão, fato, grão, relação ou medida atingiu os critérios das regras draft nesta versão."}</p>
  </section>;
}
