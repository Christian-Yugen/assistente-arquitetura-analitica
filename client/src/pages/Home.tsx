import DashboardLayout from "@/components/DashboardLayout";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { trpc } from "@/lib/trpc";
import { getAnalysisUiState } from "@/lib/analysisUiState";
import { downloadDiagnosticJson } from "@/lib/diagnosticExport";
import { useAuth } from "@/_core/hooks/useAuth";
import { startLogin } from "@/const";
import { AnalysisAuthNotice, AnalysisProcessingPanel, AnalysisSubmitButton, AnalysisSuccessNotice } from "@/components/AnalysisFlowState";
import { AlertTriangle, ArrowUpRight, CheckCircle2, Clock3, Download, FileSpreadsheet, FileUp, Loader2, ShieldCheck, Sparkles } from "lucide-react";
import React, { ChangeEvent, FormEvent, useMemo, useState } from "react";
import { toast } from "sonner";

const MAX_FILE_BYTES = 25 * 1024 * 1024;

function record(value: unknown): Record<string, unknown> {
  return value && typeof value === "object" ? value as Record<string, unknown> : {};
}

function getCount(payload: Record<string, unknown>, key: string) {
  const summary = record(payload.summary);
  const counts = record(summary.counts);
  return typeof counts[key] === "number" ? counts[key] : 0;
}

export default function Home() {
  const { loading: authLoading, isAuthenticated, error: authError } = useAuth();
  const [projectName, setProjectName] = useState("");
  const [objective, setObjective] = useState("Analisar a estrutura da planilha para modelagem dimensional.");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedDiagnosticId, setSelectedDiagnosticId] = useState<string | null>(null);
  const utils = trpc.useUtils();
  const projectsQuery = trpc.analysis.listProjects.useQuery(undefined, { enabled: isAuthenticated });
  const diagnosticQuery = trpc.analysis.getDiagnostic.useQuery(
    { diagnosticId: selectedDiagnosticId ?? "00000000-0000-4000-8000-000000000000" },
    { enabled: isAuthenticated && Boolean(selectedDiagnosticId) },
  );
  const analyze = trpc.analysis.analyzeWorkbook.useMutation({
    onSuccess: async result => {
      setSelectedDiagnosticId(result.diagnosticId);
      await utils.analysis.listProjects.invalidate();
      toast.success("Diagnóstico draft concluído e versionado.");
    },
    onError: error => toast.error(error.message),
  });

  const diagnosticPayload = useMemo(() => record(diagnosticQuery.data?.payload), [diagnosticQuery.data]);
  const activeFindingCount = Array.isArray(diagnosticPayload.findings) ? diagnosticPayload.findings.length : getCount(diagnosticPayload, "risks");
  const activeQuestionCount = Array.isArray(diagnosticPayload.questions) ? diagnosticPayload.questions.length : 0;
  const findings = Array.isArray(diagnosticPayload.findings) ? diagnosticPayload.findings.map(record) : [];
  const questions = Array.isArray(diagnosticPayload.questions) ? diagnosticPayload.questions.map(record) : [];
  const retention = record(record(diagnosticPayload.file).retention);
  const uiState = getAnalysisUiState({ authLoading, isAuthenticated, authError: Boolean(authError), isAnalyzing: analyze.isPending, isSuccess: analyze.isSuccess });

  async function onFileChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0] ?? null;
    if (!file) return;
    if (!file.name.toLowerCase().endsWith(".xlsx")) {
      toast.error("Selecione um arquivo no formato XLSX.");
      event.target.value = "";
      return;
    }
    if (file.size > MAX_FILE_BYTES) {
      toast.error("O limite de upload é 25 MB.");
      event.target.value = "";
      return;
    }
    setSelectedFile(file);
    if (!projectName) setProjectName(file.name.replace(/\.xlsx$/i, ""));
  }

  async function toBase64(file: File) {
    const bytes = new Uint8Array(await file.arrayBuffer());
    let binary = "";
    const chunk = 0x8000;
    for (let index = 0; index < bytes.length; index += chunk) {
      const current = bytes.subarray(index, index + chunk);
      let part = "";
      for (let offset = 0; offset < current.length; offset += 1) part += String.fromCharCode(current[offset]);
      binary += part;
    }
    return btoa(binary);
  }

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!isAuthenticated) {
      toast.info("Faça login para iniciar uma análise privada.");
      startLogin();
      return;
    }
    if (!selectedFile) return toast.error("Selecione uma planilha XLSX para iniciar.");
    try {
      const dataBase64 = await toBase64(selectedFile);
      analyze.mutate({ projectName: projectName.trim(), objective: objective.trim(), fileName: selectedFile.name, mimeType: selectedFile.type || "application/octet-stream", dataBase64 });
    } catch {
      toast.error("Não foi possível preparar o arquivo para análise.");
    }
  }

  function exportDiagnostic() {
    if (!diagnosticQuery.data) return;
    try {
      downloadDiagnosticJson(diagnosticQuery.data);
      toast.success("Diagnóstico JSON preparado para download.");
    } catch {
      toast.error("Não foi possível preparar a exportação JSON.");
    }
  }

  return (
    <DashboardLayout>
      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-8 sm:py-8">
        <section id="visao-geral" className="mb-8 flex flex-col gap-5 border-b border-[#e0e4dc] pb-8 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <div className="mb-3 flex items-center gap-2 text-xs font-semibold tracking-[0.14em] text-[#5a8068] uppercase"><Sparkles className="h-3.5 w-3.5" /> Motor de diagnóstico dimensional</div>
            <h1 className="font-serif text-3xl tracking-[-0.035em] text-[#18332c] sm:text-4xl">Leia a planilha antes de modelar.</h1>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-[#65746c]">Uma análise controlada para revelar estrutura, qualidade e próximos pontos de validação antes do Power BI.</p>
          </div>
          <div className="flex items-center gap-3 rounded-2xl border border-[#dbe4d9] bg-white px-4 py-3 text-sm shadow-sm">
            <ShieldCheck className="h-5 w-5 text-[#4e8a66]" />
            <div><p className="font-semibold text-[#25483d]">Ambiente isolado</p><p className="text-xs text-[#748078]">Referência do arquivo removida após a análise</p></div>
          </div>
        </section>

        <section className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <Card id="nova-analise" className="overflow-hidden rounded-[1.5rem] border-[#dbe3d9] bg-white shadow-[0_18px_45px_rgba(29,61,50,0.06)]">
            <CardContent className="p-6 sm:p-8">
              <div className="mb-7 flex items-start justify-between gap-4"><div><p className="text-xs font-semibold tracking-[0.13em] text-[#5a8068] uppercase">Nova análise</p><h2 className="mt-2 font-serif text-2xl text-[#18332c]">Enviar workbook</h2></div><Badge variant="secondary" className="rounded-full bg-[#edf4e9] px-3 py-1 text-[#47795b]">XLSX · até 25 MB</Badge></div>
              <AnalysisAuthNotice state={uiState} onLogin={startLogin} />
              {uiState === "analyzing" ? <AnalysisProcessingPanel fileName={selectedFile?.name} /> : null}
              {uiState === "ready" || uiState === "analyzing" || uiState === "success" ? <form onSubmit={submit} className="space-y-5">
                <div className="space-y-2"><Label htmlFor="projectName">Nome do projeto</Label><Input id="projectName" value={projectName} onChange={event => setProjectName(event.target.value)} placeholder="Ex.: Operação comercial" className="h-11 rounded-xl border-[#d8e1d7] bg-[#fbfcfa]" disabled={analyze.isPending} required /></div>
                <div className="space-y-2"><Label htmlFor="objective">Objetivo da análise</Label><Textarea id="objective" value={objective} onChange={event => setObjective(event.target.value)} className="min-h-24 rounded-xl border-[#d8e1d7] bg-[#fbfcfa]" disabled={analyze.isPending} required /></div>
                <label className={`group flex items-center gap-4 rounded-2xl border border-dashed border-[#a8c4aa] bg-[#f5f9f3] p-5 transition-colors ${analyze.isPending ? "cursor-not-allowed opacity-70" : "cursor-pointer hover:bg-[#edf5ea]"}`}>
                  <span className="grid h-11 w-11 place-items-center rounded-xl bg-white text-[#4b815d] shadow-sm"><FileUp className="h-5 w-5" /></span>
                  <span className="min-w-0 flex-1"><span className="block truncate text-sm font-semibold text-[#24453a]">{selectedFile ? selectedFile.name : "Escolha a planilha XLSX"}</span><span className="mt-1 block text-xs text-[#718177]">Limite de 10 abas · dados lidos somente no servidor</span></span>
                  <input className="sr-only" type="file" accept=".xlsx,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" onChange={onFileChange} disabled={analyze.isPending} />
                </label>
                <AnalysisSubmitButton isPending={analyze.isPending} />
              </form> : null}
              {uiState === "success" && analyze.data ? <AnalysisSuccessNotice version={analyze.data.version} onView={() => document.getElementById("versoes")?.scrollIntoView({ behavior: "smooth" })} /> : null}
            </CardContent>
          </Card>

          <div className="grid gap-4 sm:grid-cols-3 lg:grid-cols-1">
              {[
              { label: "Regras executáveis", value: "9", detail: "QLT-001 a QLT-009", icon: CheckCircle2, color: "text-[#39825a] bg-[#ebf5eb]" },
              { label: "Catálogo governado", value: "95", detail: "slots versionados", icon: Sparkles, color: "text-[#5774a8] bg-[#eef2fb]" },
              { label: "Gate histórico", value: "G7.5", detail: "linhagem canônica pendente", icon: AlertTriangle, color: "text-[#ad7040] bg-[#fcf2e5]" },
            ].map(item => <Card key={item.label} className="rounded-2xl border-[#e0e6df] bg-white"><CardContent className="flex items-center gap-4 p-5"><span className={`grid h-10 w-10 place-items-center rounded-xl ${item.color}`}><item.icon className="h-5 w-5" /></span><div><p className="text-xs text-[#7b8981]">{item.label}</p><p className="mt-0.5 font-serif text-xl text-[#223f35]">{item.value}</p><p className="text-xs text-[#68786f]">{item.detail}</p></div></CardContent></Card>)}
          </div>
        </section>

        <section className="mt-8 grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
          <Card id="projetos" className="rounded-[1.5rem] border-[#dfe5dc] bg-white"><CardContent className="p-6"><div className="mb-5 flex items-center justify-between"><div><p className="text-xs font-semibold tracking-[0.12em] text-[#66816e] uppercase">Projetos recentes</p><h2 className="mt-1 font-serif text-2xl text-[#18332c]">Histórico de análises</h2></div><Clock3 className="h-5 w-5 text-[#7a9680]" /></div>
            {projectsQuery.isLoading ? <div className="py-10 text-center text-sm text-[#718078]">Carregando seus projetos…</div> : projectsQuery.isError ? <div className="rounded-xl bg-[#fff3ef] p-5 text-sm leading-6 text-[#9a4d3e]">Não foi possível carregar seus projetos agora. Atualize a página para tentar novamente.</div> : projectsQuery.data?.length ? <div className="space-y-2">{projectsQuery.data.slice(0, 6).map(project => <button key={project.id} disabled={!project.lastDiagnosticId} onClick={() => project.lastDiagnosticId && setSelectedDiagnosticId(project.lastDiagnosticId)} className="flex w-full items-center gap-3 rounded-xl border border-transparent p-3 text-left transition-colors hover:border-[#dbe7d9] hover:bg-[#f6f9f5] disabled:cursor-not-allowed disabled:opacity-60"><span className="grid h-9 w-9 place-items-center rounded-lg bg-[#edf3ea] text-[#578066]"><FileSpreadsheet className="h-4 w-4" /></span><span className="min-w-0 flex-1"><span className="block truncate text-sm font-semibold text-[#2d4c40]">{project.name}</span><span className="block text-xs text-[#77867c]">{project.status.replaceAll("_", " ")} · {project.lastDiagnosticVersion ? `v${project.lastDiagnosticVersion}` : "sem versão"}</span></span><ArrowUpRight className="h-4 w-4 text-[#9aac9d]" /></button>)}</div> : <div className="rounded-xl bg-[#f7f9f5] p-5 text-sm leading-6 text-[#718078]">Seu histórico aparecerá aqui após a primeira análise concluída.</div>}</CardContent></Card>

          <Card id="versoes" className="rounded-[1.5rem] border-[#dfe5dc] bg-[#173f35] text-white"><CardContent className="p-6"><div className="mb-7 flex items-center justify-between gap-3"><div><p className="text-xs font-semibold tracking-[0.12em] text-[#a9cfac] uppercase">Diagnóstico selecionado</p><h2 className="mt-1 font-serif text-2xl">{diagnosticQuery.data ? `Versão ${diagnosticQuery.data.version}` : "Aguardando análise"}</h2></div>{diagnosticQuery.data ? <Button type="button" onClick={exportDiagnostic} variant="outline" className="border-white/20 bg-white/8 text-white hover:bg-white/15 hover:text-white"><Download className="h-4 w-4" />Exportar JSON</Button> : <span className="rounded-full border border-white/15 px-3 py-1 text-xs text-[#d0e3ce]">Contrato v1.0</span>}</div>
            {diagnosticQuery.isFetching ? <div className="flex min-h-44 items-center justify-center"><Loader2 className="h-5 w-5 animate-spin text-[#b4d4ad]" /></div> : diagnosticQuery.isError ? <div className="rounded-xl border border-[#ffb9a9] bg-[#fff1ed] p-5 text-sm leading-6 text-[#8c3d31]">Não foi possível abrir esta versão de diagnóstico. Verifique sua sessão e tente novamente.</div> : diagnosticQuery.data ? <div className="space-y-5"><div className="grid gap-3 sm:grid-cols-3">{[{ label: "Achados", value: activeFindingCount }, { label: "Perguntas", value: activeQuestionCount }, { label: "Abas", value: getCount(diagnosticPayload, "sheets") }].map(metric => <div key={metric.label} className="rounded-xl border border-white/10 bg-white/8 p-4"><p className="text-xs text-[#b9cfc0]">{metric.label}</p><p className="mt-1 font-serif text-3xl">{metric.value}</p></div>)}</div><section aria-labelledby="findings-heading"><div className="mb-2 flex items-center justify-between"><h3 id="findings-heading" className="text-xs font-semibold tracking-[0.12em] text-[#b8d9b7] uppercase">Achados de qualidade</h3><span className="text-xs text-[#b9cfc0]">{findings.length} registrado{findings.length === 1 ? "" : "s"}</span></div>{findings.length ? <div className="grid gap-3 sm:grid-cols-2">{findings.map((finding, index) => <article key={String(finding.finding_id ?? index)} className="rounded-xl border border-white/10 bg-white/8 p-4"><p className="text-xs font-semibold text-[#b8d9b7]">ACHADO</p><p className="mt-1 text-sm font-semibold text-white">{String(finding.title ?? "Achado de qualidade")}</p><p className="mt-1 text-xs leading-5 text-[#c7d8c8]">{String(finding.description ?? finding.impact ?? "Sem descrição adicional.")}</p>{finding.recommendation ? <p className="mt-3 rounded-lg border border-[#b8d7a7]/20 bg-[#b8d7a7]/10 p-3 text-xs leading-5 text-[#e0efdc]"><span className="font-semibold">Recomendação derivada: </span>{String(finding.recommendation)}</p> : null}</article>)}</div> : <p className="rounded-xl border border-dashed border-white/20 p-4 text-xs leading-5 text-[#c7d8c8]">Nenhum achado de qualidade foi emitido por este diagnóstico draft.</p>}</section><section aria-labelledby="questions-heading"><div className="mb-2 flex items-center justify-between"><h3 id="questions-heading" className="text-xs font-semibold tracking-[0.12em] text-[#cde9bb] uppercase">Perguntas de validação</h3><span className="text-xs text-[#b9cfc0]">{questions.length} pendente{questions.length === 1 ? "" : "s"}</span></div>{questions.length ? <div className="grid gap-3 sm:grid-cols-2">{questions.map((question, index) => <article key={String(question.question_id ?? index)} className="rounded-xl border border-[#b8d7a7]/25 bg-[#b8d7a7]/10 p-4"><p className="text-xs font-semibold text-[#cde9bb]">VALIDAÇÃO PENDENTE</p><p className="mt-1 text-sm font-semibold text-white">{String(question.text ?? "Pergunta pendente")}</p><p className="mt-1 text-xs leading-5 text-[#d5e7d5]">{String(question.reason ?? "A resposta influencia o diagnóstico.")}</p></article>)}</div> : <p className="rounded-xl border border-dashed border-white/20 p-4 text-xs leading-5 text-[#c7d8c8]">Não há perguntas pendentes para esta versão do diagnóstico.</p>}</section><div className="rounded-xl border border-white/10 bg-white/8 p-4 text-xs leading-5 text-[#d5e5d4]">Retenção: {String(retention.status ?? "referência controlada")} {retention.delete_at ? `· exclusão prevista em ${new Date(String(retention.delete_at)).toLocaleString("pt-BR")}` : "· o arquivo não é exibido no histórico"}.</div><div className="rounded-xl border border-white/10 bg-white/8 p-4 text-sm leading-6 text-[#d5e5d4]">O resultado permanece em modo draft: recomendações de modelo, relacionamentos e métricas só serão habilitadas após os próximos ciclos de regras e calibração.</div></div> : <div className="min-h-44 rounded-xl border border-dashed border-white/20 p-6 text-sm leading-6 text-[#c2d4c4]">Selecione um projeto concluído para consultar seus achados, perguntas de validação e versão de diagnóstico.</div>}</CardContent></Card>
        </section>
      </main>
    </DashboardLayout>
  );
}
