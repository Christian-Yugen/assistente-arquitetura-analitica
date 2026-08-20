import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const intakePath = resolve(
  import.meta.dirname,
  "../artifacts/intake/QLT-NULL-001-reconstruction-intake.json",
);
const gatePath = resolve(import.meta.dirname, "../docs/gates/QLT_NULL_RECONSTRUCTION_001.md");
const baselinePath = resolve(
  import.meta.dirname,
  "../artifacts/baselines/qlt-null-001-v0.1.0-reconstructed.1-baseline.json",
);
const baselineManifestPath = resolve(
  import.meta.dirname,
  "../artifacts/baselines/qlt-null-001-v0.1.0-reconstructed.1-baseline.manifest.json",
);

describe("QLT-NULL-001 reconstruction lineage", () => {
  it("records the lost canonical source, Chris's authorization, a new reconstruction version, baseline and execution block", () => {
    const intake = JSON.parse(readFileSync(intakePath, "utf8")) as {
      candidate_version: string;
      source_lineage: {
        canonical_artifact_status: string;
        reconstruction_authorization: { authorized_by: string; does_not_authorize: string[] };
      };
      reconstruction_constraints: string[];
      required_before_implementation: string[];
      gate_id: string;
    };
    const gate = readFileSync(gatePath, "utf8");
    const baseline = readFileSync(baselinePath);
    const baselineManifest = JSON.parse(readFileSync(baselineManifestPath, "utf8")) as {
      rule_version: string;
      baseline_path: string;
      sha256: string;
      status: string;
    };

    expect(intake.source_lineage.canonical_artifact_status).toBe("lost_by_user_declaration");
    expect(intake.source_lineage.reconstruction_authorization.authorized_by).toBe("Chris");
    expect(intake.candidate_version).toBe("0.1.0-reconstructed.1");
    expect(intake.reconstruction_constraints.join(" ")).toContain("baseline");
    expect(intake.required_before_implementation).toContain("reconstruction-baseline");
    expect(intake.source_lineage.reconstruction_authorization.does_not_authorize).toContain(
      "execution before a reconstruction gate is approved",
    );
    expect(intake.gate_id).toBe("QLT-NULL-RECONSTRUCTION-001");
    expect(gate).toContain("implementação validada e execução autorizada somente no perfil draft");
    expect(gate).toContain("Chris aprovou a continuidade");
    expect(gate).toContain("produção bloqueada");
    expect(gate).toContain("não pode alegar recuperação");
    expect(gate).toContain("Decisão final de reconstrução");
    expect(gate).toContain("36 testes Python aprovados");
    expect(gate).toContain("2 de 95");
    expect(gate).toContain("não autoriza produção");
    expect(baselineManifest.rule_version).toBe("0.1.0-reconstructed.1");
    expect(baselineManifest.baseline_path).toBe(
      "artifacts/baselines/qlt-null-001-v0.1.0-reconstructed.1-baseline.json",
    );
    expect(baselineManifest.sha256).toBe(createHash("sha256").update(baseline).digest("hex"));
    expect(baselineManifest.status).toBe("approved_for_mvp_draft_execution");
  });
});
