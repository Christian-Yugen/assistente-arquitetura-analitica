import React from "react";
import { Button } from "@/components/ui/button";
import { CheckCircle2, FileSpreadsheet, Loader2 } from "lucide-react";
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

export function AnalysisSuccessNotice({ version, onView }: { version: number; onView: () => void }) {
  return <div className="mt-5 flex items-center justify-between gap-3 rounded-xl border border-[#b8d7a8] bg-[#f1f8ec] p-4 text-sm text-[#315e43]"><span><CheckCircle2 className="mr-2 inline h-4 w-4" />Versão {version} criada com sucesso.</span><Button type="button" variant="outline" className="rounded-xl" onClick={onView}>Ver diagnóstico</Button></div>;
}
