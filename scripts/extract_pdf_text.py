"""Extract project PDF sources to plain text for deterministic agent reads."""

from __future__ import annotations

import argparse
from pathlib import Path

from pypdf import PdfReader


def extract_pdf(source: Path, destination: Path) -> tuple[int, int]:
    reader = PdfReader(source)
    pages: list[str] = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"\n\n===== PAGE {page_number} =====\n\n{text.strip()}\n")

    destination.parent.mkdir(parents=True, exist_ok=True)
    content = "".join(pages)
    destination.write_text(content, encoding="utf-8")
    return len(reader.pages), len(content)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root", type=Path)
    parser.add_argument("output_root", type=Path)
    args = parser.parse_args()

    pdfs = sorted(args.source_root.rglob("*.pdf"))
    for source in pdfs:
        relative = source.relative_to(args.source_root).with_suffix(".txt")
        destination = args.output_root / relative
        pages, characters = extract_pdf(source, destination)
        print(f"{relative.as_posix()}: {pages} pages, {characters} characters")


if __name__ == "__main__":
    main()
