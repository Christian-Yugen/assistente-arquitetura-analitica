import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("E2E environment requirements", () => {
  it("exige isolamento verificável e impede reutilização do ambiente atual", () => {
    const requirements = readFileSync(resolve(root, "docs/gates/E2E_ENVIRONMENT_REQUIREMENTS_001.md"), "utf8");

    expect(requirements).toContain("não cria ambiente, banco, armazenamento");
    expect(requirements).toContain("nenhuma URL, tabela ou migração compartilhada com o ambiente atual");
    expect(requirements).toContain("sem reutilizar segredo de produção");
    expect(requirements).toContain("Dois owners de teste");
    expect(requirements).toContain("Workbooks criados sinteticamente");
    expect(requirements).toContain("não será declarada como deleção física");
    expect(requirements).toContain("fail-closed");
    expect(requirements).toContain("não demonstra uma segunda implantação");
    expect(requirements).toContain("Nenhuma cópia manual de credencial, banco ou objeto do ambiente atual");
    expect(requirements).toContain("não expôs integração, ambiente ou comando suportado de provisionamento E2E/WebDev separado");
    expect(requirements).toContain("não há via verificável para criar o ambiente isolado");
    expect(requirements).toContain("não autoriza reutilizar a aplicação local, o banco atual ou qualquer armazenamento existente");
    expect(requirements).toContain("Aprovação dos cenários não libera produção");
  });
});
