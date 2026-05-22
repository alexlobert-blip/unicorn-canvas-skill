# sharebird-unicorn-canvas

A Claude Code plugin that walks a PMM through Chris Hines's Unicorn Messaging Framework canvas — either filling in a blank canvas or pressure-testing an existing draft.

The skill is one page, five layers (brand line → pains → differentiation → outcomes → modules → power plays), three columns (one per pain). When it is filled in well, it functions as the single source of truth that aligns positioning, product marketing, sales enablement, and CS narrative around the same three pains and one brand line.

## What you get

Three modes, picked at skill open:

1. **Information** — learn the framework. Guided tour through the Cyera worked example, or open Q&A about any layer. Optional one-page reference card to share with teammates. No canvas built.
2. **Build a canvas** — synthesize a canvas from your evidence. Sub-option: blank canvas (fresh fill-in) or critique an existing draft. Per-layer readiness gate — if you lack evidence for a layer, the skill offers (a) `[VALIDATE]` + best hypothesis, (b) inline research mini-plan for that layer, or (c) skip. Auto-ingests transcripts and prep docs from your working folder; surfaces customer-voice quotes at each layer; produces a populated `.xlsx` at `~/Downloads/unicorn-canvas-{slug}.xlsx` plus a Markdown critique with strongest/weakest cells, three next actions, and a handoff to the Power Play Table.
3. **Plan research** — generate a structured research plan + interview question packs to gather the evidence you need BEFORE building. Output: a Markdown plan at `~/Downloads/unicorn-canvas-research-plan-{slug}.md` with per-layer readiness checklist, research plan table (Layer / Gap / Research type / Question stems / Evidence target / Timeline), and per-research-type question packs (Customer call / Analyst / Field expert / Sales / CS) formatted to drop into Sharebird's deep-dive prep doc.

The three modes cover the full PMM project lifecycle — learn the framework, plan the research, synthesize the canvas. A companion to deep-dive interview workflows: Mode C produces the question packs that feed deep-dives; Mode B consumes the transcripts that come out.

## Install

### Option A — download the latest release zip

```bash
curl -L -o sharebird-unicorn-canvas.zip \
  https://github.com/alexlobert-blip/unicorn-canvas-skill/releases/latest/download/sharebird-unicorn-canvas-v0.4.1.zip
unzip sharebird-unicorn-canvas.zip -d ~/sharebird-unicorn-canvas
```

(For a release-pinned URL or future versions, browse https://github.com/alexlobert-blip/unicorn-canvas-skill/releases and grab the `.zip` asset directly.)

Then add the skill through your Claude client — Claude.app: Customize → Skills → `+` → point at the unzipped `skills/sharebird-unicorn-canvas/` directory.

### Option B — clone the repo and symlink

For developers or if you want to track updates via `git pull`:

```bash
git clone https://github.com/alexlobert-blip/unicorn-canvas-skill.git
cd unicorn-canvas-skill

# Symlink into the Claude Code CLI skills directory:
make install

# Or build your own .zip for distribution:
make plugin
```

`make install` creates `~/.claude/skills/sharebird-unicorn-canvas` as a symlink to the cloned repo, so the skill is discoverable by Claude Code CLI sessions. For Claude.app, point Customize → Skills → `+` at the cloned `skills/sharebird-unicorn-canvas/` directory.

## Use

Once installed, start a Claude Code conversation and say one of:

- "Explain the Unicorn Messaging Framework canvas" → routes to **Mode A** (Information)
- "Help me build a messaging canvas for [company]" → routes to **Mode B** (Build)
- "Pressure-test my Unicorn canvas" → routes to **Mode B** with critique sub-option
- "What research should I run to build a messaging canvas?" → routes to **Mode C** (Plan)
- "I'm refreshing our messaging — can you help?" → routes to **Mode B** (default)

Claude will invoke the skill and confirm the mode if the opening prompt is ambiguous.

## What's inside

```
unicorn-canvas-skill/
├── .claude-plugin/plugin.json         # plugin manifest
├── README.md
├── LICENSE                            # MIT
├── CHANGELOG.md
├── Makefile                           # `make plugin` builds dist/sharebird-unicorn-canvas-v*.zip
└── skills/
    └── sharebird-unicorn-canvas/
        ├── SKILL.md                   # main instructions + workflow
        ├── references/
        │   └── rubric.md              # per-layer pressure-test questions
        ├── scripts/
        │   └── fill_canvas.py         # openpyxl helper — writes payload into a copy
        └── templates/
            ├── canvas-blank.xlsx      # bundled Sharebird template (3 tabs)
            └── canvas-worked-example.xlsx
```

## Requirements

- Python 3 with `openpyxl` (only used to write the populated XLSX). Install with `pip install openpyxl`.

## Scope

What's in:
- Blank-canvas and critique workflows for the Unicorn Messaging Framework canvas.
- Per-layer pressure-test rubric covering the brand line, three pains, differentiation, outcomes, modules, and power plays.
- XLSX output via bundled `templates/canvas-blank.xlsx` + `scripts/fill_canvas.py`.
- **Automatic ingestion of customer transcripts and prep docs as upstream input** (v0.3.0+). Drop your evidence files into the working folder and the skill auto-detects, ingests, and surfaces relevant quotes at each canvas layer. Supports `.md`, `.txt`, `.docx`, `.pdf` (macOS), and public Google Docs / Sheets URLs. Skill stays Socratic — quotes only, no auto-fill.

What's out (could land in future versions):
- HTML output (XLSX only).
- Per-industry rubric variants. The current rubric is industry-neutral with cybersecurity-flavored examples drawn from the Cyera worked example that originated the framework — substitute your own buyer / opponent / SKUs as you walk the layers.
- Power Play Table integration beyond the closing handoff line in the skill (a separate `sharebird-power-play-table` skill is planned).
- Auto-watching the working folder for files dropped mid-conversation.
- OAuth-gated Google Drive access (only public / shared-link Docs and Sheets supported today).
- Cross-platform PDF extraction. `scripts/extract_artifact_text.py` uses macOS-only `textutil` for PDFs — Linux/Windows users hitting a PDF should convert to `.docx` first or paste excerpts.

## License

MIT. See [LICENSE](LICENSE).

## Acknowledgements

Built on the Unicorn Messaging Framework by Chris Hines. The canvas and rubric are derived from his Sharebird playbook session.
