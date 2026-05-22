# Cyera worked-example transcript

A condensed walkthrough of what running `sharebird-unicorn-canvas` against the Cyera example looks like end-to-end. Use as a reference when reviewing or improving the skill.

---

**User:** I'm refreshing our messaging at Cyera — can you help me get to a one-page Unicorn canvas?

**Skill:** Two paths — (a) **blank canvas**, walk through fresh; (b) you have a draft, **critique it**. Which one?

**User:** Blank canvas.

**Skill:** Let's start with the brand line. One sentence: who is Cyera in the customer's world? Customer-facing language only — no category descriptors, no product nouns if you can help it.

**User:** We're a data security platform.

**Skill:** That's a category descriptor — strip every product word from that line and there's nothing left. Try again with the customer's outcome as the subject. What does Cyera do for them?

**User:** We make sure your data is discoverable, governed, and out of the wrong hands — wherever it lives.

**Skill:** That works. Customer-world subject, three real verbs, "wherever it lives" adds your platform footprint without making it the subject. Locking it in. Next: the three pains. Mutually exclusive, dominant pain first.

**User:** AI data exposure, access governance, DLP for regulated industries.

**Skill:** Those are department names, not pains a customer would say out loud. Try again as a sentence the customer would say. And confirm: which one is dominant — the one most likely to be in the CISO's top 3 board questions this quarter?

**User:** Dominant is AI data exposure. "AI is pulling sensitive data into models faster than security can see it." Pain 2: "Access governance is broken across hundreds of SaaS apps." Pain 3: "DLP rollups are failing the audit in regulated industries."

**Skill:** Strong. Quick MECE check — could a customer experience Pain 1 without experiencing Pain 2? Yes (a small AI-native company has no SaaS sprawl). Pain 2 without Pain 3? Yes (most non-regulated industries). Cut is clean. Moving to differentiation.

*(…walkthrough continues for differentiation, outcomes, modules, power plays, with the skill challenging the user on capability-vs-value language for differentiation and on missing numbers for outcomes.)*

---

**Skill:** Canvas is done. Writing the populated XLSX now.

```
Wrote ~/Downloads/unicorn-canvas-cyera-example.xlsx
```

### Critique summary

**Strongest two cells.**
- **Pain 1 (AI is pulling sensitive data into models faster than security can see it).** Direct, customer-voiced, names the velocity gap explicitly. This is the cell that will move enterprise CISO meetings.
- **Outcome 1 (14 days → 90 minutes at a Fortune-100 retailer).** Numeric, customer-facing, named reference. Three boxes ticked.

**Weakest two cells.**
- **Differentiation 3 ("audit-ready DLP rollups by control family").** Still reads internal — what does the auditor actually feel different? Suggested rewrite: "auditors stop asking the same control-family question twice — your team answers each one once."
- **Power play 2 (SaaS access governance).** Trigger ("a Workday or Okta consolidation project") is detectable but the desired meeting ("SaaS access audit workshop") is soft. Suggested rewrite: aim for "a 30-day access-cleanup pilot scoped to one app family" — tighter and more committable.

**Three recommended next actions.**
1. Interview three Pain-2 accounts to confirm the SaaS-sprawl language reflects how their IAM lead actually describes the problem.
2. Validate the Pain-3 outcome (6 weeks → 4 days) is still current — that's a 2024 number and audit cycles have changed.
3. Stress-test the dominant pain ranking with three frontline reps: do they pitch Pain 1 first, or do they default to Pain 2 because that's the play they have the most reps on?

**Handoff teaser.** The three Power Play rows are ready to operationalize — each one expands into a row in the Power Play Table. A future `sharebird-power-play-table` skill will pick this up; until then, the XLSX template is at the Sharebird playbook page.
