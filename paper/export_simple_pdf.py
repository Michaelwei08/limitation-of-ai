"""Dependency-free Markdown-to-PDF exporter for paper drafts.

This is intentionally simple: it preserves headings, paragraphs, code blocks,
and tables well enough for review PDFs when Pandoc/LaTeX is unavailable.
"""

from __future__ import annotations

import argparse
import textwrap
from dataclasses import dataclass
from pathlib import Path


PAGE_WIDTH = 612
PAGE_HEIGHT = 792
MARGIN_X = 54
MARGIN_TOP = 54
MARGIN_BOTTOM = 54
TEXT_WIDTH = PAGE_WIDTH - (2 * MARGIN_X)


@dataclass(frozen=True)
class StyledLine:
    text: str
    font: str
    size: float
    leading: float
    gap_before: float = 0.0


def _strip_inline_markup(text: str) -> str:
    replacements = {
        "**": "",
        "__": "",
        "`": "",
        "![": "[",
    }
    cleaned = text
    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)
    return cleaned


def _wrap_text(text: str, width_chars: int) -> list[str]:
    if not text:
        return [""]
    return textwrap.wrap(
        text,
        width=max(20, width_chars),
        break_long_words=False,
        break_on_hyphens=False,
    ) or [""]


def markdown_to_lines(markdown: str) -> list[StyledLine]:
    lines: list[StyledLine] = []
    in_code = False

    for raw in markdown.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            in_code = not in_code
            lines.append(StyledLine("", "Courier", 8.0, 10.0, 4.0))
            continue

        if in_code:
            for wrapped in _wrap_text(line, 82):
                lines.append(StyledLine(wrapped, "Courier", 8.0, 10.0))
            continue

        if not line:
            if lines and lines[-1].text:
                lines.append(StyledLine("", "Helvetica", 10.0, 8.0, 2.0))
            continue

        if line.startswith("# "):
            text = _strip_inline_markup(line[2:].strip())
            for wrapped in _wrap_text(text, 48):
                lines.append(StyledLine(wrapped, "Helvetica-Bold", 18.0, 22.0, 8.0))
            continue

        if line.startswith("## "):
            text = _strip_inline_markup(line[3:].strip())
            for wrapped in _wrap_text(text, 62):
                lines.append(StyledLine(wrapped, "Helvetica-Bold", 14.0, 17.0, 8.0))
            continue

        if line.startswith("|"):
            for wrapped in _wrap_text(_strip_inline_markup(line), 100):
                lines.append(StyledLine(wrapped, "Courier", 7.0, 9.0))
            continue

        if line.startswith("- "):
            text = "- " + _strip_inline_markup(line[2:].strip())
            for index, wrapped in enumerate(_wrap_text(text, 88)):
                prefix = "" if index == 0 else "  "
                lines.append(StyledLine(prefix + wrapped, "Helvetica", 9.5, 12.0))
            continue

        text = _strip_inline_markup(line)
        for wrapped in _wrap_text(text, 92):
            lines.append(StyledLine(wrapped, "Helvetica", 9.5, 12.0))

    return lines


def _escape_pdf_text(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .encode("latin-1", errors="replace")
        .decode("latin-1")
    )


def _paginate(lines: list[StyledLine]) -> list[list[StyledLine]]:
    pages: list[list[StyledLine]] = []
    current: list[StyledLine] = []
    y = PAGE_HEIGHT - MARGIN_TOP

    for line in lines:
        needed = line.leading + line.gap_before
        if current and y - needed < MARGIN_BOTTOM:
            pages.append(current)
            current = []
            y = PAGE_HEIGHT - MARGIN_TOP
        current.append(line)
        y -= needed

    if current:
        pages.append(current)
    return pages


def _content_stream(page_lines: list[StyledLine], page_number: int) -> bytes:
    parts = ["BT"]
    y = PAGE_HEIGHT - MARGIN_TOP
    current_font = ""
    current_size = 0.0

    for line in page_lines:
        y -= line.gap_before
        if line.font != current_font or line.size != current_size:
            parts.append(f"/{_font_resource(line.font)} {line.size:.1f} Tf")
            current_font = line.font
            current_size = line.size
        if line.text:
            escaped = _escape_pdf_text(line.text)
            parts.append(f"{MARGIN_X:.1f} {y:.1f} Td ({escaped}) Tj")
            parts.append(f"{-MARGIN_X:.1f} {-line.leading:.1f} Td")
        else:
            parts.append(f"0 {-line.leading:.1f} Td")
        y -= line.leading

    parts.append("/F1 8 Tf")
    parts.append(f"{PAGE_WIDTH - 96:.1f} 28 Td (Page {page_number}) Tj")
    parts.append("ET")
    return ("\n".join(parts) + "\n").encode("latin-1", errors="replace")


def _font_resource(font: str) -> str:
    if font == "Helvetica-Bold":
        return "F2"
    if font == "Courier":
        return "F3"
    return "F1"


def write_pdf(lines: list[StyledLine], output_path: Path) -> None:
    pages = _paginate(lines)
    objects: list[bytes] = []

    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    page_refs = " ".join(f"{3 + i * 2} 0 R" for i in range(len(pages)))
    objects.append(f"<< /Type /Pages /Kids [{page_refs}] /Count {len(pages)} >>".encode("ascii"))

    for index, page_lines in enumerate(pages, start=1):
        page_obj_num = 3 + (index - 1) * 2
        content_obj_num = page_obj_num + 1
        resources = (
            "<< /Font << "
            "/F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> "
            "/F2 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >> "
            "/F3 << /Type /Font /Subtype /Type1 /BaseFont /Courier >> "
            ">> >>"
        )
        page = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
            f"/Resources {resources} /Contents {content_obj_num} 0 R >>"
        )
        stream = _content_stream(page_lines, index)
        content = b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"endstream"
        objects.append(page.encode("ascii"))
        objects.append(content)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as handle:
        handle.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]
        for obj_num, obj in enumerate(objects, start=1):
            offsets.append(handle.tell())
            handle.write(f"{obj_num} 0 obj\n".encode("ascii"))
            handle.write(obj)
            handle.write(b"\nendobj\n")
        xref = handle.tell()
        handle.write(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
        handle.write(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            handle.write(f"{offset:010d} 00000 n \n".encode("ascii"))
        trailer = f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
        handle.write(trailer.encode("ascii"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a Markdown draft to a simple PDF.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    markdown = args.input.read_text(encoding="utf-8")
    write_pdf(markdown_to_lines(markdown), args.output)


if __name__ == "__main__":
    main()
