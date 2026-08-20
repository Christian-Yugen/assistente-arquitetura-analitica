import { useAuth } from "@/_core/hooks/useAuth";
import { startLogin } from "@/const";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarInset,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
} from "@/components/ui/sidebar";
import { BarChart3, Clock3, FileSearch2, FolderKanban, LogOut, PanelLeft, ShieldCheck } from "lucide-react";
import { ReactNode, useState } from "react";

const navigation = [
  { icon: BarChart3, label: "Visão geral", href: "#visao-geral" },
  { icon: FileSearch2, label: "Nova análise", href: "#nova-analise" },
  { icon: FolderKanban, label: "Projetos", href: "#projetos" },
  { icon: Clock3, label: "Versões", href: "#versoes" },
];

export default function DashboardLayout({ children }: { children: ReactNode }) {
  const { loading, user, logout } = useAuth();
  const [collapsed, setCollapsed] = useState(false);

  if (loading) {
    return <div className="min-h-screen bg-[#f8f7f2]" />;
  }

  if (!user) {
    return (
      <main className="min-h-screen bg-[#f8f7f2] px-5 py-8 text-[#18332c] sm:px-10">
        <div className="mx-auto flex min-h-[80vh] max-w-5xl items-center">
          <section className="grid w-full overflow-hidden rounded-[2rem] border border-[#d9dfd4] bg-white shadow-[0_24px_70px_rgba(29,61,50,0.08)] md:grid-cols-[1.1fr_0.9fr]">
            <div className="p-8 sm:p-12">
              <div className="mb-12 flex items-center gap-3 text-sm font-semibold tracking-[0.18em] text-[#4f7d65] uppercase">
                <span className="grid h-9 w-9 place-items-center rounded-xl bg-[#173f35] text-xs text-white">A</span>
                Arquitetura Analítica
              </div>
              <p className="mb-4 text-sm font-medium text-[#6b7b72]">Diagnóstico dimensional para Power BI</p>
              <h1 className="max-w-xl font-serif text-4xl leading-tight tracking-[-0.04em] text-[#18332c] sm:text-5xl">
                Transforme planilhas em decisões de modelagem explicadas.
              </h1>
              <p className="mt-6 max-w-lg text-base leading-7 text-[#627168]">
                Envie uma planilha XLSX para receber uma leitura técnica estruturada, com evidências, riscos e perguntas de validação.
              </p>
              <Button className="mt-9 h-11 rounded-xl bg-[#173f35] px-6 text-white hover:bg-[#275b4a]" onClick={() => startLogin()}>
                Entrar no workspace
              </Button>
            </div>
            <div className="relative hidden overflow-hidden bg-[#173f35] p-12 text-[#ecf4ea] md:block">
              <div className="absolute -right-12 -top-12 h-56 w-56 rounded-full border border-white/15" />
              <div className="absolute -bottom-24 -left-20 h-64 w-64 rounded-full bg-[#7da77a]/25 blur-2xl" />
              <div className="relative mt-24 rounded-2xl border border-white/15 bg-white/10 p-6 backdrop-blur">
                <ShieldCheck className="mb-8 h-8 w-8 text-[#b8d7a7]" />
                <p className="font-serif text-2xl leading-snug">Dados isolados por usuário. Recomendações sempre rastreáveis.</p>
              </div>
            </div>
          </section>
        </div>
      </main>
    );
  }

  return (
    <SidebarProvider defaultOpen={!collapsed}>
      <Sidebar collapsible="icon" className="border-r border-[#dce3da] bg-[#f1f3ec]">
        <SidebarHeader className="h-20 justify-center px-3">
          <div className="flex items-center gap-3">
            <button aria-label="Alternar navegação" onClick={() => setCollapsed(value => !value)} className="grid h-9 w-9 place-items-center rounded-xl bg-[#173f35] text-white transition-transform active:scale-95">
              <PanelLeft className="h-4 w-4" />
            </button>
            <div className="min-w-0 group-data-[collapsible=icon]:hidden">
              <p className="text-xs font-semibold tracking-[0.16em] text-[#4f7d65] uppercase">Workspace</p>
              <p className="truncate font-serif text-lg text-[#18332c]">Arquitetura</p>
            </div>
          </div>
        </SidebarHeader>
        <SidebarContent className="px-2 py-4">
          <SidebarMenu>
            {navigation.map(item => (
              <SidebarMenuItem key={item.href}>
                <SidebarMenuButton asChild tooltip={item.label} className="h-11 rounded-xl text-[#496158] hover:bg-[#dfe9dd] hover:text-[#18332c] data-[active=true]:bg-[#d5e5d0]">
                  <a href={item.href}>
                    <item.icon className="h-4 w-4" />
                    <span>{item.label}</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
            ))}
          </SidebarMenu>
          <div className="mx-2 mt-8 rounded-xl border border-[#dbe5d8] bg-[#f8faf5] p-3 group-data-[collapsible=icon]:hidden">
            <p className="text-xs font-medium text-[#456d59]">Modo draft protegido</p>
            <p className="mt-1 text-[11px] leading-4 text-[#718078]">Recomendações seguem regras e gates versionados.</p>
          </div>
        </SidebarContent>
        <SidebarFooter className="p-3">
          <div className="flex items-center gap-3 rounded-xl px-2 py-2 hover:bg-[#e3ebe1]">
            <Avatar className="h-8 w-8 border border-[#cbd9ca]">
              <AvatarFallback className="bg-[#d4e5d0] text-xs font-bold text-[#315d49]">{user.name?.slice(0, 1).toUpperCase() ?? "U"}</AvatarFallback>
            </Avatar>
            <div className="min-w-0 flex-1 group-data-[collapsible=icon]:hidden">
              <p className="truncate text-xs font-semibold text-[#28483d]">{user.name ?? "Usuário"}</p>
              <p className="truncate text-[11px] text-[#78847e]">{user.email ?? "Sessão protegida"}</p>
            </div>
            <button className="text-[#668073] transition-colors hover:text-[#b24b3a] group-data-[collapsible=icon]:hidden" onClick={logout} aria-label="Sair">
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        </SidebarFooter>
      </Sidebar>
      <SidebarInset className="bg-[#f8f7f2]">{children}</SidebarInset>
    </SidebarProvider>
  );
}
