import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { protectedProcedure, publicProcedure, router } from "./_core/trpc";
import { TRPCError } from "@trpc/server";
import { randomUUID } from "node:crypto";
import { z } from "zod";
import * as db from "./db";
import { ANSWER_DECISIONS, answerDecisionFromStoredValue, questionIdsFromDiagnostic } from "./diagnosticActions";
import { buildWorkbookMetadata, executeWorkbookEngine, inspectWorkbookBeforePersistence, sanitizeSensitiveText, UploadValidationError, validateWorkbookUpload } from "./analysisPipeline";
import { containsUnsafeDiagnosticContent } from "./privacy";
import { storagePut } from "./storage";

export const appRouter = router({
    // if you need to use socket.io, read and register route in server/_core/index.ts, all api should start with '/api/' so that the gateway can route correctly
  system: systemRouter,
  auth: router({
    me: publicProcedure.query(opts => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return {
        success: true,
      } as const;
    }),
  }),
  analysis: router({
    listProjects: protectedProcedure.query(({ ctx }) => db.listAnalysisProjectsForOwner(ctx.user.id)),
    getDiagnostic: protectedProcedure.input(z.object({ diagnosticId: z.string().uuid() })).query(async ({ ctx, input }) => {
      const diagnostic = await db.getAnalysisDiagnosticForOwner(input.diagnosticId, ctx.user.id);
      if (!diagnostic) throw new TRPCError({ code: "NOT_FOUND", message: "Diagnóstico não encontrado." });
      return diagnostic;
    }),
    getActionState: protectedProcedure.input(z.object({ diagnosticId: z.string().uuid() }).strict()).query(async ({ ctx, input }) => {
      const diagnostic = await db.getAnalysisDiagnosticForOwner(input.diagnosticId, ctx.user.id);
      if (!diagnostic) throw new TRPCError({ code: "NOT_FOUND", message: "Diagnóstico não encontrado." });
      const allowedQuestionIds = new Set(questionIdsFromDiagnostic(diagnostic.payload));
      const answers = await db.listAnalysisAnswersForDiagnostic(diagnostic.id, ctx.user.id);
      return {
        answers: answers.flatMap(answer => {
          const decision = answerDecisionFromStoredValue(answer.answer);
          return decision && allowedQuestionIds.has(answer.questionId) ? [{ questionId: answer.questionId, decision }] : [];
        }),
      };
    }),
    answerQuestion: protectedProcedure.input(z.object({
      diagnosticId: z.string().uuid(),
      questionId: z.string().min(1).max(36),
      decision: z.enum(ANSWER_DECISIONS),
    }).strict()).mutation(async ({ ctx, input }) => {
      const diagnostic = await db.getAnalysisDiagnosticForOwner(input.diagnosticId, ctx.user.id);
      if (!diagnostic) throw new TRPCError({ code: "NOT_FOUND", message: "Diagnóstico não encontrado." });
      if (!questionIdsFromDiagnostic(diagnostic.payload).includes(input.questionId)) {
        throw new TRPCError({ code: "BAD_REQUEST", message: "Pergunta de validação inválida para este diagnóstico." });
      }
      await db.upsertAnalysisAnswer({
        id: randomUUID(), projectId: diagnostic.projectId, ownerId: ctx.user.id, sourceDiagnosticId: diagnostic.id,
        questionId: input.questionId, answer: { decision: input.decision },
      });
      return { questionId: input.questionId, decision: input.decision };
    }),
    analyzeWorkbook: protectedProcedure.input(z.object({
      projectName: z.string().trim().min(1).max(160),
      objective: z.string().trim().min(1).max(500).default("Analisar a estrutura da planilha para modelagem dimensional."),
      fileName: z.string().min(1).max(255),
      mimeType: z.string().max(160),
      dataBase64: z.string().min(4).max(36_000_000),
    })).mutation(async ({ ctx, input }) => {
      let workbook;
      try {
        workbook = validateWorkbookUpload(input);
        await inspectWorkbookBeforePersistence(workbook);
      } catch (error) {
        throw new TRPCError({ code: "BAD_REQUEST", message: error instanceof UploadValidationError ? error.message : "Upload inválido." });
      }
      const projectId = randomUUID();
      const fileId = randomUUID();
      const diagnosticId = randomUUID();
      try {
        await db.createAnalysisProject({ id: projectId, ownerId: ctx.user.id, name: sanitizeSensitiveText(input.projectName), domain: "generic" });
        await db.updateAnalysisProjectStatus(projectId, ctx.user.id, "uploading");
        const stored = await storagePut(`analysis/${ctx.user.id}/${projectId}/${fileId}.${workbook.extension}`, workbook.buffer, workbook.mimeType);
        await db.createAnalysisFile({
          id: fileId, projectId, ownerId: ctx.user.id, originalName: workbook.originalName, storageKey: stored.key,
          sha256: workbook.sha256, mimeType: workbook.mimeType, sizeBytes: workbook.buffer.length,
          sheetCount: 0, analyzableSheetCount: 0, retentionStatus: "private_active",
        });
        await db.updateAnalysisProjectStatus(projectId, ctx.user.id, "analyzing");
        const version = await db.getNextDiagnosticVersion(projectId, ctx.user.id);
        const diagnosis = await executeWorkbookEngine(workbook, buildWorkbookMetadata({
          analysisId: diagnosticId, projectId, ownerNumericId: ctx.user.id, projectName: input.projectName, objective: input.objective, fileId, workbook,
        }));
        if (containsUnsafeDiagnosticContent(diagnosis)) {
          throw new Error("O diagnóstico contém dados sensíveis detectáveis.");
        }
        const execution = diagnosis.execution as { engine_version: string; ruleset_version: string };
        const analysis = diagnosis.analysis as { status: "completed_with_warnings" | "failed" | "draft" };
        const file = diagnosis.file as { sheet_count: number; analyzable_sheet_count: number };
        await db.createAnalysisDiagnostic({
          id: diagnosticId, projectId, ownerId: ctx.user.id, fileId, version, status: analysis.status === "failed" ? "failed" : "completed_with_warnings",
          contractVersion: "1.0.0-reconstructed.1", engineVersion: execution.engine_version, rulesetVersion: execution.ruleset_version, payload: diagnosis,
        });
        await db.markFileReferenceRemoved(fileId, ctx.user.id);
        await db.updateAnalysisProjectStatus(projectId, ctx.user.id, analysis.status === "failed" ? "failed" : "completed");
        return { projectId, diagnosticId, version };
      } catch (error) {
        await db.updateAnalysisProjectStatus(projectId, ctx.user.id, "failed").catch(() => undefined);
        throw new TRPCError({ code: "INTERNAL_SERVER_ERROR", message: "Não foi possível concluir a análise." });
      }
    }),
  }),
});

export type AppRouter = typeof appRouter;
