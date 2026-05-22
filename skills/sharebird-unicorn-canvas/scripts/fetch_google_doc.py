#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request


def normalize_google_doc_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if "docs.google.com" not in parsed.netloc or "/document/d/" not in parsed.path:
        raise ValueError("Expected a Google Docs URL")

    path_parts = parsed.path.strip("/").split("/")
    try:
        doc_id = path_parts[path_parts.index("d") + 1]
    except (ValueError, IndexError) as exc:
        raise ValueError("Could not determine Google Doc document id") from exc

    return urllib.parse.urlunparse(
        (
            parsed.scheme or "https",
            "docs.google.com",
            f"/document/d/{doc_id}/export",
            "",
            urllib.parse.urlencode({"format": "txt"}),
            "",
        )
    )


def clean_google_doc_text(text: str) -> str:
    lines = text.replace("\ufeff", "").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    collapsed = []
    last_blank = False
    for line in lines:
        stripped = line.rstrip()
        blank = not stripped
        if blank and last_blank:
            continue
        collapsed.append(stripped)
        last_blank = blank
    return "\n".join(collapsed).strip()


def fetch_google_doc(url: str) -> dict[str, str]:
    normalized_url = normalize_google_doc_url(url)
    request = urllib.request.Request(
        normalized_url,
        headers={"User-Agent": "sharebird-launch-brief-skill/1.0"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        charset = response.headers.get_content_charset("utf-8")
        text = response.read().decode(charset, errors="replace")
    return {
        "source_url": url,
        "export_url": normalized_url,
        "text": clean_google_doc_text(text),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fetch a public Google Doc as text.")
    parser.add_argument("url", help="Public Google Docs URL")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    args = parser.parse_args(argv)

    result = fetch_google_doc(args.url)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["text"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
