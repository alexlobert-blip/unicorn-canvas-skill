# Changelog

All notable changes to this plugin will be documented here.

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
