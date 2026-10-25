import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const collector = readFileSync(resolve(process.cwd(), "client/public/__manus__/debug-collector.js"), "utf8");

describe("debug collector privacy", () => {
  it("does not record request bodies, response bodies, request headers, or query strings", () => {
    expect(collector).toContain("bodyCaptured: false");
    expect(collector).toContain("headersCaptured: false");
    expect(collector).toContain("function safeRequestPath(url)");
    expect(collector).not.toContain("body: init.body ? sanitizeValue");
    expect(collector).not.toContain("requestBody = body ? sanitizeValue");
    expect(collector).not.toContain("clonedResponse");
    expect(collector).not.toContain("xhr.responseText");
  });
});
