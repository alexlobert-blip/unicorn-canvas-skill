#!/usr/bin/env python3
"""Ingest customer transcripts / prep docs as upstream input for the canvas.

Auto-detects likely transcript and prep-doc files in a working folder,
optionally accepts additional explicit file paths and Google Doc / Sheet
URLs, then runs the right extractor per source and returns a structured
JSON payload that the skill brings into conversation context.

Usage::

    python3 ingest_inputs.py \\
        [--working-folder /path/to/dir] \\
        [--path file1.md --path file2.docx] \\
        [--url https://docs.google.com/document/d/...] \\
        [--max-chars 50000]

Outputs JSON to stdout with shape::

    {
      "sources": [
        {"path": "...", "source_type": "markdown", "chars": 18432, "preview": "..."},
        ...
      ],
      "concatenated_text": "<all sources joined with ## headers>",
      "warnings": ["..."],
      "total_chars": 47128,
      "truncated": false
    }

Cell-level extraction is left to the LLM consuming this output — Claude
reads the concatenated text from context and pulls per-layer relevant
quotes natively. This script does file→text only, no classification.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

# Local sibling-script imports (callable APIs from the vendored scripts).
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from extract_artifact_text import extract_text  # noqa: E402
from fetch_google_doc import fetch_google_doc  # noqa: E402
from fetch_google_sheet import fetch_google_sheet  # noqa: E402


CANDIDATE_EXTENSIONS = {".md", ".txt", ".docx", ".pdf", ".vtt"}
SKIP_PATTERNS = (".DS_Store", ".gitignore", ".gitkeep")
DEFAULT_MAX_CHARS = 50_000
PREVIEW_LEN = 240


def _is_likely_input(path: pathlib.Path) -> bool:
    if path.name in SKIP_PATTERNS or path.name.startswith("."):
        return False
    if path.suffix.lower() not in CANDIDATE_EXTENSIONS:
        return False
    return path.is_file()


def _scan_folder(folder: pathlib.Path) -> list[pathlib.Path]:
    if not folder.exists() or not folder.is_dir():
        return []
    return sorted(p for p in folder.iterdir() if _is_likely_input(p))


def _looks_like_google_doc(url: str) -> bool:
    return "docs.google.com/document" in url


def _looks_like_google_sheet(url: str) -> bool:
    return "docs.google.com/spreadsheets" in url


def _preview(text: str) -> str:
    snippet = " ".join(text.split())[:PREVIEW_LEN]
    return snippet + "…" if len(snippet) == PREVIEW_LEN else snippet


def _extract_one(source: str | pathlib.Path) -> dict[str, Any]:
    """Return {label, source_type, text, warnings} for one source."""
    if isinstance(source, pathlib.Path):
        result = extract_text(str(source))
        return {
            "path": str(source),
            "source_type": result.get("source_type", "unknown"),
            "text": result.get("text", ""),
            "warnings": list(result.get("warnings", [])),
        }
    # String — treat as URL
    if _looks_like_google_doc(source):
        result = fetch_google_doc(source)
        return {
            "path": source,
            "source_type": "google_doc",
            "text": result.get("text", ""),
            "warnings": list(result.get("warnings", [])),
        }
    if _looks_like_google_sheet(source):
        result = fetch_google_sheet(source)
        return {
            "path": source,
            "source_type": "google_sheet",
            "text": result.get("text", ""),
            "warnings": list(result.get("warnings", [])),
        }
    return {
        "path": source,
        "source_type": "unknown",
        "text": "",
        "warnings": [f"Unrecognized URL or path: {source}"],
    }


def ingest(
    working_folder: str | None = None,
    paths: list[str] | None = None,
    urls: list[str] | None = None,
    max_chars: int = DEFAULT_MAX_CHARS,
) -> dict[str, Any]:
    sources: list[dict[str, Any]] = []
    warnings: list[str] = []

    # 1. Auto-detect from working folder
    if working_folder:
        folder_path = pathlib.Path(working_folder).expanduser()
        for candidate in _scan_folder(folder_path):
            sources.append(_extract_one(candidate))

    # 2. Explicit paths
    for raw_path in paths or []:
        candidate = pathlib.Path(raw_path).expanduser()
        if not candidate.exists():
            warnings.append(f"Path does not exist: {raw_path}")
            continue
        sources.append(_extract_one(candidate))

    # 3. URLs
    for url in urls or []:
        sources.append(_extract_one(url))

    # Build concatenated text + per-source summaries
    chunks: list[str] = []
    summaries: list[dict[str, Any]] = []
    total = 0
    truncated = False
    for entry in sources:
        text = entry["text"]
        warnings.extend(entry.get("warnings", []))
        if not text:
            summaries.append(
                {
                    "path": entry["path"],
                    "source_type": entry["source_type"],
                    "chars": 0,
                    "preview": "",
                }
            )
            continue
        remaining = max_chars - total
        if remaining <= 0:
            truncated = True
            warnings.append(
                f"Skipped {entry['path']} — exceeded max_chars ({max_chars})."
            )
            continue
        if len(text) > remaining:
            text = text[:remaining]
            truncated = True
            warnings.append(
                f"Truncated {entry['path']} to {remaining} chars — exceeded max_chars."
            )
        header = f"## Source: {entry['path']} ({entry['source_type']})"
        chunks.append(f"{header}\n\n{text}")
        total += len(text)
        summaries.append(
            {
                "path": entry["path"],
                "source_type": entry["source_type"],
                "chars": len(text),
                "preview": _preview(text),
            }
        )

    return {
        "sources": summaries,
        "concatenated_text": "\n\n---\n\n".join(chunks),
        "warnings": warnings,
        "total_chars": total,
        "truncated": truncated,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--working-folder",
        help="Directory to scan for likely transcript/prep-doc files.",
    )
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        help="Explicit file path to ingest (repeatable).",
    )
    parser.add_argument(
        "--url",
        action="append",
        default=[],
        help="Google Doc or Google Sheet URL to ingest (repeatable).",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=DEFAULT_MAX_CHARS,
        help=f"Soft cap on total ingested text (default: {DEFAULT_MAX_CHARS}).",
    )
    args = parser.parse_args()

    if not args.working_folder and not args.path and not args.url:
        sys.stderr.write(
            "Nothing to ingest — pass --working-folder, --path, or --url.\n"
        )
        return 2

    result = ingest(
        working_folder=args.working_folder,
        paths=args.path,
        urls=args.url,
        max_chars=args.max_chars,
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
