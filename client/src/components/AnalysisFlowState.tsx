import React from "react";
import { Button } from "@/components/ui/button";
import { CheckCircle2, FileSearch2, FileSpreadsheet, Loader2, ShieldCheck } from "lucide-react";
import type { AnalysisUiState } from "@/lib/analysisUiState";

export function AnalysisAuthNotice({ state, onLogin }: { state: AnalysisUiState; onLogin: () => void }) {
  if (state === "auth_loading") return <div className="rounded-xl bg-[#f5f9f3] p-4 text-sm text-[#557060]"><Loader2 className="mr-2 inline h-4 w-4 animate-spin" />Verificando sua sessão segura…</div>;
  if (state === "sign_in_required") return <div className="rounded-xl border border-[#d8e7d7] bg-[#f5f9f3] p-4"><p className="text-sm font-semibold text-[#24453a]">Faça login para iniciar uma análise privada.</p><p className="mt-1 text-xs leading-5 text-[#66806f]">Seus projetos, diagnósticos e referências de arquivo ficam isolados por usuário.</p><Button type="button" onClick={onLogin} className="mt-3 rounded-xl bg-[#173f35] hover:bg-[#285b4a]">Entrar no workspace</Button></div>;
  if (state === "auth_error") return <div className="rounded-xl border border-[#f0b6a8] bg-[#fff2ed] p-4 text-sm text-[#9a4d3e]"><p className="font-semibold">Não foi possível validar sua sessão.</p><Button type="button" variant="outline" onClick={onLogin} className="mt-3 rounded-xl border-[#e9b0a1]">Tentar login novamente</Button></div>;
  return null;
}

export function AnalysisSubmitButton({ isPending }: { isPending: boolean }) {
  return <Button type="submit" disabled={isPending} className="h-11 w-full rounded-xl bg-[#173f35] text-white hover:bg-[#285b4a]">
    {isPending ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" />Analisando estrutura…</> : <><FileSpreadsheet className="mr-2 h-4 w-4" />Iniciar diagnóstico</>}
  </Button>;
}

export function AnalysisProcessingPanel({ fileName }: { fileName?: string }) {
  return <section role="status" aria-live="polite" className="mb-5 rounded-2xl border border-[#c9dfc4] bg-[#f3f8ef] p-4 text-[#27493b]">
    <div className="flex items-start gap-3">
      <span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-white text-[#4a865e] shadow-sm"><Loader2 className="h-5 w-5 animate-spin" /></span>
      <div>
        <p className="font-semibold">Análise em andamento no servidor</p>
        <p className="mt-1 text-xs leading-5 text-[#5e7568]">O tempo varia conforme o tamanho e a estrutura do workbook. Nenhum percentual é estimado enquanto o diagnóstico é processado.</p>
      </div>
    </div>
    <div className="mt-4 grid gap-2 text-xs sm:grid-cols-3">
      <div className="flex items-center gap-2 rounded-xl bg-white/80 p-3"><FileSpreadsheet className="h-4 w-4 text-[#5a8b68]" /><span className="min-w-0 truncate">Arquivo: {fileName ?? "workbook selecionado"}</span></div>
      <div className="flex items-center gap-2 rounded-xl bg-white/80 p-3"><ShieldCheck className="h-4 w-4 text-[#5a8b68]" /><span>Validação e isolamento</span></div>
      <div className="flex items-center gap-2 rounded-xl bg-white/80 p-3"><FileSearch2 className="h-4 w-4 text-[#5a8b68]" /><span>Profiling e diagnóstico</span></div>
    </div>
    <p className="mt-3 text-xs leading-5 text-[#60786a]">A edição do formulário permanece temporariamente bloqueada para preservar a consistência da solicitação enviada.</p>
  </section>;
}

export function AnalysisSuccessNotice({ version, onView }: { version: number; onView: () => void }) {
  return <div className="mt-5 flex items-center justify-between gap-3 rounded-xl border border-[#b8d7a8] bg-[#f1f8ec] p-4 text-sm text-[#315e43]"><span><CheckCircle2 className="mr-2 inline h-4 w-4" />Versão {version} criada com sucesso.</span><Button type="button" variant="outline" className="rounded-xl" onClick={onView}>Ver diagnóstico</Button></div>;
}
