"""Exporta exemplos determinísticos usados pelo gate de reconstrução do contrato."""

from __future__ import annotations

import json
from pathlib import Path

from engine.contracts.examples import build_complete_example, build_invalid_example, build_minimal_example


OUTPUT = Path(__file__).resolve().parents[2] / "artifacts/contracts/PM-MVP-PBI-CON-001/examples"


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    examples = {
        "minimal.valid.json": build_minimal_example(),
        "complete.valid.json": build_complete_example(),
        "invalid.unknown-root.json": build_invalid_example(),
    }
    for filename, payload in examples.items():
        (OUTPUT / filename).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
