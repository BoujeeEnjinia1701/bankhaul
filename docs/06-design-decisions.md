---
doc_id: BKH-DEC-001
title: BankHaul design decisions register
project: BankHaul
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened; design decisions made under Amish's pre-approvals of 2026-10-03; two requirement decisions proposed
---

# BankHaul design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in `docs/REVIEW.md`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list decisions.

> **Safety:** Several decisions below set BankHaul's safety case (weak links, working distance, stayed post, far stake, floods). Each took the conservative option; the evidence that would relax it is in BKH-DDR-001, Table 1.

## Open decisions

Two requirements are not met or at risk on paper. They are not decided under the pre-approval; the state, options and recommendation for each are set out in `docs/REVIEW.md`, TRL 3 section, "Decisions for Amish".

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | R5, far stake holding in very soft mud: factor 1.23 on the 1.5 kN load where the bed's shear strength is about 5 kPa | A: drive 3.5 m into very soft beds (5.0 m stake); B: two stakes 1 m apart, tied at the top; C: keep 2.5 m and use only sites with a firmer bed | Proposed, awaiting Amish. Recommend A | Stake length and mass (section 3.2, step 6) | BKH-CAL-001, E; `docs/REVIEW.md` |
| 2 | R8, cost per station: USD 382 | A: build the steel station for the TRL 4 trials and cost a local-materials station with the co-design partner; B: switch the prototype to local materials now (about USD 98); C: one bank post and table for three loops (about USD 257 per loop) | Proposed, awaiting Amish. Recommend A | None if A; most made parts if B; the post head if C | BKH-CAL-001, I; `docs/REVIEW.md` |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The weak link cord: three samples from the batch each release between 500 and 700 N as a single 80 mm loop | Sets the largest load a seized net can put into the system (R10) | BKH-CAL-001, C |
| 2 | The screw anchors' helix diameter, rod length and eye, and the supplier's holding figure in soft clay | The bank check uses a 250 mm helix 0.9 m deep (R4) | BKH-CAL-001, D |
| 3 | The blocks' eye and cheek-spacer positions sit outside the rope's path round the sheave, and the sheave takes 12 mm rope | The loop must not rub the block; the post and collar holes are set for this block length | BKH-DDR-002, item 9 |
| 4 | The jam cleats' fixing hole spacing | The cleat bar is drilled for 60 mm | BKH-DWG-101 |
| 5 | The rope's breaking strength, floating and UV stabilisation | Factor 5.7 after a season assumes 20 kN new and half lost to sun | BKH-CAL-001, F |
| 6 | The turnbuckles and shackles are rated and marked with their working load limits | They carry the stays at up to 2.1 kN | BKH-CAL-001, D |
| 7 | The bed's shear strength at the trial site (a hand vane or cone test from the boat) | Decides whether open decision 1 applies there | BKH-CAL-001, E |

## Value engineering

Value-engineering target: USD 1,800 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 392 including the stake driving cap (USD 1,408 under the target). Main cost drivers and savings worth trying:

- The two screw anchors (USD 76) are the largest line, then the rope (USD 54), the far stake (USD 48), the two blocks (USD 44), the table (USD 35) and the post (USD 32).
- Rated rigging (shackles, turnbuckles, blocks) is kept because it carries the safety case.
- Savings worth trying: rope bought only for the site's span (USD 29 for 30 m); a local timber table; anchors bought in bulk through a fencing or utility supplier; a hardwood far pole where the bed is firm.

## Decisions made

The pre-approvals: Amish, 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." and, for this batch, "Proceed with the remaining 15 scaffolds".

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | Bank anchor: post on a foot plate, held back by two stays to two screw anchors | Amish, under both pre-approvals quoted above | BKH-DDR-001, item 1 |
| 2026-10-03 | Driven stake for the first prototype; float kept as a variant for deep beds | Amish, under both pre-approvals quoted above | BKH-DDR-001, item 2 |
| 2026-10-03 | Weak link at each net end, 500 to 700 N; requirement R10 added | Amish, under both pre-approvals quoted above | BKH-DDR-001, item 3 |
| 2026-10-03 | Fisher works at least 5 m from the water; post 6 m back; requirement R11 added | Amish, under both pre-approvals quoted above | BKH-DDR-001, item 4 |
| 2026-10-03 | 12 mm floating polysteel loop | Amish, under both pre-approvals quoted above | BKH-DDR-001, item 5 |
| 2026-10-03 | Two swivel rings half a loop apart as clip rings and end stops; net at least 2 m shorter than the span | Amish, under both pre-approvals quoted above | BKH-DDR-001, item 6 |
| 2026-10-03 | A jam cleat for each leg as the bank brake | Amish, under both pre-approvals quoted above | BKH-DDR-001, item 7 |
| 2026-10-03 | Haul by the net's near end with the loop following | Amish, under both pre-approvals quoted above | BKH-DDR-001, item 8 |
| 2026-10-03 | Loop taken out before floods | Amish, under both pre-approvals quoted above | BKH-DDR-001, item 9 |
| 2026-10-03 | First co-design candidate to approach: the Lake Kariba research group of the Oryx study with an inshore fishing cooperative (not agreed) | Amish, under both pre-approvals quoted above | BKH-DDR-001, item 10 |
| 2026-10-03 | CalRig as the first candidate proof-load rig; no hand capstan | Amish, under both pre-approvals quoted above | BKH-DDR-001, item 11 |
| 2026-10-03 | `budget_usd` kept at 1,800 as a value-engineering target | Amish: "I also accept any cost overruns or variations from the assumed scope cost." | BKH-DDR-001, item 12 |
| 2026-10-03 | Design for construction: the twelve changes of BKH-DDR-002 | Amish, under both pre-approvals quoted above | BKH-DDR-002 |
| 2026-10-03 | Appearance model additions for renders: loop cut short, stake above the bed only, net on the table, mannequin beside the post | Amish, under both pre-approvals quoted above | `docs/REVIEW.md`, TRL 3 |
