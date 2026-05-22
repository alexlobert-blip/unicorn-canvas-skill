# Changelog

All notable changes to this plugin will be documented here.

## [0.4.0] - 2026-05-21

### Added — three enterprise-grade modes

Top-level Step 1 is now a mode picker. Three modes match where the user actually is in their project:

- **Mode A — Information.** New. For PMMs (or teammates) who want to learn the framework before using it. Two sub-options: guided tour through the Cyera worked example, or open Q&A. Optional one-page reference card output for sharing with teammates.
- **Mode B — Build a canvas.** Today's flow, augmented. Sub-option asks blank-canvas vs. critique-an-existing-draft (the old top-level Critique mode is now folded in here). Per-layer **readiness gate** added before each layer in Step 4: confirms the user has the evidence to fill the layer; if not, user picks (a) hypothesis with `[VALIDATE]`, (b) generate a research mini-plan for that layer inline, or (c) skip. Output flow unchanged.
- **Mode C — Plan research.** New. For PMMs who want to use the canvas eventually but don't have the evidence yet. Walks per-layer inputs audit, generates a structured Markdown research plan saved to `~/Downloads/unicorn-canvas-research-plan-{slug}.md` with three sections: (1) per-layer readiness checklist, (2) research plan table (Layer / Gap / Research type / Question stems / Evidence target / Timeline), (3) per-research-type question packs (Customer call / Analyst / Field expert / Sales / CS). Question packs are formatted to drop directly into Sharebird's deep-dive prep doc — the skill becomes a companion to the deep-dive workflow.

### Added — per-layer Readiness criterion in the Inline Rubric

Each of the 6 rubric layers now has a fifth element alongside Job / Grounding question / Common mistake / Pressure-test questions: a **Readiness criterion** stating what evidence is required to fill the layer well. The Build-mode readiness gate (Step 4) checks against this criterion; the Plan-mode inputs audit (Step 3') maps directly to it.

### Changed

- **Step 1 — Mode Select** replaces the old top-level "blank vs critique" question. Critique is now a sub-option inside Build mode.
- **README.md** — Scope section rewritten to describe all three modes.
- **SKILL.md grew from 220 → 360 lines** (+64%). Significant. The lines earn their cost by tripling the skill's audience (learners + planners + builders, not just builders). Both reference benchmarks (`narrative-pressure-test` 147 LOC, `sharebird-launch-brief` 133 LOC) serve narrower use cases.

### Preserved (no behavior change)

- All 6 grounding questions (Brand line, Pains, Differentiation, Outcomes, Modules, Power plays).
- All 5 pressure-test questions per layer (30 total — the skill's teeth).
- All `[VALIDATE]` / `[BETA]` / `[ROADMAP]` / `[NEW MOTION]` markers.
- Trigger surface (frontmatter description) — same trigger phrases, same eager priority.
- v0.3.0's auto-ingestion in Step 3 (now part of Mode B).
- v0.2.2's "canvas is one source of truth" stance.
- Step 6 Output (XLSX + Markdown critique).
- Bundled Python scripts unchanged (`fill_canvas.py`, `ingest_inputs.py`, the 3 vendored extractors).

### Out of scope (could land in future versions)

- Branching tour in Mode A ("which layer do you want to dig into?").
- Cross-mode state persistence (start in Mode C, return weeks later, resume in Mode B with auto-loaded research plan).
- Project-management features in Mode C (assignees, Linear/Jira tickets, calendar timelines).
- Stakeholder mapping / sign-off workflows.
- Quarterly canvas refresh as a 4th mode.

## [0.3.0] - 2026-05-21

### Added
- **Automatic ingestion of customer transcripts / prep docs as upstream input** — the headline gap from v0.1–v0.2 that the user flagged as the difference between "useful" and "truly useful."
  - **Three vendored scripts from `sharebird-launch-brief`** (`extract_artifact_text.py`, `fetch_google_doc.py`, `fetch_google_sheet.py`) — stdlib-only, byte-identical copies. Handle `.md`, `.txt`, `.docx`, `.pdf`, plus public Google Doc / Sheet URLs.
  - **New `scripts/ingest_inputs.py`** — wrapper that auto-scans a working folder for likely transcript / prep-doc files, optionally takes additional `--path` / `--url` flags, runs the right extractor per source, and returns a single JSON payload with concatenated text + per-source metadata + warnings. Soft cap of 50,000 chars to keep context budget sane.
  - **New `scripts/smoke_ingest_inputs.py`** — fixture-based smoke test exercising the auto-scan + concatenation flow.
- **Per-layer quote pattern in SKILL.md Step 4.** At each layer's grounding question, if transcripts were ingested, the skill surfaces 2–3 relevant quotes ("Here's how your customers describe Pain 1: [quote]") before asking the user to craft the cell in their own words. Preserves the framework's "user does the thinking" principle — quotes only, no auto-fill.

### Changed
- **Step 3 (Inputs Check) rewritten** as a three-path flow: (A) auto-detect from the working folder, (B) ask user for explicit paths/URLs/excerpts if no working folder or nothing found, (C) hypothesis-driven if no inputs at all.
- **README.md** — moved "Automatic ingestion of customer transcripts or prep docs as upstream input" from "What's out of v1" to "What's in." Added macOS-only PDF caveat under Requirements.

### Known limitations
- **PDF extraction is macOS-only** (uses `textutil`). Linux/Windows users hitting a PDF source see a warning and the source's text comes back empty. Workaround: convert PDF to `.docx` or paste excerpts directly. This is a deliberate regression in cross-platform parity to keep the install footprint stdlib-only; a future patch could swap in `pypdf` if user demand arrives.
- **No auto-watching** — one-time scan at Step 3; if the user drops new files mid-conversation, they re-trigger ingestion explicitly.
- **No OAuth Google Drive** — only public / shared-link Google Docs and Sheets are supported.

## [0.2.2] - 2026-05-21

### Fixed
- **Step 2 — Context Check no longer asks "where does this live downstream" and no longer "calibrates language register" to the surface.** This contradicted the framework: per Chris Hines's playbook, the canvas is ONE source of truth that must be surface-durable. The brand-line pressure-test already enforces this — *"Works at a sales kickoff AND on a website hero? If only one, too narrow."* — and adding a "tune the canvas for exec vs. sales vs. web" instruction in Step 2 was incompatible with that pressure-test. Step 2 now asks just two things: company + product, and target ICP.

### Changed
- **Surface translation moved to Output Step 6 as a recommended-next-action.** Translating the canvas into specific deliverables (exec memo, sales kickoff deck, website hero rewrite, board update) is downstream copywriting work — not changes to the canvas itself. One of the three recommended next actions at Output time is now always a surface-translation prompt.

## [0.2.1] - 2026-05-21

### Changed
- **Subtraction pass on `SKILL.md`** — 286 lines → 205 lines (~28% reduction). Removed pure documentation (`What stays out of v1`, `Optional bundled files`, `Two non-negotiables` preamble, `Everything you need is inline` paragraph), compressed Overview from 6 paragraphs to 2, collapsed Path A/B output instructions into one paragraph, tightened each rubric layer's prose (grounding questions kept verbatim, pressure-test wording compressed without cutting questions). All 6 grounding questions, all 5 pressure-tests per layer, and all `[VALIDATE]` / `[BETA]` / `[ROADMAP]` / `[NEW MOTION]` markers preserved.

### Fixed
- **Portability:** Dropped cross-reference to `narrative-pressure-test` skill in the Overview. The instruction *"match `narrative-pressure-test`'s tone"* would silently fail for users who install this plugin standalone without the rest of Sharebird's skill ecosystem. Tone is now self-described: *"direct, specific, never preachy. Push back, never block."*
- **Portability:** Replaced vague *"Sharebird playbook page"* reference in the handoff line with concrete pointer to the bundled `templates/canvas-blank.xlsx` and the GitHub release URL.
- **Portability:** Annotated `output_path` resolution to explicitly call out cross-platform support (macOS / Linux / Windows via `Path.expanduser()`).

### Not changed
- Behavior — the skill produces the same flow, same XLSX, same Markdown critique. Pure density + portability pass.
- Trigger surface — frontmatter `description` is untouched.
- `references/rubric.md`, `scripts/fill_canvas.py`, `templates/canvas-blank.xlsx` — all unchanged.

## [0.2.0] - 2026-05-21

### Added
- **Step 2 — Context Check.** Before Inputs Check, ask company/product, target ICP, and downstream surface (exec memo / sales enablement / website hero / board update). Catches the "what does this product do?" gap that Cowork was previously filling with generic intake. Enforces the one-ICP-per-canvas rule explicitly.
- **Per-layer grounding questions** — every layer in the rubric now opens with a grounding question that prevents the most expensive cascade failure at that layer:
  - **Brand line:** *"Do you have one today? Paste it — we'll critique or replace deliberately."* (Prevents accidentally contradicting an existing line and creating alignment debt.)
  - **Pains:** Restate the ICP from Step 2 + enforce single-ICP rule. (Prevents the most common cascade failure — pains drift across ICPs and the whole canvas collapses.)
  - **Differentiation:** *"For each pain, who/what are you positioning against?"* (Prevents differentiation written without a named opponent — which is decoration.)
  - **Outcomes:** *"Real customer outcome with a named reference, or a hypothesis?"* Hypothesis-only outcomes get `[VALIDATE]` markers and become customer-interview tasks in the recommended-next-actions list. (Prevents un-validated outcomes leaking into sales decks as facts.)
  - **Modules:** *"List only what's GA today. `[BETA]` / `[ROADMAP]` items can appear but can't anchor power plays."* (Prevents power plays anchored on roadmap items that fail when sales demos them 60 days later.)
  - **Power plays:** *"What GTM motion does your team currently run for this? `[NEW MOTION]` items get a pilot quarter."* (Prevents inventing plays the team has zero reps for.)
- **Critique-branch-specific intake.** Three additional questions (who wrote the draft, what's the goal of critique, what evidence backed each cell) layered on top of Steps 2 + 3.

### Changed
- **Inputs Check (now Step 3)** now actively requests the 2 highest-leverage artifacts be pasted — not just listed. Includes a default leverage ranking (transcripts > win-loss > outcome data > competitive research > existing messaging).
- Layer walkthrough renumbered to Step 4; Critique Branch to Step 5; Output to Step 6.
- **Output step now auto-prioritizes validation tasks.** If Step 3 flagged thin inputs, OR any Outcome was marked `[VALIDATE]`, OR any Module was marked `[BETA]` / `[ROADMAP]`, the first recommended-next-action is the matching validation task.
- Overview now states the two non-negotiables (one ICP, real evidence or explicit hypothesis-only acceptance) up front.

## [0.1.1] - 2026-05-21

### Changed
- **Inlined the full rubric into `SKILL.md`** so Cowork and other sandboxed environments — which only load `SKILL.md` into the prompt, not the surrounding `references/`, `scripts/`, `templates/` folders — have everything they need to run the skill correctly. `references/rubric.md` is retained as a duplicate for environments that prefer file references.
- **Added Step 2 "Inputs Check"** between mode selection and the brand-line layer. The skill now asks what evidence (customer transcripts, win/loss research, competitive analysis, outcome data) the user has before walking the canvas, so output can be anchored in real customer language and the "hypothesis-only" caveat fires automatically when inputs are thin.
- **Output step is now environment-aware.** Documents both Path A (run the bundled `fill_canvas.py` script when accessible) and Path B (write a fresh openpyxl script inline using the documented cell map when the bundled script isn't reachable).
- **Cell map is now inline** in `SKILL.md` so Path B can be executed from memory.

### Fixed
- Bug where sandboxed runs (Cowork) reported "the skill's bundled rubric, XLSX template, and fill script aren't available" — the skill now degrades gracefully because all critical content is inline.

## [0.1.0] - 2026-05-21

### Added
- Initial release.
- `sharebird-unicorn-canvas` skill with hybrid blank-canvas / critique workflow.
- Per-layer pressure-test rubric (`references/rubric.md`) — brand line, pains, differentiation, outcomes, modules, power plays.
- `scripts/fill_canvas.py` writes user answers into a copy of the bundled XLSX.
- Bundled XLSX templates (blank and worked example).
- MIT license, plugin manifest at `.claude-plugin/plugin.json`.
