import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (relativePath: string) => fs.readFileSync(path.join(root, relativePath), "utf8");

describe("MDL-FACTNOGRAIN-019 preparation governance", () => {
  it("keeps implementation and production blocked pending specific policy approval", () => {
    const intake = read("artifacts/intake/MDL-FACTNOGRAIN-019.json");
    const policy = read("docs/rules/MDL_FACTNOGRAIN_019_POLICY_PROPOSAL_001.md");
    const specification = read("docs/rules/MDL_FACTNOGRAIN_019_LOGICAL_SPEC_PROPOSAL_001.md");

    expect(intake).toContain('"execution_blocked": true');
    expect(intake).toContain('"implementation_authorized": false');
    expect(policy).toContain("Proposta A");
    expect(policy).toContain("não é implementação");
    expect(specification).toContain("não executável");
    expect(specification).toContain("não deduz nem escolhe granularidade");
  });
});
