import { index, int, json, mysqlEnum, mysqlTable, text, timestamp, uniqueIndex, varchar } from "drizzle-orm/mysql-core";

/**
 * Core user table backing auth flow.
 * Extend this file with additional tables as your product grows.
 * Columns use camelCase to match both database fields and generated types.
 */
export const users = mysqlTable("users", {
  /**
   * Surrogate primary key. Auto-incremented numeric value managed by the database.
   * Use this for relations between tables.
   */
  id: int("id").autoincrement().primaryKey(),
  /** Manus OAuth identifier (openId) returned from the OAuth callback. Unique per user. */
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

export const analysisProjects = mysqlTable(
  "analysis_projects",
  {
    id: varchar("id", { length: 36 }).primaryKey(),
    ownerId: int("ownerId").notNull().references(() => users.id, { onDelete: "cascade" }),
    name: varchar("name", { length: 160 }).notNull(),
    domain: varchar("domain", { length: 80 }).default("generic").notNull(),
    status: mysqlEnum("status", ["draft", "uploading", "analyzing", "completed", "failed"]).default("draft").notNull(),
    createdAt: timestamp("createdAt").defaultNow().notNull(),
    updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
    completedAt: timestamp("completedAt"),
  },
  table => ({
    ownerStatusIdx: index("analysis_projects_owner_status_idx").on(table.ownerId, table.status),
  }),
);

export const analysisFiles = mysqlTable(
  "analysis_files",
  {
    id: varchar("id", { length: 36 }).primaryKey(),
    projectId: varchar("projectId", { length: 36 }).notNull().references(() => analysisProjects.id, { onDelete: "cascade" }),
    ownerId: int("ownerId").notNull().references(() => users.id, { onDelete: "cascade" }),
    originalName: varchar("originalName", { length: 255 }).notNull(),
    storageKey: text("storageKey"),
    sha256: varchar("sha256", { length: 64 }).notNull(),
    mimeType: varchar("mimeType", { length: 160 }).notNull(),
    sizeBytes: int("sizeBytes").notNull(),
    sheetCount: int("sheetCount").notNull(),
    analyzableSheetCount: int("analyzableSheetCount").notNull(),
    retentionStatus: mysqlEnum("retentionStatus", ["private_active", "reference_removed", "rejected"]).default("private_active").notNull(),
    referenceRemovedAt: timestamp("referenceRemovedAt"),
    createdAt: timestamp("createdAt").defaultNow().notNull(),
  },
  table => ({
    projectOwnerIdx: index("analysis_files_project_owner_idx").on(table.projectId, table.ownerId),
    ownerRetentionIdx: index("analysis_files_owner_retention_idx").on(table.ownerId, table.retentionStatus),
  }),
);

export const analysisDiagnostics = mysqlTable(
  "analysis_diagnostics",
  {
    id: varchar("id", { length: 36 }).primaryKey(),
    projectId: varchar("projectId", { length: 36 }).notNull().references(() => analysisProjects.id, { onDelete: "cascade" }),
    ownerId: int("ownerId").notNull().references(() => users.id, { onDelete: "cascade" }),
    fileId: varchar("fileId", { length: 36 }).references(() => analysisFiles.id, { onDelete: "set null" }),
    version: int("version").notNull(),
    status: mysqlEnum("status", ["draft", "completed_with_warnings", "failed"]).notNull(),
    contractVersion: varchar("contractVersion", { length: 64 }).notNull(),
    engineVersion: varchar("engineVersion", { length: 64 }).notNull(),
    rulesetVersion: varchar("rulesetVersion", { length: 64 }).notNull(),
    payload: json("payload").notNull(),
    createdAt: timestamp("createdAt").defaultNow().notNull(),
  },
  table => ({
    projectOwnerVersionUnique: uniqueIndex("analysis_diagnostics_project_owner_version_uq").on(table.projectId, table.ownerId, table.version),
    ownerCreatedIdx: index("analysis_diagnostics_owner_created_idx").on(table.ownerId, table.createdAt),
  }),
);

export const analysisAnswers = mysqlTable(
  "analysis_answers",
  {
    id: varchar("id", { length: 36 }).primaryKey(),
    projectId: varchar("projectId", { length: 36 }).notNull().references(() => analysisProjects.id, { onDelete: "cascade" }),
    ownerId: int("ownerId").notNull().references(() => users.id, { onDelete: "cascade" }),
    sourceDiagnosticId: varchar("sourceDiagnosticId", { length: 36 }).notNull().references(() => analysisDiagnostics.id, { onDelete: "cascade" }),
    questionId: varchar("questionId", { length: 36 }).notNull(),
    answer: json("answer").notNull(),
    createdAt: timestamp("createdAt").defaultNow().notNull(),
  },
  table => ({
    sourceQuestionUnique: uniqueIndex("analysis_answers_source_question_uq").on(table.sourceDiagnosticId, table.questionId),
    ownerProjectIdx: index("analysis_answers_owner_project_idx").on(table.ownerId, table.projectId),
  }),
);

export type AnalysisProject = typeof analysisProjects.$inferSelect;
export type AnalysisFile = typeof analysisFiles.$inferSelect;
export type AnalysisDiagnostic = typeof analysisDiagnostics.$inferSelect;
export type AnalysisAnswer = typeof analysisAnswers.$inferSelect;
