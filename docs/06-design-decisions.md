---
doc_id: BKH-DEC-001
title: BankHaul design decisions register
project: BankHaul
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened; design decisions made under Amish's pre-approvals of 2026-10-03; two requirement decisions proposed
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: R5 and R8 decided by Amish on 2026-10-03 as recommended (BKH-DDR-003) and moved to decisions made; new open question on beds weaker than 4.9 kPa; change log added
---

# BankHaul design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in `docs/REVIEW.md`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list decisions.

> **Safety:** Several decisions below set BankHaul's safety case (weak links, working distance, stayed post, far stake, floods). Each took the conservative option; the evidence that would relax it is in BKH-DDR-001, Table 1.

## Open decisions

R5 (far stake in very soft mud) and R8 (cost per station) were decided by Amish on 2026-10-03 and are listed under decisions made (BKH-DDR-003). Applying them raised one new question; its state, options and recommendation are in `docs/REVIEW.md`, round 2 session.

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 3 | Beds weaker than 4.9 kPa: the 5.0 m stake driven 3.5 m gives a factor of 2 on R5 only down to a bed of 4.9 kPa; at 3 kPa it gives 1.22 | A: do not site a station where any vane reading is under 5 kPa (no cost). B: two long stakes 1 m apart tied at the top in such beds (factor 2.19 at 3 kPa, estimate; about 33 kg more and a tie bar). C: a float-and-mooring far end for such beds, designed at TRL 4 | Proposed, awaiting Amish. Recommend A | Site selection (section 3.2); none in the parts for A | BKH-CAL-001, E; BKH-DDR-003 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The weak link cord: three samples from the batch each release between 500 and 700 N as a single 80 mm loop | Sets the largest load a seized net can put into the system (R10) | BKH-CAL-001, C |
| 2 | The screw anchors' helix diameter, rod length and eye, and the supplier's holding figure in soft clay | The bank check uses a 250 mm helix 0.9 m deep (R4) | BKH-CAL-001, D |
| 3 | The blocks' eye and cheek-spacer positions sit outside the rope's path round the sheave, and the sheave takes 12 mm rope | The loop must not rub the block; the post and collar holes are set for this block length | BKH-DDR-002, item 9 |
| 4 | The jam cleats' fixing hole spacing | The cleat bar is drilled for 60 mm | BKH-DWG-101 |
| 5 | The rope's breaking strength, floating and UV stabilisation | Factor 5.7 after a season assumes 20 kN new and half lost to sun | BKH-CAL-001, F |
| 6 | The turnbuckles and shackles are rated and marked with their working load limits | They carry the stays at up to 2.1 kN | BKH-CAL-001, D |
| 7 | The bed's shear strength at the trial site (a hand vane on extension rods from the boat, down to 2.5 m) | Under 10 kPa: the 5.0 m stake driven 3.5 m (BKH-DDR-003); under 5 kPa: open decision 3 | BKH-CAL-001, E |

## Value engineering

Value-engineering target: USD 1,800 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 392 including the stake driving cap (USD 1,408 under the target); USD 404 with the 5.0 m stake for a very soft bed (BKH-DDR-003). R8 (USD 80 per station) is not met by the steel trial station; by Amish's decision of 2026-10-03 a local-materials station is costed with the co-design partner from local prices before the season pilot, and that figure replaces the estimate for R8. Main cost drivers and savings worth trying:

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
| 2026-10-03 | R5, far stake in very soft mud: option A, drive 3.5 m into very soft beds (5.0 m stake), the extra 1 m cut only where the vane test shows it is needed (factor 2.03 at 5 kPa) | Amish: "i approve all of the 47 recommendations provided by you. Execute them." | [BKH-DDR-003](decisions/0003-requirement-decisions-round2.md) |
| 2026-10-03 | R8, cost per station: option A, build the steel station for the TRL 4 trials and cost a local-materials station with the co-design partner before the season pilot (R8 not met for the trial station) | Amish, same instruction | [BKH-DDR-003](decisions/0003-requirement-decisions-round2.md) |

## Change log

| Date | Change |
| --- | --- |
| 2026-10-03 | v0.1: register opened at TRL 3 with R5 and R8 proposed, awaiting Amish |
| 2026-10-03 | v0.2: R5 (option A) and R8 (option A) decided by Amish (BKH-DDR-003) and moved to decisions made; open decision 3 (beds under 4.9 kPa) added; confirm item 7 updated |
