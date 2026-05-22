---
name: sharebird-unicorn-canvas
description: Walks a PMM through Chris Hines's Unicorn Messaging Framework canvas end-to-end — either filling in a blank canvas or pressure-testing an existing draft. Produces a populated XLSX plus a Markdown critique. Use whenever the user is working on positioning, refreshing messaging, building a launch narrative, defining customer pains, or aligning a company on one brand line. Trigger eagerly on phrases like "help me build my messaging canvas", "pressure-test my messaging canvas", "build a messaging canvas", "messaging canvas", "messaging framework", "positioning canvas", "unicorn messaging", "unicorn canvas", "build my messaging", "pressure-test my messaging", "I'm refreshing our messaging", "three pains", "company alignment around messaging", "brand line", "power play" (in a positioning context), or anytime a PMM is laddering from brand line → pains → solutions → GTM motion.
---

# Sharebird Unicorn Canvas

## Overview

Walk a PMM through Chris Hines's Unicorn Messaging Framework canvas: one page, five layers (brand line → pains → differentiation → outcomes → modules → power plays), three columns (one per pain). When filled in well it functions as the single source of truth aligning positioning, product marketing, sales enablement, and CS narrative around the same three pains and one brand line.

Tone: direct, specific, never preachy. Push back on weak answers, never block. If the user disagrees with a pressure-test, accept it and move on.

The skill supports three modes: **Information** (learn the framework), **Build** (synthesize a canvas from evidence — fresh or critique an existing draft), **Plan** (generate a research plan to gather the evidence needed before building). Use the mode that matches where the user is in their project.

---

## Step 1 — Mode Select

Open with one question, wait:

> Three paths — which fits where you are?
>
> 1. **Learn the framework.** You want to understand the Unicorn Messaging Framework canvas — what it is, how the layers connect, see a worked example. No canvas built.
> 2. **Build a canvas.** You have (or will paste/upload) customer evidence — transcripts, win/loss notes, competitive research — and want to synthesize a canvas. Fresh or critiquing an existing draft.
> 3. **Plan research to build a canvas later.** You want to use the canvas eventually but don't have the evidence yet. Generate a research plan + interview question packs you can run against customers, analysts, sales, CS.

Route accordingly. If the user's opening prompt already implies a mode ("explain the canvas" → Mode A; "build a canvas for Acme" → Mode B; "what research should I do" → Mode C), skip to that mode without asking.

---

## Mode A — Information

Ask one follow-up, wait:

> Two ways to learn — (a) **guided tour** through the Cyera worked example, layer by layer; (b) open **Q&A** about any part of the framework. Which?

**Tour path.** Walk through the worked example (bundled in `templates/canvas-worked-example.xlsx`, or describe inline if file access is unavailable). For each of the 6 layers in order:
- State the layer's **Job** (from the Inline Rubric).
- Show the Cyera cell as an example.
- Name the **Common mistake** for that layer.
- Offer one **Pressure-test question** as a "this is how the skill would push back."

End with: *"That's the whole canvas. When you're ready to build one for your company, restart me and pick Mode B. If you're not at the evidence stage yet, pick Mode C and I'll help you plan the research."*

**Q&A path.** Open-ended. Answer questions about layers, the framework's origin, how it compares to other messaging frameworks, etc. Use the Inline Rubric below as the primary source. Offer to switch into the tour if the user's questions suggest they'd benefit.

**Optional deliverable.** If the user asks for something shareable, produce a one-page reference card (markdown) summarizing the 6 layers + one sample line each. Save to `~/Downloads/unicorn-canvas-reference.md`.

No XLSX produced in Mode A. No grounding questions, no pressure-tests of user answers — they're not building yet.

---

## Mode B — Build a Canvas

Ask one sub-option, wait:

> Two paths inside Build — (a) **blank canvas**, walk through fresh; (b) you have a **draft to critique**, walk it cell-by-cell.

Both paths run Steps 2–3 (Context + Inputs), then differ at Step 4.

### Step 2 — Context Check

Ask one thing, wait:

> Before we start: **company + product** in one line.

That's the only canvas-level fact the skill needs up front. Buyer personas are captured per-pain in the Pains layer — most products serve multiple buyer types (a CISO feels Pain 1, a Compliance lead feels Pain 3), and the canvas accommodates that. The brand line still has to work across every persona the product serves (the brand-line pressure-test enforces this — *"works at a sales kickoff AND on a website hero"*).

The canvas is one source of truth — written once, in neutral surface-durable language. Different downstream surfaces (exec memo, sales deck, website hero) are translations FROM the canvas, handled at Output time — not different versions OF the canvas.

### Step 3 — Inputs Check (auto-ingest, then confirm + add more)

The skill auto-detects likely transcript / prep-doc files in the working folder and offers to ingest them. The user can add more paths, URLs, or pasted excerpts.

**Path A — auto-detect mode (preferred):** Run `scripts/ingest_inputs.py --working-folder <path>` on the conversation's working folder. Present what was found:

> I found these files in your working folder — should I ingest all of them?
> - [filename] · [source_type] · [chars]
>
> Anything to add — additional file paths, Google Doc / Sheet URLs, or pasted excerpts?

If the user adds paths or URLs, re-run with `--path` / `--url`. Confirm: *"Ingested N sources, ~M chars. I'll quote from them at each layer."*

**Path B — no auto-detect:** Ask the user directly for paths / URLs / pasted excerpts.

**Path C — no inputs at all:** Say *"This canvas will be hypothesis-driven. We'll walk it through to a clean v0, but you'll need to validate against real customer conversations before scaling it."* The first Recommended Next Action at Output time must be customer validation. Consider suggesting Mode C as a way to plan that validation work upfront.

PDF extraction is macOS-only. Linux/Windows users hitting a PDF see a warning — fall back to `.docx` conversion or pasted excerpts.

### Step 4 — Layer-by-layer walkthrough (blank-canvas sub-path)

For each layer in order — **Brand line → Three pains → Differentiation (×3) → Outcomes (×3) → Modules (3 per pain = 9) → Power plays (×3)** — run this sequence:

1. **Readiness gate.** Check the layer's **Readiness criterion** from the Inline Rubric against what you know about the user's evidence base. If criterion met → proceed to step 2. If not met → ask:
   > Quick gate for **[Layer]** — [criterion]. Do you have this?
   >
   > Three options if not:
   > - (a) **Mark `[VALIDATE]` and fill with best hypothesis.** We'll come back later. Output will flag this for follow-up validation.
   > - (b) **Pause and generate a research mini-plan for this layer now.** I'll produce 2-3 question stems + target evidence type + timeline — you can run the research later and rebuild the layer.
   > - (c) **Skip this layer entirely.** Rare; usually flags a structural issue with the canvas (wrong product scope, wrong stage).
2. **Ask the layer's grounding question** (from the rubric).
3. **If transcripts were ingested in Step 3, surface 2–3 relevant quotes** from `concatenated_text` for this layer ("Here's how your customers describe [pain]: [quote 1, source]; [quote 2, source]").
4. **Ask the user to craft the cell in their own words.** Suggest quotes only — do NOT draft cells for the user.
5. **Pressure-test using the rubric.**
6. **When locked, move on.**

If the user picks (b) in step 1, generate the mini-plan as a markdown block inline:
> **Research mini-plan: [Layer]**
> - **Question stems:** 2-3 stems formatted for the target research type
> - **Target evidence:** what kind of response moves this from assumed to validated
> - **Timeline:** 1-week / 2-week / ongoing

Then return to the next layer (the mini-plan layer gets `[VALIDATE]` until the research happens). The user can run Mode C separately for a full canvas-wide research plan.

Hold the line on the dominant pain. Most messaging fails because the three pains aren't truly distinct.

### Step 4 — Critique sub-path (alternative)

If the user chose to critique an existing draft:

> Three more things before I critique:
> 1. **Who wrote this draft** — solo PMM, agency, exec, group exercise?
> 2. **What's the goal** — improve before launch, kill a bad direction, align stakeholders?
> 3. **What evidence backed each cell** when it was written?

Then ask for the draft (HTML, XLSX text, markdown, prose). Parse into the 5-layer × 3-pain structure — say so explicitly when something is missing rather than fabricating. Walk each populated cell against the rubric. Suggest concrete rewrites, never "this is generic." Loop on the weakest 2–3 cells if the user wants to revise, then go to Output. Readiness gate also applies here per layer when revising.

### Step 5 — Output (both sub-paths converge)

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
- **Three recommended next actions.** Concrete, testable. **If Step 3 flagged thin/no inputs, OR any Outcome was marked `[VALIDATE]`, OR any Module was marked `[BETA]` / `[ROADMAP]`, OR any layer routed to a mini-plan in Step 4, the first recommended action must be the matching validation task.** One of the three actions should always be **surface translation** — once the canvas is locked, translate it into the specific deliverables it feeds (exec memo, sales kickoff deck, website hero rewrite, board update).
- **Handoff teaser:** *"The three Power Play rows are ready to operationalize — each one expands into a row in the Power Play Table. A future `sharebird-power-play-table` skill will pick this up; until then, the XLSX template is bundled with this plugin at `templates/canvas-blank.xlsx`."*

---

## Mode C — Plan Research

Generate a structured research plan + interview question packs the user can run BEFORE building the canvas. Output is markdown saved to disk, formatted to drop into Sharebird's deep-dive prep doc (the practitioner-interview template Sharebird uses to extract playbooks).

### Step 2 — Context Check

Same one question as Mode B (company + product). Personas are captured per-pain in the Inputs Audit below.

### Step 3 — Inputs Audit (per layer)

For each of the 6 layers in order, ask:

> **[Layer]** — what evidence do you have today?
> - Brand line: existing tagline / hero copy / mission, customer-voiced descriptions of who you are.
> - Pains: customer interview transcripts, win/loss notes, sales objection logs.
> - Differentiation: competitive research, analyst reports, customer comparisons to alternatives.
> - Outcomes: customer outcome data with named references (case studies, ROI numbers, willing-to-be-cited customers).
> - Modules: current pricing-page / SKU list / capability matrix.
> - Power plays: existing GTM motions the team runs reps on, target ICP lists, trigger detection signals.
>
> *"None"* is a valid answer. Capture per layer: ✅ Ready / ⚠️ Partial / ❌ Missing + the specific gap.

### Step 4 — Generate research plan

Produce a markdown document saved to `~/Downloads/unicorn-canvas-research-plan-{company-slug}.md` with three sections:

#### Section 1 — Framework readiness checklist

| Layer | Status | Gap |
|---|---|---|
| Brand line | ✅ / ⚠️ / ❌ | Specific missing input |
| Pains | ... | ... |
| Differentiation | ... | ... |
| Outcomes | ... | ... |
| Modules | ... | ... |
| Power plays | ... | ... |

#### Section 2 — Research plan

For each layer with ⚠️ or ❌ status:

| Layer | Gap | Research type | Question stems | Evidence target | Timeline |
|---|---|---|---|---|---|
| [Layer] | [What's missing] | Customer call / Analyst / Field expert / Sales / CS | 2-3 specific stems | What kind of response validates the layer | 1-week / 2-week / ongoing |

#### Section 3 — Question packs by research type

For each research type referenced in Section 2, produce a pack of 5–7 question stems. Format each stem with a one-line "why-asked" so the PMM understands the intent:

```
### Customer call — [per-pain persona]
1. [Question stem] — why-asked: [one line]
2. [Question stem] — why-asked: [one line]
...

### Analyst interview
1. ...

### Field expert validation
1. ...

### Sales / GTM alignment
1. ...

### CS validation
1. ...
```

**Companion-to-deep-dive format note.** These question stems are designed to plug into Sharebird's deep-dive prep doc — same per-phase columnar structure (tactics / artifacts / contrarian). A PMM can paste them directly into a Hines-style prep doc to run with a practitioner.

End the document with:

> ## Recommended sequence
> 1. Run the **Customer call** pack first — produces the inputs for Pains + Differentiation + Outcomes layers (the three highest-leverage layers).
> 2. Run **Sales / CS** packs in parallel — validates Modules + Power plays.
> 3. Run **Analyst** and **Field expert** packs last — sharpens differentiation language and validates contrarian moves.
>
> When you have the evidence, restart this skill in **Mode B** to synthesize the canvas. Drop your research transcripts in the working folder — the skill will auto-ingest and surface customer-voice quotes at each layer.

Save to disk, tell the user the path, and close with: *"That's your research plan. When the evidence is in, come back to Mode B."*

---

## Inline Rubric

Each layer: **Job / Grounding question / Common mistake / Pressure-test questions / Readiness criterion.** Ask the Grounding question BEFORE the user answers (Mode B). Check the Readiness criterion BEFORE the layer starts (Mode B). Use Pressure-tests AFTER the user gives an answer (Mode B). Use Job + Common mistake + sample pressure-test for Mode A's tour.

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

**Readiness criterion.** Have an existing brand line OR have customer-voiced descriptions of who the company is (3+ direct quotes or paraphrases from interviews / win-loss / hero-copy testing).

### Pains

**Job.** Three customer pains the company is uniquely qualified to solve. Mutually exclusive. First is dominant.

**Grounding question.** *"For each pain, who specifically feels it? Title, company size, vertical. Different pains can target different personas — that's normal for products serving multiple buyers (a CISO feels Pain 1, an IT/IAM lead feels Pain 2, a Compliance/GRC lead feels Pain 3). Capture the persona per pain so the rest of the column lands right. What stays consistent across the canvas: the PRODUCT being positioned, not the buyer."*

**Common mistake.** Three pains that collapse into the same root pain ("data is messy" / "hard to find" / "hard to govern" — same pain three ways). Or three pains that are actually about three different products dressed as pains for one canvas.

**Pressure-test questions.**
1. Could a target ACCOUNT experience Pain 1 without Pain 2 (even if different personas inside that account feel them)? If no — the pains always co-occur in the same buyer's life — merge or re-cut.
2. Which pain is dominant? If you can't pick one, the cut isn't right yet.
3. Customer-language, or department names? "Access governance" is internal; "auditors are flagging our access controls" is what a customer says.
4. Do the three pains hold together as a single PRODUCT'S story across a target account? If a buyer in that account would say "those are three different products," the pains aren't right for this canvas — you may have a portfolio canvas trying to live as one product canvas.
5. Per pain, does it map to real budget in that persona's org? Pain without budget for that persona is a wishlist.

**Readiness criterion.** Customer-voiced pain language for the relevant persona per pain — at least 3 quotes per pain candidate, from interviews / win-loss calls / sales objection logs with that specific persona.

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

**Readiness criterion.** Named competitive context per pain — status quo, named competitor, in-house build, or category. Plus customer or analyst language describing the comparative gap.

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

**Readiness criterion.** At least one numeric, customer-facing, named-reference outcome per pain. CS / customer marketing should confirm willing-to-be-cited.

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

**Readiness criterion.** Current pricing-page / SKU list / capability matrix confirming what's GA today. PM confirmation on what's `[BETA]` vs. `[ROADMAP]`.

### Power plays

**Job.** For each pain, one sentence: target ICP + trigger + asset/play + desired meeting. Handoff to the Power Play Table.

**Grounding question.** *"For each power play, what's the GTM motion your team currently runs that this would extend or replace? If a play is greenfield — zero existing reps — mark it `[NEW MOTION]` and treat the first quarter as pilot, not production. Inventing plays the team can't execute is how canvases turn into shelfware."*

**Common mistake.** Campaign tagline instead of a motion ("AI Security Now" is a tagline). Or an asset without a trigger/target ("we run a webinar" is half a play).

**Pressure-test questions.**
1. Names target ICP, trigger, asset, AND desired meeting? If any of the four missing, incomplete.
2. Is the trigger detectable — title change, 10-K mention, funding event, tech stack signal? Or wishful thinking?
3. Could marketing, sales, AND CS each describe their role after reading this one sentence? If no, not operational.
4. Does this resolve the pain in the same column, or did it drift? Plays drift toward motions the team has the most reps on.
5. Run for a quarter without producing pipeline — what's the disconfirming evidence? If you can't name it, no measurable hypothesis.

**Readiness criterion.** At least a v0 motion per pain the team has existing reps on, OR willingness to mark `[NEW MOTION]` and treat the first quarter as pilot.
