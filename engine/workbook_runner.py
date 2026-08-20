"""Entrada CLI do motor: recebe metadados e XLSX locais e devolve diagnóstico JSON canônico."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from engine.contracts.execution_profile import load_authorized_draft_profile
from engine.pipeline.quality_diagnosis import DiagnosisMetadata, execute_quality_diagnosis
from engine.profiling.workbook import profile_workbook


def run(input_path: Path, metadata_path: Path) -> dict[str, object]:
    raw_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    business_questions = tuple(raw_metadata.pop("business_questions", []))
    metadata = DiagnosisMetadata(
        **raw_metadata,
        business_questions=business_questions,
        execution_profile=load_authorized_draft_profile(),
    )
    columns = profile_workbook(input_path)
    return execute_quality_diagnosis(columns, metadata=metadata)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    diagnosis = run(Path(args.input), Path(args.metadata))
    Path(args.output).write_text(json.dumps(diagnosis, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
