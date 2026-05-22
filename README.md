# sharebird-unicorn-canvas

A Claude Code plugin that walks a PMM through Chris Hines's Unicorn Messaging Framework canvas — either filling in a blank canvas or pressure-testing an existing draft.

The skill is one page, five layers (brand line → pains → differentiation → outcomes → modules → power plays), three columns (one per pain). When it is filled in well, it functions as the single source of truth that aligns positioning, product marketing, sales enablement, and CS narrative around the same three pains and one brand line.

## What you get

- A hybrid workflow — the skill asks at the start whether you are starting from a blank canvas or critiquing an existing draft.
- Layer-by-layer pressure-test using a medium-rigor rubric (push back on weak answers, never block).
- A populated `.xlsx` saved to `~/Downloads/unicorn-canvas-{slug}.xlsx` once the canvas is done.
- A Markdown critique in the conversation: strongest cells, weakest cells, three recommended next actions, handoff to the Power Play Table.

## Install

### Option A — install from a Claude Code marketplace

```
/plugin marketplace add sharebird/unicorn-canvas-skill
/plugin install sharebird-unicorn-canvas@unicorn-canvas-skill
```

### Option B — install from a local clone (for testing)

```
git clone https://github.com/sharebird/unicorn-canvas-skill.git
/plugin marketplace add /absolute/path/to/unicorn-canvas-skill
/plugin install sharebird-unicorn-canvas@unicorn-canvas-skill
```

### Option C — drop the skill into `~/.claude/skills/`

If you just want the skill (not the full plugin), symlink or copy the skill folder:

```
ln -s "$(pwd)/skills/sharebird-unicorn-canvas" ~/.claude/skills/sharebird-unicorn-canvas
```

## Use

Once installed, start a Claude Code conversation and say one of:

- "I'm refreshing our messaging — can you help?"
- "Pressure-test my Unicorn canvas"
- "Walk me through the Unicorn Messaging Framework"
- "Help me get to one brand line + three pains"

Claude will invoke the skill and ask whether you want to start from a blank canvas or critique an existing draft.

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

## Scope (v1)

What's in:
- Blank-canvas and critique workflows for the Unicorn Messaging Framework canvas.
- Per-layer pressure-test rubric covering the brand line, three pains, differentiation, outcomes, modules, and power plays.
- XLSX output via bundled `templates/canvas-blank.xlsx` + `scripts/fill_canvas.py`.

What's out of v1 (could land in future versions):
- HTML output (XLSX only).
- Automatic ingestion of customer transcripts or prep docs as upstream input.
- Per-industry rubric variants. v1 is industry-neutral with cybersecurity-flavored examples drawn from the Cyera worked example that originated the framework — substitute your own buyer / opponent / SKUs as you walk the layers.
- Power Play Table integration beyond the closing handoff line in the skill (a separate `sharebird-power-play-table` skill is planned).

## License

MIT. See [LICENSE](LICENSE).

## Acknowledgements

Built on the Unicorn Messaging Framework by Chris Hines. The canvas and rubric are derived from his Sharebird playbook session.
