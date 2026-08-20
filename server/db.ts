import { and, desc, eq } from "drizzle-orm";
import { drizzle } from "drizzle-orm/mysql2";
import { analysisDiagnostics, analysisFiles, analysisProjects, InsertUser, users } from "../drizzle/schema";
import { ENV } from './_core/env';
import { buildReferenceRemovalAudit } from "./analysisRetention";

let _db: ReturnType<typeof drizzle> | null = null;

// Lazily create the drizzle instance so local tooling can run without a DB.
export async function getDb() {
  if (!_db && process.env.DATABASE_URL) {
    try {
      _db = drizzle(process.env.DATABASE_URL);
    } catch (error) {
      console.warn("[Database] Failed to connect:", error);
      _db = null;
    }
  }
  return _db;
}

export async function upsertUser(user: InsertUser): Promise<void> {
  if (!user.openId) {
    throw new Error("User openId is required for upsert");
  }

  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot upsert user: database not available");
    return;
  }

  try {
    const values: InsertUser = {
      openId: user.openId,
    };
    const updateSet: Record<string, unknown> = {};

    const textFields = ["name", "email", "loginMethod"] as const;
    type TextField = (typeof textFields)[number];

    const assignNullable = (field: TextField) => {
      const value = user[field];
      if (value === undefined) return;
      const normalized = value ?? null;
      values[field] = normalized;
      updateSet[field] = normalized;
    };

    textFields.forEach(assignNullable);

    if (user.lastSignedIn !== undefined) {
      values.lastSignedIn = user.lastSignedIn;
      updateSet.lastSignedIn = user.lastSignedIn;
    }
    if (user.role !== undefined) {
      values.role = user.role;
      updateSet.role = user.role;
    } else if (user.openId === ENV.ownerOpenId) {
      values.role = 'admin';
      updateSet.role = 'admin';
    }

    if (!values.lastSignedIn) {
      values.lastSignedIn = new Date();
    }

    if (Object.keys(updateSet).length === 0) {
      updateSet.lastSignedIn = new Date();
    }

    await db.insert(users).values(values).onDuplicateKeyUpdate({
      set: updateSet,
    });
  } catch (error) {
    console.error("[Database] Failed to upsert user:", error);
    throw error;
  }
}

export async function getUserByOpenId(openId: string) {
  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot get user: database not available");
    return undefined;
  }

  const result = await db.select().from(users).where(eq(users.openId, openId)).limit(1);

  return result.length > 0 ? result[0] : undefined;
}

export async function createAnalysisProject(input: { id: string; ownerId: number; name: string; domain: "generic" | "sso" | "hr" }) {
  const db = await getDb();
  if (!db) throw new Error("Banco de dados indisponível.");
  await db.insert(analysisProjects).values(input);
  return getAnalysisProjectForOwner(input.id, input.ownerId);
}

export async function getAnalysisProjectForOwner(projectId: string, ownerId: number) {
  const db = await getDb();
  if (!db) throw new Error("Banco de dados indisponível.");
  const [project] = await db.select().from(analysisProjects).where(and(eq(analysisProjects.id, projectId), eq(analysisProjects.ownerId, ownerId))).limit(1);
  return project;
}

export async function listAnalysisProjectsForOwner(ownerId: number) {
  const db = await getDb();
  if (!db) throw new Error("Banco de dados indisponível.");
  const projects = await db.select().from(analysisProjects).where(eq(analysisProjects.ownerId, ownerId)).orderBy(desc(analysisProjects.createdAt));
  return Promise.all(projects.map(async project => {
    const [latest] = await db.select({ id: analysisDiagnostics.id, version: analysisDiagnostics.version })
      .from(analysisDiagnostics)
      .where(and(eq(analysisDiagnostics.projectId, project.id), eq(analysisDiagnostics.ownerId, ownerId)))
      .orderBy(desc(analysisDiagnostics.version))
      .limit(1);
    return { ...project, lastDiagnosticId: latest?.id ?? null, lastDiagnosticVersion: latest?.version ?? null };
  }));
}

export async function updateAnalysisProjectStatus(projectId: string, ownerId: number, status: "draft" | "uploading" | "analyzing" | "completed" | "failed") {
  const db = await getDb();
  if (!db) throw new Error("Banco de dados indisponível.");
  await db.update(analysisProjects).set({ status, completedAt: status === "completed" || status === "failed" ? new Date() : null }).where(and(eq(analysisProjects.id, projectId), eq(analysisProjects.ownerId, ownerId)));
}

export async function createAnalysisFile(input: typeof analysisFiles.$inferInsert) {
  const db = await getDb();
  if (!db) throw new Error("Banco de dados indisponível.");
  await db.insert(analysisFiles).values(input);
}

export async function markFileReferenceRemoved(fileId: string, ownerId: number) {
  const db = await getDb();
  if (!db) throw new Error("Banco de dados indisponível.");
  await db.update(analysisFiles).set(buildReferenceRemovalAudit()).where(and(eq(analysisFiles.id, fileId), eq(analysisFiles.ownerId, ownerId)));
}

export async function getNextDiagnosticVersion(projectId: string, ownerId: number) {
  const db = await getDb();
  if (!db) throw new Error("Banco de dados indisponível.");
  const existing = await db.select({ version: analysisDiagnostics.version }).from(analysisDiagnostics).where(and(eq(analysisDiagnostics.projectId, projectId), eq(analysisDiagnostics.ownerId, ownerId))).orderBy(desc(analysisDiagnostics.version)).limit(1);
  return (existing[0]?.version ?? 0) + 1;
}

export async function createAnalysisDiagnostic(input: typeof analysisDiagnostics.$inferInsert) {
  const db = await getDb();
  if (!db) throw new Error("Banco de dados indisponível.");
  await db.insert(analysisDiagnostics).values(input);
}

export async function getAnalysisDiagnosticForOwner(diagnosticId: string, ownerId: number) {
  const db = await getDb();
  if (!db) throw new Error("Banco de dados indisponível.");
  const [diagnostic] = await db.select().from(analysisDiagnostics).where(and(eq(analysisDiagnostics.id, diagnosticId), eq(analysisDiagnostics.ownerId, ownerId))).limit(1);
  return diagnostic;
}
