import { afterAll, beforeEach, describe, expect, it, vi } from "vitest";

type Clause = { kind: "eq"; column: string; value: unknown } | { kind: "and"; clauses: Clause[] };
type SortClause = { kind: "desc"; column: string };
type Row = Record<string, unknown>;

const trace = vi.hoisted(() => ({
  rows: {} as Record<string, Row[]>,
  where: [] as Clause[],
  orderBy: [] as SortClause[],
}));

vi.mock("drizzle-orm", async importOriginal => {
  const actual = await importOriginal<typeof import("drizzle-orm")>();
  return {
    ...actual,
    eq: (column: { name: string }, value: unknown): Clause => ({ kind: "eq", column: column.name, value }),
    and: (...clauses: Clause[]): Clause => ({ kind: "and", clauses }),
    desc: (column: { name: string }): SortClause => ({ kind: "desc", column: column.name }),
  };
});

function matches(row: Row, clause: Clause): boolean {
  return clause.kind === "eq" ? row[clause.column] === clause.value : clause.clauses.every(item => matches(row, item));
}

function tableName(table: unknown): string {
  return (table as Record<symbol, string>)[Symbol.for("drizzle:Name")];
}

function createDb() {
  return {
    select: () => ({
      from: (table: unknown) => ({
        where: (condition: Clause) => {
          trace.where.push(condition);
          const getRows = () => trace.rows[tableName(table)].filter(row => matches(row, condition));
          const orderBy = (...sort: SortClause[]) => {
            trace.orderBy.push(...sort);
            const rows = getRows().sort((left, right) => {
              const key = sort[0]?.column;
              return key ? Number(right[key] ?? 0) - Number(left[key] ?? 0) : 0;
            });
            const query = Promise.resolve(rows) as Promise<Row[]> & { limit: (count: number) => Promise<Row[]> };
            query.limit = async count => rows.slice(0, count);
            return query;
          };
          return { orderBy, limit: async (count: number) => getRows().slice(0, count) };
        },
      }),
    }),
  };
}

vi.mock("drizzle-orm/mysql2", () => ({ drizzle: () => createDb() }));

function hasOwnerScope(clause: Clause, ownerId: number): boolean {
  return clause.kind === "eq"
    ? clause.column === "ownerId" && clause.value === ownerId
    : clause.clauses.some(item => hasOwnerScope(item, ownerId));
}

const initialDatabaseUrl = process.env.DATABASE_URL;

describe("analysis database owner scope", () => {
  beforeEach(() => {
    process.env.DATABASE_URL = "mysql://owner-scope-test";
    vi.resetModules();
    trace.where = [];
    trace.orderBy = [];
    trace.rows = {
      analysis_projects: [
        { id: "project-owner-1", ownerId: 1, name: "Projeto de Chris", status: "completed" },
        { id: "project-owner-2", ownerId: 2, name: "Projeto externo", status: "completed" },
      ],
      analysis_diagnostics: [
        { id: "diagnostic-owner-1-v1", projectId: "project-owner-1", ownerId: 1, version: 1 },
        { id: "diagnostic-owner-1-v2", projectId: "project-owner-1", ownerId: 1, version: 2 },
        { id: "diagnostic-foreign-on-shared-project", projectId: "project-owner-1", ownerId: 2, version: 99 },
        { id: "diagnostic-owner-2", projectId: "project-owner-2", ownerId: 2, version: 1 },
      ],
    };
  });

  afterAll(() => {
    if (initialDatabaseUrl === undefined) delete process.env.DATABASE_URL;
    else process.env.DATABASE_URL = initialDatabaseUrl;
  });

  it("returns only the owner project and excludes a foreign diagnostic even if it targets the same project id", async () => {
    const { listAnalysisProjectsForOwner } = await import("./db");
    const projects = await listAnalysisProjectsForOwner(1);

    expect(projects).toHaveLength(1);
    expect(projects[0]).toMatchObject({ id: "project-owner-1", ownerId: 1, lastDiagnosticId: "diagnostic-owner-1-v2", lastDiagnosticVersion: 2 });
    expect(trace.where).toHaveLength(2);
    expect(trace.where.every(clause => hasOwnerScope(clause, 1))).toBe(true);
  });

  it("does not resolve a diagnostic owned by a different user", async () => {
    const { getAnalysisDiagnosticForOwner } = await import("./db");
    const diagnostic = await getAnalysisDiagnosticForOwner("diagnostic-owner-2", 1);

    expect(diagnostic).toBeUndefined();
    expect(trace.where).toHaveLength(1);
    expect(hasOwnerScope(trace.where[0], 1)).toBe(true);
  });

  it("excludes a foreign project and calculates the next version from owner-scoped diagnostics only", async () => {
    const { getAnalysisProjectForOwner, getNextDiagnosticVersion } = await import("./db");
    const foreignProject = await getAnalysisProjectForOwner("project-owner-2", 1);
    const nextVersion = await getNextDiagnosticVersion("project-owner-1", 1);

    expect(foreignProject).toBeUndefined();
    expect(nextVersion).toBe(3);
    expect(trace.where).toHaveLength(2);
    expect(trace.where.every(clause => hasOwnerScope(clause, 1))).toBe(true);
  });
});
