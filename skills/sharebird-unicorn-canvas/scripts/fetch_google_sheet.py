#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
import urllib.parse
import urllib.request


def normalize_google_sheet_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if "docs.google.com" not in parsed.netloc or "/spreadsheets/d/" not in parsed.path:
        raise ValueError("Expected a Google Sheets URL")

    path_parts = parsed.path.strip("/").split("/")
    try:
        doc_id = path_parts[path_parts.index("d") + 1]
    except (ValueError, IndexError) as exc:
        raise ValueError("Could not determine Google Sheet document id") from exc

    query = urllib.parse.parse_qs(parsed.query)
    fragment = urllib.parse.parse_qs(parsed.fragment)
    gid = (query.get("gid") or fragment.get("gid") or [None])[0]

    export_query = {"format": "csv"}
    if gid:
        export_query["gid"] = gid

    return urllib.parse.urlunparse(
        (
            parsed.scheme or "https",
            "docs.google.com",
            f"/spreadsheets/d/{doc_id}/export",
            "",
            urllib.parse.urlencode(export_query),
            "",
        )
    )


def flatten_csv_text(sheet_name: str, csv_text: str) -> str:
    reader = csv.reader(io.StringIO(csv_text))
    rows = list(reader)
    if not rows:
        return f"Sheet: {sheet_name}\n<empty>"

    rendered = [f"Sheet: {sheet_name}"]
    for row in rows:
        if any(cell.strip() for cell in row):
            rendered.append(" | ".join(cell.strip() for cell in row))
    return "\n".join(rendered)


def _infer_sheet_name(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    if query.get("sheet"):
        return query["sheet"][0]
    return "Google Sheet"


def fetch_google_sheet(url: str) -> dict[str, str]:
    normalized_url = normalize_google_sheet_url(url)
    request = urllib.request.Request(
        normalized_url,
        headers={"User-Agent": "sharebird-launch-brief-skill/1.0"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        charset = response.headers.get_content_charset("utf-8")
        csv_text = response.read().decode(charset)
    sheet_name = _infer_sheet_name(url)
    return {
        "source_url": url,
        "export_url": normalized_url,
        "sheet_name": sheet_name,
        "text": flatten_csv_text(sheet_name, csv_text),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fetch a public Google Sheet as text.")
    parser.add_argument("url", help="Public or shared-export Google Sheets URL")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    args = parser.parse_args(argv)

    result = fetch_google_sheet(args.url)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["text"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
