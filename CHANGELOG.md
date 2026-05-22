# Changelog

All notable changes to this plugin will be documented here.

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
