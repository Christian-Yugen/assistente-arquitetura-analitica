"""Inspeção mínima de workbook para controles prévios à persistência."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from openpyxl import load_workbook


MAX_SHEETS = 10


class WorkbookValidationError(ValueError):
    """Erro seguro para validação estrutural prévia à persistência."""


def inspect_workbook(path: Path) -> dict[str, int]:
    try:
        workbook = load_workbook(path, read_only=True, data_only=False, keep_links=False)
    except Exception as error:
        raise WorkbookValidationError("Arquivo XLSX inválido, criptografado ou não legível.") from error
    sheet_count = len(workbook.worksheets)
    if sheet_count == 0 or sheet_count > MAX_SHEETS:
        raise WorkbookValidationError(f"O workbook deve ter entre 1 e {MAX_SHEETS} abas.")
    return {"sheet_count": sheet_count}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(inspect_workbook(Path(args.input))))
        return 0
    except WorkbookValidationError as error:
        print(json.dumps({"error": "workbook_validation_error", "message": str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
