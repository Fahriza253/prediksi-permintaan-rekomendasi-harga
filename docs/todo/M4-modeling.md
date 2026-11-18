# M4 — Modeling (`modeling`)

**Status modul:** `pending`  
**Depends on:** M2  
**Scratch:** `.scratch/modeling/`  
**ADR:** [0001-time-based-train-test-split](../adr/0001-time-based-train-test-split.md)

## Task

- [ ] Pisah latih/uji berbasis waktu (cutoff dari M2)
- [ ] **Baseline:** Linear Regression pada fitur terpilih
- [ ] **Lanjutan:** ≥1 model (mis. Random Forest atau Gradient Boosting)
- [ ] Pipeline fit (sklearn) terpisah baseline vs lanjutan
- [ ] Serialisasi model (`outputs/models/`)
- [ ] Konfigurasi random seed / reproduksi dicatat

## Keluaran

- [ ] Daftar fitur final yang masuk model
- [ ] Artefak siap untuk M5

**Catatan / blocker:**