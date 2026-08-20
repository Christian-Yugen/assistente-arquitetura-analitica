import { describe, expect, it } from "vitest";
import { buildReferenceRemovalAudit } from "./analysisRetention";

describe("buildReferenceRemovalAudit", () => {
  it("removes the private storage reference while retaining only auditable retention metadata", () => {
    const removedAt = new Date("2026-08-20T00:00:00.000Z");
    expect(buildReferenceRemovalAudit(removedAt)).toEqual({
      storageKey: null,
      retentionStatus: "reference_removed",
      referenceRemovedAt: removedAt,
    });
  });
});
