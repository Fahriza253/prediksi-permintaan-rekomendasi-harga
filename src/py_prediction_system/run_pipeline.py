"""Jalankan pipeline M2–M6 berurutan (profil data di M1 terpisah jika perlu)."""

from __future__ import annotations

import sys
from collections.abc import Callable

from py_prediction_system.eda.explore import run_eda
from py_prediction_system.evaluation.metrics import run_evaluation
from py_prediction_system.models.train import run_training
from py_prediction_system.preprocessing.pipeline import run_preprocessing
from py_prediction_system.simulation.price_grid import run_simulation


def _step(name: str, fn: Callable[[], object]) -> None:
    print(f"=== {name} ===")
    fn()
    print()


def main() -> int:
    steps: list[tuple[str, Callable[[], object]]] = [
        ("M2 Preprocessing", lambda: run_preprocessing()[0]),
        ("M3 EDA", lambda: run_eda()[0]),
        ("M4 Modeling", lambda: run_training()[2]),
        ("M5 Evaluation", run_evaluation),
        ("M6 Price simulation", run_simulation),
    ]
    for name, fn in steps:
        try:
            _step(name, fn)
        except Exception as exc:
            print(f"Gagal pada {name}: {exc}", file=sys.stderr)
            return 1
    print("Pipeline selesai. Lihat outputs/ dan report/LAPORAN_UTS.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())