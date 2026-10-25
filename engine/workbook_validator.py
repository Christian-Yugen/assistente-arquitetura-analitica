"""Inspeção mínima de workbook para controles prévios à persistência."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from openpyxl import load_workbook

from engine.csv_workbook import CsvWorkbookError, inspect_csv
from engine.profiling.workbook import MAX_SHEETS, WorkbookValidationError


def inspect_workbook(path: Path, file_format: str = "xlsx") -> dict[str, int]:
    if file_format == "csv":
        try:
            return inspect_csv(path)
        except CsvWorkbookError as error:
            raise WorkbookValidationError(str(error)) from error
    if file_format != "xlsx":
        raise WorkbookValidationError("Formato de arquivo não suportado.")
    try:
        workbook = load_workbook(path, read_only=True, data_only=False, keep_links=False)
    except Exception as error:
        raise WorkbookValidationError("Arquivo XLSX inválido, criptografado ou não legível.") from error
    try:
        sheet_count = len(workbook.worksheets)
        if sheet_count == 0 or sheet_count > MAX_SHEETS:
            raise WorkbookValidationError(f"O workbook deve ter entre 1 e {MAX_SHEETS} abas.")
        return {"sheet_count": sheet_count}
    finally:
        workbook.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--format", choices=("xlsx", "csv"), default="xlsx")
    parser.add_argument("--error-output")
    args = parser.parse_args()
    try:
        print(json.dumps(inspect_workbook(Path(args.input), args.format)))
    except WorkbookValidationError:
        if args.error_output:
            failure_code = "inspection_csv_invalid" if args.format == "csv" else "inspection_workbook_invalid"
            Path(args.error_output).write_text(json.dumps({"failure_code": failure_code}), encoding="utf-8")
        raise SystemExit(1)
    except Exception:
        if args.error_output:
            Path(args.error_output).write_text(json.dumps({"failure_code": "inspection_process_failed"}), encoding="utf-8")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
