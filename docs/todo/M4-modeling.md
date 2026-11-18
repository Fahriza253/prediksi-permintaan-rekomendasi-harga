# M4 — Modeling (`modeling`)

**Status modul:** `done`  
**Depends on:** M2  
**Scratch:** `.scratch/modeling/`  
**ADR:** [0001-time-based-train-test-split](../adr/0001-time-based-train-test-split.md)

## Task

- [x] Pisah latih/uji berbasis waktu (cutoff dari M2)
- [x] **Baseline:** Linear Regression pada fitur terpilih
- [x] **Lanjutan:** ≥1 model (mis. Random Forest atau Gradient Boosting)
- [x] Pipeline fit (sklearn) terpisah baseline vs lanjutan
- [x] Serialisasi model (`outputs/models/`)
- [x] Konfigurasi random seed / reproduksi dicatat

## Keluaran

- [x] Daftar fitur final yang masuk model
- [x] Artefak siap untuk M5

**Catatan / blocker:** `python -m py_prediction_system.models.train`. Manifest: `outputs/models/training_manifest.json`. Seed 42.