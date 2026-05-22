---
name: sharebird-unicorn-canvas
description: Walks a PMM through Chris Hines's Unicorn Messaging Framework canvas end-to-end — either filling in a blank canvas or pressure-testing an existing draft. Produces a populated XLSX plus a Markdown critique. Use whenever the user is working on positioning, refreshing messaging, building a launch narrative, defining customer pains, or aligning a company on one brand line. Trigger eagerly on phrases like "help me build my messaging canvas", "pressure-test my messaging canvas", "build a messaging canvas", "messaging canvas", "messaging framework", "positioning canvas", "unicorn messaging", "unicorn canvas", "build my messaging", "pressure-test my messaging", "I'm refreshing our messaging", "three pains", "company alignment around messaging", "brand line", "power play" (in a positioning context), or anytime a PMM is laddering from brand line → pains → solutions → GTM motion.
---

# Sharebird Unicorn Canvas

## Overview

Walk a PMM through Chris Hines's Unicorn Messaging Framework canvas: one page, five layers (brand line → pains → differentiation → outcomes → modules → power plays), three columns (one per pain). Output is two artifacts — a populated XLSX plus a Markdown critique.

Tone: direct, specific, never preachy. Push back on weak answers, never block. If the user disagrees with a pressure-test, accept it and move on.

## Step 1 — Workflow Choice

Ask one question, wait:

> Two paths — (a) **blank canvas**, walk through fresh; (b) you have a draft, **critique it**. Which one?

Blank → Step 2. Critique → Step 5.

## Step 2 — Context Check

Ask two things in one turn, terse answers fine:

> Before we start, two quick things:
> 1. **Company + product** in one line.
> 2. **Target ICP** for this canvas — title, company size, vertical if relevant.
>
> One ICP per canvas. Multiple ICPs = separate canvases; pain language doesn't generalize.

The canvas is one source of truth — write it once, in neutral surface-durable language (the brand-line pressure-test enforces this: "works at a sales kickoff AND on a website hero"). Different downstream surfaces (exec memo, sales deck, website hero) are translations FROM the canvas, handled in Output Step 6's recommended-next-actions — not different versions OF the canvas.

## Step 3 — Inputs Check

Ask what evidence the user has, then **actively request the 2 highest-leverage artifacts.**

> Quick inputs check — what evidence do you have to anchor this canvas?
> - Customer interview transcripts or win/loss notes (highest leverage)
> - Customer outcome data with named references (critical for Outcomes layer)
> - Competitive research / analyst reports (important for Differentiation)
> - Sales objection logs (useful for power-play triggers)
> - Existing messaging docs, narrative drafts, sales decks (useful for Brand line + as critique baseline)
>
> List what you have (or "nothing yet" — that's valid).

After they answer, name the top 2 and ask for them: *"Of what you listed, the most useful right now are [type 1] and [type 2]. Paste the most relevant excerpts (or upload). I'll quote from them as we walk each layer."*

If "nothing yet": say plainly *"This canvas will be hypothesis-driven. We'll walk it through to a clean v0, but you'll need to validate against real customer conversations before scaling it across enablement, sales decks, or the website."* The first Recommended Next Action at Output time must be customer validation.

## Step 4 — Layer-by-layer walkthrough (blank-canvas branch)

For each layer: (1) ask the layer's **Grounding question** from the rubric, (2) ask for the user's answer, (3) pressure-test using the rubric, (4) when locked, move on.

Layers, in order: **Brand line → Three pains → Differentiation (×3) → Outcomes (×3) → Modules (3 per pain = 9) → Power plays (×3).**

Hold the line on the dominant pain. Most messaging fails because the three pains aren't truly distinct.

## Step 5 — Critique Branch (alternative to Step 4)

Run Steps 2 and 3 first. Then add:

> Three more things before I critique:
> 1. **Who wrote this draft** — solo PMM, agency, exec, group exercise?
> 2. **What's the goal** — improve before launch, kill a bad direction, align stakeholders?
> 3. **What evidence backed each cell** when it was written?

Then: ask user to paste/upload the draft (HTML, XLSX text, markdown, prose). Parse into the 5-layer × 3-pain structure — say so explicitly when something is missing rather than fabricating. Walk each populated cell against the rubric. Suggest concrete rewrites, never "this is generic." Loop on the weakest 2–3 cells if the user wants to revise, then go to Output.

## Step 6 — Output (both branches converge)

Collect the user's answers into this payload:

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

Produce the XLSX. If `scripts/fill_canvas.py` and `templates/canvas-blank.xlsx` are accessible (Claude Code CLI), run `python3 scripts/fill_canvas.py --input <payload.json>`. Otherwise (Cowork, web), write a fresh openpyxl script inline using this cell map for the `Worked example` tab:

| Field | Cells |
|---|---|
| Brand line | `B5` (merged B5:D5) |
| Pain headers (`"EYEBROW \| title"`) | `B7`, `C7`, `D7` |
| Differentiation | `B9`, `C9`, `D9` |
| Outcomes | `B11`, `C11`, `D11` |
| Modules | `B12/B13/B14`, `C12/C13/C14`, `D12/D13/D14` |
| Power plays | `B15`, `C15`, `D15` |

Save to the user's Downloads folder (`Path(output_path).expanduser()` resolves correctly on macOS, Linux, and Windows). Tell the user the path.

Then generate the Markdown critique in the conversation:

- **Strongest two cells.** Name them and say why.
- **Weakest two cells.** Name them and recommend a concrete rewrite.
- **Three recommended next actions.** Concrete, testable. **If Step 3 flagged thin/no inputs, OR any Outcome was marked `[VALIDATE]`, OR any Module was marked `[BETA]` / `[ROADMAP]`, the first recommended action must be the matching validation task** (customer interviews, outcome confirmation, module-availability check). One of the three actions should always be **surface translation** — once the canvas is locked, translate it into the specific deliverables it feeds (exec memo, sales kickoff deck, website hero rewrite, board update). The canvas is source-of-truth; each surface is a downstream copywriting pass that pulls from it.
- **Handoff teaser:** *"The three Power Play rows are ready to operationalize — each one expands into a row in the Power Play Table. A future `sharebird-power-play-table` skill will pick this up; until then, the XLSX template is bundled with this plugin at `templates/canvas-blank.xlsx` (or downloadable from the GitHub release)."*

---

## Inline Rubric

Each layer: **Job / Grounding question / Common mistake / Pressure-test questions.** Ask the Grounding question BEFORE the user answers; use Pressure-tests AFTER.

### Brand line

**Job.** One sentence: who is the company in the customer's world. Repeatable from memory. Customer-facing.

**Grounding question.** *"Do you have a brand line today — tagline, mission, hero copy, anything from the last brand refresh? Paste it. We'll either pressure-test what's there or replace it deliberately."* If they have one, START from critique.

**Common mistake.** Writing a category descriptor ("we're a data security platform") instead of a customer-world line ("we keep your data discoverable, governed, and out of the wrong hands").

**Pressure-test questions.**
1. Would a customer say this back to you in their own words after a 30-min call? If not, too internal.
2. Strip every product word — still makes sense? If yes, too generic; add a product anchor.
3. Works at a sales kickoff AND on a website hero? If only one, too narrow.
4. Could a competitor copy this word-for-word and have it still be true? If yes, undifferentiated.
5. Sentence or tagline? Brand line is a sentence; taglines are downstream.

### Pains

**Job.** Three customer pains the company is uniquely qualified to solve. Mutually exclusive. First is dominant.

**Grounding question.** Restate ICP from Step 2: *"Writing pains for [ICP]. Three pains for one ICP, mutually exclusive. If you find yourself wanting pains for a different ICP, stop me — we'll run a separate canvas. Pain language doesn't generalize across ICPs and that's the most common reason canvases break."*

**Common mistake.** Three pains that collapse into the same root pain ("data is messy" / "hard to find" / "hard to govern" — same pain three ways).

**Pressure-test questions.**
1. Could a customer experience Pain 1 without Pain 2? If no, merge or re-cut.
2. Which is dominant? If you can't pick one, the cut isn't right.
3. Customer-language, or department names? "Access governance" is internal; "auditors are flagging our access controls" is what a customer says.
4. If ranked across three target accounts in your ICP, would rank order be consistent? If no, you may have three pains for three sub-segments — re-cut or split the canvas.
5. Do these map to real budget? Pain without budget is a wishlist.

### Differentiation

**Job.** For each pain, one customer-value-shaped differentiator.

**Grounding question.** *"For each pain, who or what are you positioning against — status quo, a named competitor (which?), an in-house build, a different category? Capture the opponent in brackets if helpful (`[vs. Splunk]`, `[vs. status quo: Excel + email]`). Differentiation without a named opponent is decoration."*

**Common mistake.** Capability words ("we have AI", "agents", "a graph") instead of customer-value words ("catches data exfiltration in minutes instead of weeks", "auto-revokes stale access without breaking workflows").

**Pressure-test questions.**
1. Is the subject the customer's outcome, or your product's feature? Latter → rewrite.
2. Would the named opponent write this same sentence about themselves? If yes, it's a category claim.
3. What would a skeptical buyer say? If "so what" — customer value missing.
4. Does the language ladder up to the pain in the same column? If no, column broken.
5. Strip every adjective ("blazing-fast", "AI-native", "enterprise-grade"). Real claim underneath? If not, decoration.

### Outcomes

**Job.** For each pain, numeric, customer-facing, real-reference outcome.

**Grounding question.** *"For each pain, do you have an actual customer outcome with a named reference, or are we writing directional hypotheses? Mark hypothesis-only outcomes `[VALIDATE]` — they become customer-interview tasks in the recommended-next-actions list. Don't ship un-validated outcomes to sales — they leak into decks as facts and become claims you can't defend on calls."*

**Common mistake.** Vague directional language ("faster", "more secure") with no number and no named reference. Or numbers without a customer story (benchmark, not result).

**Pressure-test questions.**
1. Is there a number? If no, not yet an outcome.
2. Customer-facing or internal? "Cut investigation time 14d → 90min" is customer-facing. "Reduced query latency 40%" is internal.
3. Named reference willing to be cited? If no, mark `[VALIDATE]`.
4. Does the outcome resolve the pain in the same column? "Auditors flagging us" → "engineers ship faster" = misaligned.
5. Could a competitor cite the same number? If yes, generic — find the version uniquely yours.

### Modules

**Job.** For each pain, three product modules that ladder up to it. SKU-shaped.

**Grounding question.** *"Constraint: list only what's generally available today, in the order a buyer sees them on a pricing page. Beta items get `[BETA]`, roadmap items get `[ROADMAP]` — they can appear but the power play in this column can't be anchored on them. Power plays anchored on roadmap modules fail when sales tries to demo them; the damage shows up 60 days later, not in canvas review."*

**Common mistake.** Marketing themes ("AI-powered insights", "intelligent automation") instead of SKUs ("Data Discovery", "Access Reviews", "DLP Posture Manager"). Or modules from the wrong pain's column — they drift to where the team is proudest, not where the pain lives.

**Pressure-test questions.**
1. Could a buyer order this on a contract? If no, it's a marketing theme.
2. Are these the three modules that solve THIS pain, or the three the team is proudest of? If latter, re-cut by pain.
3. Do these overlap with another column? Some overlap is fine (platform). Total overlap = columns not cut by pain.
4. If a sales rep walks into a deal driven by this pain, are these the three modules they demo? If no, column doesn't match how you sell.
5. Is one carrying most of the weight? Mark it — that's your wedge module.

### Power plays

**Job.** For each pain, one sentence: target ICP + trigger + asset/play + desired meeting. Handoff to the Power Play Table.

**Grounding question.** *"For each power play, what's the GTM motion your team currently runs that this would extend or replace? If a play is greenfield — zero existing reps — mark it `[NEW MOTION]` and treat the first quarter as pilot, not production. Inventing plays the team can't execute is how canvases turn into shelfware."*

**Common mistake.** Campaign tagline instead of a motion ("AI Security Now" is a tagline). Or an asset without a trigger/target ("we run a webinar" is half a play).

**Pressure-test questions.**
1. Names target ICP, trigger, asset, AND desired meeting? If any of the four missing, incomplete.
2. Is the trigger detectable — title change, 10-K mention, funding event, tech stack signal? Or wishful thinking?
3. Could marketing, sales, AND CS each describe their role after reading this one sentence? If no, not operational.
4. Does this resolve the pain in the same column, or did it drift? Plays drift toward motions the team has reps on.
5. Run for a quarter without producing pipeline — what's the disconfirming evidence? If you can't name it, no measurable hypothesis.
