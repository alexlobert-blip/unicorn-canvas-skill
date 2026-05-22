#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile


WORD_NAMESPACE = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def _normalize_text(text: str) -> str:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    collapsed = []
    last_blank = False
    for line in lines:
        blank = not line.strip()
        if blank and last_blank:
            continue
        collapsed.append(line)
        last_blank = blank
    return "\n".join(collapsed).strip()


def _read_text_file(path: pathlib.Path) -> str:
    for encoding in ("utf-8", "utf-16", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not decode text file: {path}")


def _extract_docx_text(path: pathlib.Path) -> str:
    with zipfile.ZipFile(path) as archive:
        xml_text = archive.read("word/document.xml")
    root = ET.fromstring(xml_text)
    paragraphs = []
    for paragraph in root.findall(".//w:p", WORD_NAMESPACE):
        fragments = [node.text or "" for node in paragraph.findall(".//w:t", WORD_NAMESPACE)]
        text = "".join(fragments).strip()
        if text:
            paragraphs.append(text)
    return "\n\n".join(paragraphs)


def _run_command(command: list[str]) -> str:
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return ""
    return completed.stdout.strip()


def _extract_pdf_text(path: pathlib.Path) -> str:
    commands = [
        ["/usr/bin/mdls", "-raw", "-name", "kMDItemTextContent", str(path)],
        ["/usr/bin/textutil", "-convert", "txt", "-stdout", str(path)],
    ]
    for command in commands:
        output = _run_command(command)
        if output and output != "(null)":
            cleaned = _normalize_text(output)
            if cleaned:
                return cleaned
    raise RuntimeError(
        "Could not extract text from PDF with the available system tools. "
        "Provide a text export or source document instead."
    )


def extract_text(path: str | pathlib.Path) -> dict[str, str]:
    target = pathlib.Path(path)
    suffix = target.suffix.lower()
    if suffix in {".md", ".markdown"}:
        source_type = "markdown"
        text = _read_text_file(target)
    elif suffix in {".txt", ".text"}:
        source_type = "text"
        text = _read_text_file(target)
    elif suffix == ".docx":
        source_type = "docx"
        text = _extract_docx_text(target)
    elif suffix == ".pdf":
        source_type = "pdf"
        text = _extract_pdf_text(target)
    else:
        raise ValueError(f"Unsupported artifact type: {suffix or 'no extension'}")

    return {
        "path": str(target),
        "source_type": source_type,
        "text": _normalize_text(text),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract text from launch artifacts.")
    parser.add_argument("path", help="Path to a supported artifact file")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    args = parser.parse_args(argv)

    result = extract_text(args.path)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["text"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
