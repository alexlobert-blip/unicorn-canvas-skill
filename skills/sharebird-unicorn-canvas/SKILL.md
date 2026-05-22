---
name: sharebird-unicorn-canvas
description: Walks a PMM through Chris Hines's Unicorn Messaging Framework canvas end-to-end — either filling in a blank canvas or pressure-testing an existing draft. Produces a populated XLSX plus a Markdown critique. Use whenever the user is working on positioning, refreshing messaging, building a launch narrative, defining customer pains, or aligning a company on one brand line. Trigger eagerly on phrases like "help me build my messaging canvas", "pressure-test my messaging canvas", "build a messaging canvas", "messaging canvas", "messaging framework", "positioning canvas", "unicorn messaging", "unicorn canvas", "build my messaging", "pressure-test my messaging", "I'm refreshing our messaging", "three pains", "company alignment around messaging", "brand line", "power play" (in a positioning context), or anytime a PMM is laddering from brand line → pains → solutions → GTM motion.
---

# Sharebird Unicorn Canvas

## Overview

Walk a PMM through Chris Hines's Unicorn Messaging Framework canvas end-to-end. The canvas is one page, five layers (brand line → pains → differentiation → outcomes → modules → power plays), three columns (one per pain). When filled in well it functions as the single source of truth aligning positioning, product marketing, sales enablement, and CS narrative around the same three pains and one brand line.

Tone is medium-rigor: push back on weak answers ("this differentiation reads as a capability, not a customer value — try again?") but never block. Match `narrative-pressure-test` — direct, specific, never preachy.

Output is always two artifacts: a populated XLSX (the user's answers written into the Worked-example tab structure) plus a Markdown critique in the conversation.

**Everything you need to run this skill is inline below.** The bundled `references/`, `scripts/`, and `templates/` subdirectories are optional accelerators — use them if accessible (Claude Code CLI), but do not depend on them (Cowork, web). When in doubt, work from this file.

---

## Step 1 — Workflow Choice

At skill open, ask exactly one question and wait for the answer:

> Two paths — (a) **blank canvas**, walk through fresh; (b) you have a draft, **critique it**. Which one?

Branches:
- **blank-canvas** — fresh fill-in, layer-by-layer. Go to Step 2.
- **critique** — user pastes/uploads a draft. Skip to the Critique Branch below.

---

## Step 2 — Inputs Check (blank-canvas branch only)

Before Layer 1, ask one question and wait:

> Quick inputs check — what evidence do you have to anchor this canvas? Examples:
> - Customer interview transcripts or win/loss call notes
> - Competitive research or analyst reports
> - Customer outcome data with named references (case studies, ROI numbers)
> - Sales objection logs or recurring deal-stage friction points
> - An existing messaging doc, narrative draft, or sales deck we can pull from
>
> List what you have (or say "nothing yet" — that's a valid answer). I'll pull from your inputs at each layer and flag any layer where we're flying blind.

Calibration:
- **Rich inputs** — ask the user to paste/upload the most relevant items. Quote from them as you walk each layer. Anchor differentiation and outcomes in their actual customer language.
- **Thin or no inputs** — say plainly: *"This canvas will be hypothesis-driven. We'll walk it through to a clean v0, but you'll need to validate against real customer conversations before scaling it across enablement or the website."* Then proceed. Flag this again in the Output step's "recommended next actions."

After this, proceed to Layer 1.

---

## Step 3 — Layer-by-layer walkthrough (blank-canvas branch)

Walk top-to-bottom. Do not skip layers. For each layer use the inline rubric below to push back on weak answers. Hold the line on the dominant pain — most messaging fails because the three pains aren't truly distinct.

Layers, in order: **Brand line → Three pains → Differentiation (×3) → Outcomes (×3) → Modules (×3 per pain = 9) → Power plays (×3).**

---

## Step 4 — Critique Branch (alternative to Step 3)

1. Ask the user to paste or upload the draft. Accept HTML, XLSX text exports, raw markdown, or prose.
2. Parse into the 5-layer × 3-pain structure. If something is missing, say so explicitly — do not fabricate.
3. Walk each populated cell against the matching rubric section below. Call out specifically what is strong and what is weak. Suggest concrete rewrites — never just "this is generic."
4. If the user wants to revise, loop on the weakest 2–3 cells before moving to Output.

---

## Step 5 — Output (both branches converge here)

Collect the user's answers into this shape:

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

Then produce the XLSX. Use whichever path works in your environment:

**Path A — bundled script (Claude Code CLI, file access to skill dir).**
```
python3 scripts/fill_canvas.py --input <payload.json>
```
Reads `templates/canvas-blank.xlsx`, writes into the `Worked example` tab, saves to `output_path`.

**Path B — inline script (Cowork, web, anywhere `templates/` is unreachable).**
Write a fresh Python script in the conversation using openpyxl. Cell map (Worked example tab):

| Field | Cells |
|---|---|
| Brand line | `B5` (merged B5:D5) |
| Pain headers (`"EYEBROW \| title"`) | `B7`, `C7`, `D7` |
| Differentiation | `B9`, `C9`, `D9` |
| Outcomes | `B11`, `C11`, `D11` |
| Modules | `B12/B13/B14`, `C12/C13/C14`, `D12/D13/D14` |
| Power plays | `B15`, `C15`, `D15` |

Build the workbook from scratch with three tabs (`Read me`, `Worked example`, `Blank template`) — or, if the user uploads a copy of `Unicorn-Messaging-Canvas.xlsx`, write into that. Save the populated file and tell the user the path.

Then generate the Markdown critique summary directly in the conversation:

- **Strongest two cells.** Name them and say why.
- **Weakest two cells.** Name them and recommend a concrete rewrite.
- **Three recommended next actions.** Concrete, testable — e.g., "interview three accounts on Pain 2 to confirm the wording reflects how they actually describe it." If Step 2 flagged thin inputs, the first recommended action must be customer validation.
- **Handoff teaser.** One line — see below.

Closing line:

> The three Power Play rows are ready to operationalize — each one expands into a row in the Power Play Table. A future `sharebird-power-play-table` skill will pick this up; until then, the XLSX template is at the Sharebird playbook page.

---

## Inline Rubric

Use the matching section at each layer. Push back on weak answers; never block. If the user disagrees with your pressure-test, accept their reasoning and move on — your job is to surface the weakness, not litigate it.

### Brand line

**Job.** State, in one sentence, who the company is in the customer's world. Repeatable from memory. Customer-facing language only.

**Common mistake.** Writing a category descriptor ("we're a data security platform") instead of a customer-world line ("we keep your data discoverable, governed, and out of the wrong hands"). First describes a product shelf. Second describes a customer outcome.

**Pressure-test questions.**
1. Would a customer say this sentence back to you in their own words after a 30-min call? If not, it's too internal.
2. Strip every product word. Does it still make sense? If yes, it's too generic — swap one product anchor back in.
3. Does it work read aloud at a sales kickoff AND on a website hero? If only one, it's too narrow.
4. If a competitor copied this line word-for-word, would it still be true of them? If yes, undifferentiated.
5. Is this a sentence, or a tagline? A brand line is a sentence — taglines are downstream.

### Pains

**Job.** Surface the three customer pains the company is uniquely qualified to solve. Mutually exclusive. First pain is dominant; others ladder under it.

**Common mistake.** Three pains that all collapse into the same root pain ("data is messy" / "data is hard to find" / "data is hard to govern" — same pain three ways).

**Pressure-test questions.**
1. Could a customer experience Pain 1 without experiencing Pain 2? If no, merge or re-cut.
2. Which one is dominant? If you can't pick one, the cut isn't right yet.
3. Are these pains a customer would say out loud, or department names? "Access governance" is internal. "Auditors are flagging our access controls" is what a customer says.
4. If you ranked these pains across three target ICPs, would the rank order be consistent? If no, you may have three pains for three different ICPs — that's a different framework.
5. Do these pains map to real budget? A pain without budget is a wishlist item.

### Differentiation

**Job.** For each pain, name the one customer-value-shaped differentiator that makes this company the answer.

**Common mistake.** Capability words ("we have AI", "we have agents", "we have a graph") instead of customer-value words ("catches data exfiltration in minutes instead of weeks", "auto-revokes stale access without breaking workflows").

**Pressure-test questions.**
1. Is the subject the customer's outcome, or your product's feature? If the latter, rewrite.
2. Would three competitors write this same sentence about themselves? If yes, it's a category claim, not a differentiator.
3. What would a skeptical CISO say after reading this? If "so what" — the customer value is missing.
4. Does the language ladder up to the pain in the same column? If you can't draw a line from pain to differentiation, the column is broken.
5. Remove every adjective ("blazing-fast", "AI-native", "enterprise-grade"). Is there a real claim underneath? If not, the differentiation is decoration.

### Outcomes

**Job.** For each pain, name the numeric, customer-facing, real-reference outcome the company has delivered.

**Common mistake.** Vague directional language ("faster", "more secure", "easier") with no number and no named reference. Or numbers without a customer story (benchmark, not result).

**Pressure-test questions.**
1. Is there a number? If no, this isn't yet an outcome.
2. Customer-facing (buyer-felt) or internal (only engineering felt)? "Cut investigation time 14d → 90min" is customer-facing. "Reduced query latency 40%" is internal.
3. Named reference? A real customer who would let you say their name. If no, the outcome is unaudited.
4. Does the outcome resolve the pain in the same column? Pain "auditors flagging us" → outcome "engineers ship faster" = misaligned.
5. Could a competitor cite the same number? If yes, generic — find the version uniquely yours.

### Modules

**Job.** For each pain, name three product modules or capabilities that ladder up to it. SKU-shaped — what shows up on a pricing page.

**Common mistake.** Marketing themes ("AI-powered insights", "intelligent automation") instead of SKUs ("Data Discovery", "Access Reviews", "DLP Posture Manager"). Or modules from the wrong pain's column — they drift to where the team is proudest of the product, not where the pain actually lives.

**Pressure-test questions.**
1. Could a buyer order this on a contract? If no, it's a marketing theme, not a module.
2. Are these the three modules that genuinely solve THIS pain, or the three modules the team is most proud of? If the latter, re-cut by pain.
3. Do these modules overlap with another column? Some overlap is fine (platform). Total overlap means columns aren't cut by pain.
4. If a sales rep walks into a deal driven by this pain, are these the three modules they demo? If no, the column doesn't match how you sell.
5. Is one of these three carrying most of the weight? Mark it — that's your wedge module.

### Power plays

**Job.** For each pain, one sentence: who you target, what trigger you watch for, what asset/play you lead with, what the desired meeting is. Handoff to the Power Play Table.

**Common mistake.** A campaign tagline instead of a motion ("AI Security Now" is a tagline, not a play). Or an asset without a trigger/target ("we run a webinar" is half a play).

**Pressure-test questions.**
1. Does this sentence name a target ICP, a trigger, an asset, AND a desired meeting? If any of the four is missing, incomplete.
2. Is the trigger detectable — job title change, 10-K mention, funding event, tech stack signal? Or wishful thinking?
3. Could marketing, sales, AND CS each describe their role after reading this one sentence? If no, not yet operational.
4. Does this resolve the pain in the same column, or did it drift? Power plays drift toward the motion the team has the most reps on.
5. If you ran this play for a quarter and it didn't produce pipeline, what's the disconfirming evidence? If you can't name it, no measurable hypothesis.

---

## Optional bundled files (use if accessible)

These accelerate Path A but are not required:

- `templates/canvas-blank.xlsx` — three-tab source template (Read me / Worked example / Blank template).
- `templates/canvas-worked-example.xlsx` — Cyera-flavored worked example for "what good looks like."
- `references/rubric.md` — duplicate of the inline rubric above, kept for environments that prefer file references.
- `scripts/fill_canvas.py` — openpyxl helper for Path A. Cell map in the Output section matches what this script writes.

## What stays out of v1

- HTML output (XLSX only).
- Automatic ingestion of transcripts or prep docs (could become v2).
- Per-industry rubric variants — v1 is industry-neutral with cybersecurity examples from the Hines worked example.
- Power Play Table integration beyond the closing handoff line.
