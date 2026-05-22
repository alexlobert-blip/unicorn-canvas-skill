---
name: sharebird-unicorn-canvas
description: Walks a PMM through Chris Hines's Unicorn Messaging Framework canvas end-to-end — either filling in a blank canvas or pressure-testing an existing draft. Produces a populated XLSX plus a Markdown critique. Use whenever the user is working on positioning, refreshing messaging, building a launch narrative, defining customer pains, or aligning a company on one brand line. Trigger eagerly on phrases like "messaging framework", "positioning canvas", "unicorn messaging", "pressure-test my messaging", "I'm refreshing our messaging", "three pains", "company alignment around messaging", "brand line", "power play" (in a positioning context), or anytime a PMM is laddering from brand line → pains → solutions → GTM motion.
---

# Sharebird Unicorn Canvas

## Overview

Use this skill to walk a PMM through Chris Hines's Unicorn Messaging Framework canvas end-to-end. The canvas is one page, five layers (brand line → pains → differentiation → outcomes → modules → power plays), three columns (one per pain). When it is filled in well it functions as the single source of truth that aligns positioning, product marketing, sales enablement, and CS narrative around the same three pains and one brand line.

The skill is medium-rigor: push back on weak answers ("this differentiation reads as a capability, not a customer value — try again?") but never block the user from progressing. Match the tone of `narrative-pressure-test` — direct, specific, never preachy.

Output is always two artifacts: a populated XLSX (a copy of the bundled blank template with the user's answers written into the **Worked example** tab) plus a short Markdown critique summary in the conversation.

## Workflow Choice

At skill open, ask the user which path they are on, then commit to that branch:

> Two paths — (a) **blank canvas**, walk through fresh; (b) you have a draft, **critique it**. Which one?

- **blank-canvas** — fresh fill-in, layer-by-layer.
- **critique** — user pastes/uploads their draft (HTML, XLSX text, markdown, or just prose). Skill parses into the 5-layer × 3-pain structure, then walks each cell with the same rubric — no filling in, just critique + suggested rewrites.

Both branches converge on the same Output step at the end.

## Blank-Canvas Branch

Walk top-to-bottom. Do not skip layers. At each layer, load the matching section of [references/rubric.md](references/rubric.md) before responding, and use its pressure-test questions to push back on weak answers.

1. **Brand line.** One sentence: who is the company in the customer's world? Do not proceed until the line is customer-facing (not capability-facing) and short enough to repeat from memory. Rubric section: `Brand line`.

2. **Three pains.** Mutually exclusive. Each one a sentence the customer would actually say out loud, not an internal department name. Pressure-test hard for MECE-ness — if two pains overlap, ask which is dominant and force a split or a merge. The first pain is the dominant pain. Rubric section: `Pains`.

3. **Differentiation row (one per pain).** Pressure-test: capability vs. customer value. "We have AI" is a capability. "Catches data exfiltration in minutes instead of weeks" is a customer value. Rubric section: `Differentiation`.

4. **Customer outcome row (one per pain).** Numeric, customer-facing, has a real reference. "Faster" is not an outcome — "cut investigation time from 14 days to 90 minutes at Acme Bank" is. Rubric section: `Outcomes`.

5. **Platform modules (three per pain).** Three product modules or capabilities that ladder up to that pain. SKU-shaped, not marketing-shaped. Rubric section: `Modules`.

6. **Power play (one per pain).** One-sentence GTM motion summary. This is the handoff target for the future `sharebird-power-play-table` skill — capture it cleanly. Rubric section: `Power plays`.

## Critique Branch

1. Ask the user to paste or upload the draft. Accept HTML, XLSX text exports, raw markdown, or prose.
2. Parse into the 5-layer × 3-pain structure. If something is missing, say so explicitly rather than fabricating a guess.
3. Walk each populated cell against the matching rubric section in [references/rubric.md](references/rubric.md). Call out specifically what is strong and what is weak. Suggest concrete rewrites — do not just say "this is generic".
4. If the user wants to revise, loop with them on the weakest 2–3 cells before moving to Output.

## Output

Once the canvas is complete (both branches converge here):

1. Collect the user's answers into the JSON payload shape expected by [scripts/fill_canvas.py](scripts/fill_canvas.py):
   ```json
   {
     "brand_line": "…",
     "pains": [
       {"eyebrow": "PAIN 1 · DOMINANT", "title": "…"},
       {"eyebrow": "PAIN 2", "title": "…"},
       {"eyebrow": "PAIN 3", "title": "…"}
     ],
     "differentiation": ["…", "…", "…"],
     "outcomes": ["…", "…", "…"],
     "modules": [["…", "…", "…"], ["…", "…", "…"], ["…", "…", "…"]],
     "power_plays": ["…", "…", "…"],
     "output_path": "~/Downloads/unicorn-canvas-{company-slug}.xlsx"
   }
   ```
2. Run `python3 scripts/fill_canvas.py --input <json-file>` (or pipe the JSON on stdin). The script copies `templates/canvas-blank.xlsx` and writes the user's answers into the `Worked example` tab using the exact cell addresses encoded in the script.
3. Generate the Markdown critique summary directly in the conversation, in this shape:
   - **Strongest two cells.** Name them and say why.
   - **Weakest two cells.** Name them and recommend a concrete rewrite.
   - **Three recommended next actions.** Concrete, testable — e.g., "interview three accounts on Pain 2 to confirm wording reflects how they actually describe it".
   - **Handoff teaser.** One line.
4. Tell the user where the XLSX landed: `~/Downloads/unicorn-canvas-{company-slug}.xlsx`.

## Handoff

Closing line of the conversation:

> The three Power Play rows are ready to operationalize — each one expands into a row in the Power Play Table. A future `sharebird-power-play-table` skill will pick this up; until then, the XLSX template is at the Sharebird playbook page (linked from the GitHub release notes).

## Files

- `templates/canvas-blank.xlsx` — the source template. Three tabs (Read me, Worked example, Blank template). Copy verbatim, do not modify in place. The script writes into a copy.
- `templates/canvas-worked-example.xlsx` — same file with the Cyera worked example. Reference only — show the user what "good" looks like if asked.
- `references/rubric.md` — per-layer pressure-test rubric. Load the matching section before responding at each layer.
- `scripts/fill_canvas.py` — openpyxl helper that writes a populated XLSX. Only dependency: `openpyxl`.

## What stays out of v1

- HTML output (XLSX only).
- Automatic ingestion of transcripts or prep docs (could become a v2 mode).
- Per-industry rubric variants — v1 is industry-neutral with cybersecurity examples drawn from the Hines worked example.
- Power Play Table integration beyond the closing handoff line.
