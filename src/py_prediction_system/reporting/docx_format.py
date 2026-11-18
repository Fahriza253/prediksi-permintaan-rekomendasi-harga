"""Normalisasi gaya DOCX: Times New Roman 12 pt, teks hitam, spasi 1,15."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

FONT_NAME = "Times New Roman"
FONT_SIZE = Pt(12)
TEXT_COLOR = RGBColor(0, 0, 0)
LINE_SPACING = 1.15


def _apply_run_style(run) -> None:
    run.font.name = FONT_NAME
    run.font.size = FONT_SIZE
    run.font.color.rgb = TEXT_COLOR
    element = run._element
    r_pr = element.get_or_add_rPr()
    fonts = r_pr.get_or_add_rFonts()
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        fonts.set(qn(attr), FONT_NAME)


def _apply_paragraph_style(paragraph) -> None:
    for run in paragraph.runs:
        _apply_run_style(run)
    fmt = paragraph.paragraph_format
    fmt.line_spacing = LINE_SPACING


def normalize_docx_styles(docx_path: Path) -> None:
    doc = Document(docx_path)
    for paragraph in doc.paragraphs:
        _apply_paragraph_style(paragraph)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    _apply_paragraph_style(paragraph)
    for section in doc.sections:
        for paragraph in section.header.paragraphs:
            _apply_paragraph_style(paragraph)
        for paragraph in section.footer.paragraphs:
            _apply_paragraph_style(paragraph)
    doc.save(docx_path)