import { describe, expect, it } from "vitest";
import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";

describe("analysis router authorization", () => {
  it("requires a signed-in user before listing or starting an analysis", async () => {
    const caller = appRouter.createCaller({ user: null, req: {} as TrpcContext["req"], res: {} as TrpcContext["res"] });
    await expect(caller.analysis.listProjects()).rejects.toMatchObject({ code: "UNAUTHORIZED" });
    await expect(caller.analysis.analyzeWorkbook({ projectName: "Projeto", objective: "Objetivo", fileName: "arquivo.xlsx", mimeType: "application/octet-stream", dataBase64: "UEsDBA==" })).rejects.toMatchObject({ code: "UNAUTHORIZED" });
  });
});
