# Evidência de Fluxo de Autenticação — UI-AUTH-001

O workspace usa `useAuth()` e `startLogin()` sem construir URL de OAuth durante a renderização. A função pura `getAnalysisUiState()` explicita seis estados: carregamento de autenticação, login obrigatório, erro de autenticação, pronto, análise em execução e sucesso.

| Estado | Comportamento do workspace |
|---|---|
| `auth_loading` | Mantém o formulário indisponível enquanto a sessão é verificada. |
| `sign_in_required` | Explica que o workspace é privado e oferece o botão de login. |
| `auth_error` | Exibe mensagem de sessão indisponível e permite reiniciar o login. |
| `ready` | Permite selecionar e enviar XLSX. |
| `analyzing` | Desabilita o envio e exibe progresso. |
| `success` | Confirma a versão criada e direciona o usuário ao diagnóstico. |

As consultas privadas são habilitadas somente após `isAuthenticated`, e o procedimento de análise interrompe o envio e inicia login se uma sessão não estiver presente.
