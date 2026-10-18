"""Build readable, self-contained PDF submission records with macOS CUPS.

This uses only the Python standard library and the local PostScript-to-PDF filter.
"""

from __future__ import annotations

import re
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
WIDTH, HEIGHT = 612, 792
LEFT, TOP, BOTTOM = 54, 744, 54


def escape(text: str) -> str:
    replacements = str.maketrans({"–": "-", "—": "-", "’": "'", "“": '"', "”": '"', "±": "+/-", "×": "x"})
    text = text.translate(replacements).encode("ascii", "replace").decode("ascii")
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def normalize(line: str) -> tuple[str, str]:
    line = line.rstrip()
    if line.startswith("# "):
        return "title", line[2:]
    if line.startswith("## "):
        return "heading", line[3:]
    if line.startswith("### "):
        return "subheading", line[4:]
    line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
    line = re.sub(r"`([^`]*)`", r"\1", line)
    line = line.replace("|", " | ")
    line = re.sub(r"\s+", " ", line).strip()
    if line and set(line.replace("|", "").replace(" ", "")) <= {"-", ":"}:
        return "skip", ""
    if line.startswith("- "):
        return "bullet", line[2:]
    return "body", line


def source_lines(markdown: Path, appendix: Path | None = None) -> list[tuple[str, str]]:
    records = [normalize(line) for line in markdown.read_text(encoding="utf-8").splitlines()]
    if appendix:
        records += [("heading", "Edition A unchanged transcription")]
        records += [("body", line.strip()) for line in appendix.read_text(encoding="utf-8").splitlines() if line.strip()]
    return records


def create_pdf(records: list[tuple[str, str]], target: Path) -> None:
    pages: list[list[str]] = [[]]
    y = TOP

    def new_page() -> None:
        nonlocal y
        pages.append([])
        y = TOP

    def emit(font: str, size: float, text: str, indent: int = 0) -> None:
        nonlocal y
        if y < BOTTOM + size + 5:
            new_page()
        font_name = "F2" if font == "Helvetica-Bold" else "F1"
        pages[-1].append(f"BT /{font_name} {size} Tf {LEFT + indent} {y:.1f} Td ({escape(text)}) Tj ET")
        y -= size + 4

    for kind, raw in records:
        if kind == "skip":
            continue
        if not raw:
            y -= 6
            continue
        if kind == "title":
            for line in textwrap.wrap(raw, width=54):
                emit("Helvetica-Bold", 16, line)
            y -= 6
        elif kind == "heading":
            if y < BOTTOM + 36:
                new_page()
            for line in textwrap.wrap(raw, width=72):
                emit("Helvetica-Bold", 12, line)
            y -= 2
        elif kind == "subheading":
            for line in textwrap.wrap(raw, width=76):
                emit("Helvetica-Bold", 10, line)
        else:
            indent = 12 if kind == "bullet" else 0
            width = 83 if kind == "body" else 79
            wrapped = textwrap.wrap(raw, width=width, break_long_words=False, break_on_hyphens=False) or [""]
            for index, line in enumerate(wrapped):
                prefix = "- " if kind == "bullet" and index == 0 else ""
                emit("Helvetica", 9.5, prefix + line, indent)
    for number, content in enumerate(pages, start=1):
        content.append(f"BT /F1 8 Tf 54 32 Td (Page {number}) Tj ET")

    # Minimal PDF 1.4 writer using only built-in Helvetica fonts.
    objects: list[bytes] = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    page_object_numbers = [6 + index * 2 for index in range(len(pages))]
    kids = " ".join(f"{number} 0 R" for number in page_object_numbers)
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>".encode())
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
    for index, commands in enumerate(pages):
        content = ("\n".join(commands) + "\n").encode("ascii")
        content_object = 5 + index * 2
        page_object = content_object + 1
        objects.append(f"<< /Length {len(content)} >>\nstream\n".encode() + content + b"endstream")
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {WIDTH} {HEIGHT}] "
            f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {content_object} 0 R >>".encode()
        )
    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, body in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{number} 0 obj\n".encode())
        output.extend(body)
        output.extend(b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode())
    output.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    target.write_bytes(output)


def build(markdown_name: str, pdf_name: str, appendix: str | None = None) -> None:
    create_pdf(source_lines(DOCS / markdown_name, DOCS / appendix if appendix else None), DOCS / pdf_name)


def main() -> None:
    build("decision-memo.md", "Decision-Memo.pdf")
    build("validation-and-ai-use.md", "Validation-and-AI-Use.pdf")
    build("research-evolution.md", "Research-Evolution.pdf", "edition-a-transcription.txt")


if __name__ == "__main__":
    main()
