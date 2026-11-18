"""Ekspor LAPORAN_UTS.md ke Word dan estimasi jumlah halaman (M7)."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

from py_prediction_system.config import REPORT_DIR
from py_prediction_system.reporting.docx_format import normalize_docx_styles

WORDS_PER_PAGE = 380.0
FIGURE_PAGE_COST = 0.45
MAX_PAGES = 10

SOURCE_MD = REPORT_DIR / "LAPORAN_UTS.md"
OUTPUT_DOCX = REPORT_DIR / "LAPORAN_UTS.docx"
ESTIMATE_TXT = REPORT_DIR / "page_count_estimate.txt"


def _strip_markdown_for_count(text: str) -> str:
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"[#*|>\-]", " ", text)
    return text


def estimate_pages(md_path: Path) -> float:
    raw = md_path.read_text(encoding="utf-8")
    words = len(_strip_markdown_for_count(raw).split())
    figures = len(re.findall(r"!\[", raw))
    return words / WORDS_PER_PAGE + figures * FIGURE_PAGE_COST


def export_docx(source: Path | None = None, output: Path | None = None) -> Path:
    src = source or SOURCE_MD
    out = output or OUTPUT_DOCX
    if not src.is_file():
        raise FileNotFoundError(f"Naskah tidak ada: {src}")

    repo_root = src.resolve().parents[1]
    resource_path = f"{repo_root}{os.pathsep}{src.parent}"

    cmd = [
        "pandoc",
        str(src),
        "-o",
        str(out),
        "--resource-path",
        resource_path,
    ]
    subprocess.run(cmd, check=True)
    normalize_docx_styles(out)

    pages = estimate_pages(src)
    note = (
        f"Estimasi halaman (heuristik): {pages:.1f}\n"
        f"Batas wajib: {MAX_PAGES} halaman\n"
        f"Sumber: {src.name}\n"
        f"Output: {out.name}\n"
        f"Status: {'OK (estimasi ≤ batas)' if pages <= MAX_PAGES else 'PERINGATAN: estimasi melebihi batas — potong teks atau verifikasi di Word'}\n"
        "Format: Times New Roman 12 pt, warna hitam, spasi 1,15 (diterapkan saat ekspor).\n"
        "Verifikasi final: buka .docx di Word dan hitung halaman.\n"
    )
    ESTIMATE_TXT.write_text(note, encoding="utf-8")
    return out


def main() -> int:
    try:
        out = export_docx()
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1
    except subprocess.CalledProcessError:
        print("pandoc gagal. Pastikan pandoc terpasang.", file=sys.stderr)
        return 1

    estimate = ESTIMATE_TXT.read_text(encoding="utf-8")
    print(f"Wrote {out}")
    print(estimate, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())