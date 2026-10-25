import { describe, expect, it, vi } from "vitest";
import { deleteAndVerifyObject } from "./physicalRetention";
import type { ObjectStore } from "./physicalRetention";

describe("physical retention additional security tests", () => {
  const key = "analysis/77/project/file.xlsx";

  it("deletes an existing object and verifies its absence", async () => {
    let exists = true;

    const store: ObjectStore = {
      deleteObject: vi.fn(async () => {
        exists = false;
      }),
      objectExists: vi.fn(async () => exists),
    };

    const result = await deleteAndVerifyObject(store, key);

    expect(result).toEqual({
      status: "deleted",
      referenceMayBeRemoved: true,
    });
    expect(store.deleteObject).toHaveBeenCalledWith(key);
    expect(store.objectExists).toHaveBeenCalledTimes(2);
    expect(exists).toBe(false);
  });

  it("preserves the reference when deletion fails", async () => {
    const store: ObjectStore = {
      deleteObject: vi.fn(async () => {
        throw new Error("provider unavailable");
      }),
      objectExists: vi.fn(async () => true),
    };

    const result = await deleteAndVerifyObject(store, key);

    expect(result).toEqual({
      status: "retry_required",
      referenceMayBeRemoved: false,
      reason: "provider_error",
    });
  });

  it("preserves the reference when absence cannot be verified", async () => {
    const store: ObjectStore = {
      deleteObject: vi.fn(async () => undefined),
      objectExists: vi.fn(async () => true),
    };

    const result = await deleteAndVerifyObject(store, key);

    expect(result).toEqual({
      status: "retry_required",
      referenceMayBeRemoved: false,
      reason: "unverified",
    });
    expect(store.objectExists).toHaveBeenCalledTimes(2);
  });

  it("allows removal when the object is already absent", async () => {
    const store: ObjectStore = {
      deleteObject: vi.fn(async () => undefined),
      objectExists: vi.fn(async () => false),
    };

    const result = await deleteAndVerifyObject(store, key);

    expect(result).toEqual({
      status: "already_absent",
      referenceMayBeRemoved: true,
    });
    expect(store.deleteObject).not.toHaveBeenCalled();
  });

  it("rejects unsafe storage keys without calling the provider", async () => {
    const store: ObjectStore = {
      deleteObject: vi.fn(async () => undefined),
      objectExists: vi.fn(async () => true),
    };

    for (const unsafeKey of ["", "/private/file.xlsx", "../file.xlsx", "a\\b.xlsx"]) {
      const result = await deleteAndVerifyObject(store, unsafeKey);
      expect(result.referenceMayBeRemoved).toBe(false);
      expect(result.status).toBe("retry_required");
    }

    expect(store.deleteObject).not.toHaveBeenCalled();
    expect(store.objectExists).not.toHaveBeenCalled();
  });
});