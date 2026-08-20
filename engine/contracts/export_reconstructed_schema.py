"""Exporta o schema reconstruído como artefato JSON rastreável do repositório."""

from __future__ import annotations

import json
from pathlib import Path

from engine.contracts.reconstructed_schema import build_reconstructed_schema


OUTPUT = Path(__file__).resolve().parents[2] / "artifacts/contracts/PM-MVP-PBI-CON-001/diagnosis.schema.json"


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(build_reconstructed_schema(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
