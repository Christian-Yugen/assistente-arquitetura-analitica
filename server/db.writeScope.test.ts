import { afterAll, beforeEach, describe, expect, it, vi } from "vitest";

type Clause = { kind: "eq"; column: string; value: unknown } | { kind: "and"; clauses: Clause[] };
type Mutation = { table: string; values: Record<string, unknown>; where?: Clause };

const trace = vi.hoisted(() => ({
  inserts: [] as Mutation[],
  updates: [] as Mutation[],
}));

vi.mock("drizzle-orm", async importOriginal => {
  const actual = await importOriginal<typeof import("drizzle-orm")>();
  return {
    ...actual,
    eq: (column: { name: string }, value: unknown): Clause => ({ kind: "eq", column: column.name, value }),
    and: (...clauses: Clause[]): Clause => ({ kind: "and", clauses }),
  };
});

function tableName(table: unknown): string {
  return (table as Record<symbol, string>)[Symbol.for("drizzle:Name")];
}

function createDb() {
  return {
    select: () => ({
      from: () => ({
        where: () => ({ limit: async () => [] }),
      }),
    }),
    insert: (table: unknown) => ({
      values: async (values: Record<string, unknown>) => {
        trace.inserts.push({ table: tableName(table), values });
      },
    }),
    update: (table: unknown) => ({
      set: (values: Record<string, unknown>) => ({
        where: async (where: Clause) => {
          trace.updates.push({ table: tableName(table), values, where });
        },
      }),
    }),
  };
}

vi.mock("drizzle-orm/mysql2", () => ({ drizzle: () => createDb() }));

function hasOwnerScope(clause: Clause | undefined, ownerId: number): boolean {
  if (!clause) return false;
  return clause.kind === "eq"
    ? clause.column === "ownerId" && clause.value === ownerId
    : clause.clauses.some(item => hasOwnerScope(item, ownerId));
}

const initialDatabaseUrl = process.env.DATABASE_URL;

describe("analysis database write scope and retention", () => {
  beforeEach(() => {
    process.env.DATABASE_URL = "mysql://write-scope-test";
    vi.resetModules();
    trace.inserts = [];
    trace.updates = [];
  });

  afterAll(() => {
    if (initialDatabaseUrl === undefined) delete process.env.DATABASE_URL;
    else process.env.DATABASE_URL = initialDatabaseUrl;
  });

  it("creates project, file and diagnostic for one owner and removes only that owner's storage reference", async () => {
    const db = await import("./db");
    const ownerId = 77;
    const projectId = "11111111-1111-4111-8111-111111111111";
    const fileId = "22222222-2222-4222-8222-222222222222";
    const diagnosticId = "33333333-3333-4333-8333-333333333333";

    await db.createAnalysisProject({ id: projectId, ownerId, name: "Projeto seguro", domain: "generic" });
    await db.createAnalysisFile({ id: fileId, projectId, ownerId, originalName: "workbook.xlsx", storageKey: "analysis/77/file.xlsx", sha256: "abc", mimeType: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", sizeBytes: 128, sheetCount: 1, analyzableSheetCount: 1, retentionStatus: "private_active" });
    await db.createAnalysisDiagnostic({ id: diagnosticId, projectId, ownerId, fileId, version: 1, status: "completed_with_warnings", contractVersion: "1.0.0-reconstructed.1", engineVersion: "0.1.0", rulesetVersion: "0.7.0-draft", payload: { analysis: { status: "completed_with_warnings" } } });
    await db.updateAnalysisProjectStatus(projectId, ownerId, "completed");
    await db.markFileReferenceRemoved(fileId, ownerId);

    expect(trace.inserts).toHaveLength(3);
    expect(trace.inserts.map(item => item.table)).toEqual(["analysis_projects", "analysis_files", "analysis_diagnostics"]);
    expect(trace.inserts.every(item => item.values.ownerId === ownerId)).toBe(true);

    const projectUpdate = trace.updates.find(item => item.table === "analysis_projects");
    const retentionUpdate = trace.updates.find(item => item.table === "analysis_files");
    expect(projectUpdate).toMatchObject({ values: { status: "completed" } });
    expect(hasOwnerScope(projectUpdate?.where, ownerId)).toBe(true);
    expect(retentionUpdate?.values).toMatchObject({ storageKey: null, retentionStatus: "reference_removed" });
    expect(retentionUpdate?.values.referenceRemovedAt).toBeInstanceOf(Date);
    expect(hasOwnerScope(retentionUpdate?.where, ownerId)).toBe(true);
  });
});
