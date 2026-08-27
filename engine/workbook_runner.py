"""Entrada CLI do motor: recebe metadados e XLSX locais e devolve diagnóstico JSON canônico."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from engine.csv_workbook import CsvWorkbookError, convert_csv_to_workbook
from engine.contracts.execution_profile import load_authorized_draft_profile
from engine.pipeline.quality_diagnosis import DiagnosisMetadata, execute_quality_diagnosis
from engine.profiling.workbook import profile_workbook_with_relationship_pairs


SAFE_ENGINE_FAILURE_CODES = {
    "WorkbookValidationError": "engine_workbook_invalid",
    "ValueError": "engine_value_error",
    "TypeError": "engine_type_error",
    "KeyError": "engine_key_error",
    "AssertionError": "engine_assertion_error",
}


def safe_engine_failure_code(error: Exception) -> str:
    """Classifica a exceção sem reter nem imprimir a mensagem potencialmente sensível."""

    for error_class in type(error).__mro__:
        safe_code = SAFE_ENGINE_FAILURE_CODES.get(error_class.__name__)
        if safe_code:
            return safe_code
    return "engine_unexpected_error"


def run(input_path: Path, metadata_path: Path, file_format: str = "xlsx") -> dict[str, object]:
    raw_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    business_questions = tuple(raw_metadata.pop("business_questions", []))
    metadata = DiagnosisMetadata(
        **raw_metadata,
        business_questions=business_questions,
        execution_profile=load_authorized_draft_profile(),
    )
    profiling_path = input_path
    if file_format == "csv":
        profiling_path = input_path.with_name("normalized.csv.xlsx")
        try:
            convert_csv_to_workbook(input_path, profiling_path)
        except CsvWorkbookError as error:
            raise ValueError("O CSV não pôde ser normalizado para análise.") from error
    elif file_format != "xlsx":
        raise ValueError("Formato de arquivo não suportado.")
    workbook_profile = profile_workbook_with_relationship_pairs(profiling_path)
    return execute_quality_diagnosis(
        workbook_profile.columns,
        metadata=metadata,
        relationship_pair_signals=workbook_profile.relationship_pair_signals,
        composite_relationship_pair_signals=workbook_profile.composite_relationship_pair_signals,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--error-output")
    parser.add_argument("--format", choices=("xlsx", "csv"), default="xlsx")
    args = parser.parse_args()
    try:
        diagnosis = run(Path(args.input), Path(args.metadata), args.format)
        Path(args.output).write_text(json.dumps(diagnosis, ensure_ascii=False), encoding="utf-8")
    except Exception as error:
        if args.error_output:
            Path(args.error_output).write_text(
                json.dumps({"failure_code": safe_engine_failure_code(error)}),
                encoding="utf-8",
            )
        raise SystemExit(1)


if __name__ == "__main__":
    main()
