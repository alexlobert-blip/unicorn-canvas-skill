#!/usr/bin/env python3
"""Smoke test for skills/sharebird-unicorn-canvas/scripts/ingest_inputs.py.

Creates a temp dir with 3 fixture files (markdown transcripts + a txt
prep-doc), runs ingest_inputs.py against it, and asserts the output is
shaped as expected.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INGEST_SCRIPT = REPO_ROOT / "skills" / "sharebird-unicorn-canvas" / "scripts" / "ingest_inputs.py"

FIXTURES = {
    "customer-interview-1.md": """\
# Customer interview — Acme Co, Mar 14

Sarah, VP Marketing: "Honestly, the biggest pain is that we spend half
the quarter rebuilding the same enablement deck every launch. We don't
have a source of truth."

Sarah: "We picked Cyera over Wiz because their team understood our
auditor's workflow — Wiz felt more engineer-led."
""",
    "win-loss-prep.md": """\
# Win/loss prep — Q1 closed/won deals

Top three reasons cited in interviews:
1. "Cut investigation time from 14 days to 90 minutes" — Northwell pilot.
2. Procurement frictionless — single contract covered all 3 modules.
3. References from peer CISOs in regulated industries.
""",
    "competitive-research.txt": """\
Wiz: engineer-first messaging, fast time-to-value, less mature in
regulated industries.

Varonis: governance-heavy, slow to deploy, expensive.

Splunk: status quo for most enterprises — Excel-and-email workflow plus
SIEM rules. Pain point: investigation latency.
""",
}


def main() -> int:
    if not INGEST_SCRIPT.exists():
        print(f"Missing ingest script: {INGEST_SCRIPT}", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        for name, content in FIXTURES.items():
            (tmppath / name).write_text(content, encoding="utf-8")
        # Also drop a noise file that should be skipped.
        (tmppath / ".DS_Store").write_text("noise", encoding="utf-8")
        (tmppath / "Unicorn-Canvas-template.xlsx").write_text(
            "binary noise (xlsx not in candidate extensions)", encoding="utf-8"
        )

        result = subprocess.run(
            [
                sys.executable,
                str(INGEST_SCRIPT),
                "--working-folder",
                str(tmppath),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            print("ingest_inputs.py exited non-zero", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            return result.returncode

        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            print(f"ingest_inputs.py emitted invalid JSON: {exc}", file=sys.stderr)
            print(result.stdout[:500], file=sys.stderr)
            return 1

        # Assertions
        sources = payload.get("sources", [])
        if len(sources) != 3:
            print(
                f"Expected 3 sources (md/md/txt), got {len(sources)}: "
                f"{[s['path'] for s in sources]}",
                file=sys.stderr,
            )
            return 1
        names = {Path(s["path"]).name for s in sources}
        if not {"customer-interview-1.md", "win-loss-prep.md", "competitive-research.txt"} <= names:
            print(f"Wrong file set: {names}", file=sys.stderr)
            return 1

        text = payload.get("concatenated_text", "")
        for expected in (
            "rebuilding the same enablement deck",
            "Northwell pilot",
            "engineer-first messaging",
        ):
            if expected not in text:
                print(f"Expected snippet missing from concatenated text: {expected!r}", file=sys.stderr)
                return 1

        if payload.get("total_chars", 0) < 500:
            print(f"Suspiciously small total_chars: {payload.get('total_chars')}", file=sys.stderr)
            return 1

        print(
            f"OK — ingested {len(sources)} sources, "
            f"{payload['total_chars']} chars, "
            f"{len(payload.get('warnings', []))} warnings"
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
