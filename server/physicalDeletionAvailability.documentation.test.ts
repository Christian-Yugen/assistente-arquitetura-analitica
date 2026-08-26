import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const root = resolve(import.meta.dirname, "..");

describe("physical deletion availability gate", () => {
  it("confirma que a camada atual não expõe deleção e mantém produção bloqueada", () => {
    const storage = readFileSync(resolve(root, "server/storage.ts"), "utf8");
    const gate = readFileSync(resolve(root, "docs/gates/PHYSICAL_DELETION_AVAILABILITY_001.md"), "utf8");
    expect(storage).toContain("export async function storagePut");
    expect(storage).toContain("export async function storageGet");
    expect(storage).toContain("export async function storageGetSignedUrl");
    expect(storage).not.toMatch(/function storageDelete|export async function storageDelete|presign\/delete/i);
    expect(gate).toContain("não expõe helper, endpoint ou operação de `DELETE`");
    expect(gate).toContain("Produção permanece bloqueada");
    expect(gate).toContain("Não é permitido simular exclusão física");
  });
});
