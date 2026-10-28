---
doc_id: BKH-DEC-001
title: BankHaul design decisions register
project: BankHaul
doc_type: Design decisions register
version: '0.4'
status: Draft
date: '2026-10-25'
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
  change: Amish decided both open items (14A far stake 3.5 m, 15A R8 restated); moved to Decisions made (BKH-DDR-003)
- version: "0.3"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Kit 1.8 and 1.9 upgrade: STEM fixes D-S1 to D-S7 decided under Amish's standing instruction of 2026-10-23 (D-S5 to D-S7 after the independent review); concept selection O-1 and seven more items proposed, awaiting Amish; items to confirm 9 to 12"
- version: '0.4'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Amish decided O-1 to O-8 as recommended on 2026-10-25 ("i concur with your recommendations"); moved to decisions made; station USD 399'
---

# BankHaul design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in `docs/REVIEW.md`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list decisions.

> **Safety:** Several decisions below set BankHaul's safety case (weak links, working distance, stayed post, far stake, floods). Each took the conservative option; the evidence that would relax it is in BKH-DDR-001, Table 1.

## Open decisions

None. Amish decided O-1 to O-8 on 2026-10-25 as recommended ("i concur with your recommendations"); they are under Decisions made.

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The weak link cord: three samples from the batch each release between 500 and 700 N as a single 80 mm loop | Sets the largest load a seized net can put into the system (R10) | BKH-CAL-001, C |
| 2 | The screw anchors' helix diameter, rod length and eye, and the supplier's holding figure in soft clay | The bank check uses a 250 mm helix 0.9 m deep (R4) | BKH-CAL-001, D |
| 3 | The blocks' eye and cheek-spacer positions sit outside the rope's path round the sheave, and the sheave takes 12 mm rope | The loop must not rub the block; the post and collar holes are set for this block length | BKH-DDR-002, item 9 |
| 4 | The jam cleats' fixing hole spacing | The cleat bar is drilled for 60 mm | BKH-DWG-101 |
| 5 | The rope's breaking strength, floating and UV stabilisation | Factor 5.7 after a season assumes 20 kN new and half lost to sun | BKH-CAL-001, F |
| 6 | The turnbuckles and shackles are rated and marked with their working load limits | They carry the stays at up to 2.1 kN | BKH-CAL-001, D |
| 7 | The bed's shear strength at the trial site (a hand vane or cone test from the boat) | The 3.5 m stake holds at factor 2.03 down to about 5 kPa; a softer bed needs a new check | BKH-CAL-001, E |
| 8 | Local prices for the local-materials station, with the co-design partner | Sets the restated R8 figure (estimate about USD 98 against USD 80) | BKH-CAL-001, I; BKH-DDR-003 |
| 9 | The shackle, turnbuckle and block envelopes match the D3 model: 10 mm bow shackle with 18 mm jaw and 51 mm from pin to bow; M12 jaw-and-jaw turnbuckle 200 mm pin to pin at mid take-up | The stay chain closes at 1,110 mm between thimbles (D-S3) only with this hardware | `cad/src/bkh_parts.py`; BKH-CAL-001 D |
| 10 | The pin-plate rule used for D-S1, from the text of EN 1993-1-8 Table 3.9 | The formula was used as commonly quoted; the standard's text was not consulted | BKH-STM-001 S13 |
| 11 | The steel grades: S235 plate and S355 stake tube, with mill certificates | The pad eye check uses S235; the stake capacity uses S355 (long-pile case, D-S2) | BKH-CAL-001 D, E |
| 12 | The bed under the far stake has no firm layer above 3.5 m (probe from the boat) | A firm layer stops the stake short of its embedment (STEM S17) | BKH-BLD-001 step 6 |

## Value engineering

Value-engineering target: USD 1,800 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 409 including the stake driving cap (USD 1,391 under the target). Main cost drivers and savings worth trying:

- The two screw anchors (USD 76) are the largest line, then the far stake (USD 60), the rope (USD 54), the two blocks (USD 44), the table (USD 35) and the post (USD 32).
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
| 2026-10-03 | 14A, R5: far stake 5.0 m long, driven 3.5 m (factor 2.03 in very soft mud; USD 12 and 6.4 kg more) | Amish, 2026-10-03: "i agree with all the 46 recommendations you provided. please proceed." | BKH-DDR-003 |
| 2026-10-03 | 15A, R8: build the steel station for the TRL 4 trials and cost a local-materials station with the co-design partner; R8 restated to apply USD 80 to the local-materials station | Amish, 2026-10-03: "i agree with all the 46 recommendations you provided. please proceed." | BKH-DDR-003 |
| 2026-10-25 | D-S1: pad eye 64 mm radial (plate 64 x 100 mm, its end 88 mm from the post axis; was 60 x 100, written 84 x 100 in the BOM as the distance from the axis), hole unchanged, so its end distance meets EN 1993-1-8 Table 3.9 at 1.5 x 3 kN (15.2 mm against 13.2 mm; was 11.2 mm). Options weighed: a longer pad eye (chosen, no cost); a 10 mm plate (end distance still short); the hole moved 4 mm inboard (moves the block and the loop). Cost: none | Claude under Amish's standing instruction of 2026-10-23 (STEM fix, BKH-STM-001 S13); Amish can reverse it | BKH-STM-001; BKH-CAL-001 D |
| 2026-10-25 | D-S2: the far stake's capacity is the lesser of Broms' short-pile (soil fails) and long-pile (stake yields) cases: 4.2 kN in soft mud (factor 2.77, was stated 6.1 kN and 4.05) and 3.0 kN in very soft mud (2.03, unchanged, governs). No design change; PR-005 stays met | Claude under Amish's standing instruction of 2026-10-23 (STEM fix, S15) | BKH-STM-001; BKH-CAL-001 E |
| 2026-10-25 | D-S3: back-stays 1,110 mm between thimble centres, cut 1.5 m (were drawn 1,440 mm between eyes, cut 1.8 m), so the chain of lug shackle, stay, shackle and turnbuckle closes at mid take-up between the lug and the anchor eye 1,440 mm apart. Options weighed: shorter stays (chosen, no cost); anchors moved 330 mm further back (larger footprint, changes the stay angle and R4). Cost: none | Claude under Amish's standing instruction of 2026-10-23 (STEM fix, S29) | BKH-STM-001; BKH-CAL-001 D; BKH-DWG-105 |
| 2026-10-25 | D-S4: fits found by the D3 model: table legs 825 mm (were 750, below the rails), end rails 550 mm fitted inside the legs (were 475, clashing with them), screws through the rails into the legs and eight 6 x 100 mm screws through the lip boards; jam cleat bolts M8 x 35 (were M8 x 50). Cost: about USD 1 | Claude under Amish's standing instruction of 2026-10-23 (STEM fix, S29) | BKH-STM-001; BKH-DWG-104; bom/bom.csv |
| 2026-10-25 | D-S5: the stays' rope is checked at its rated 1,590 kg (15.6 kN, Marlow, 10 mm three-strand polyester), not 22 kN: factor 6.4 at the 3 kN bank load (was 9.0), above 5. No design change (found by the independent review) | Claude under Amish's standing instruction of 2026-10-23 (STEM fix, S9) | BKH-STM-001; BKH-CAL-001 D |
| 2026-10-25 | D-S6: both ends of each loop half are eye-spliced round the swivel rings, the second at installation with the rope work kit; the round turn and two half hitches kept about 60 % of the rope's strength, a factor of 4.0 at the season's end against 5. A span change means re-splicing (about 15 minutes). Options weighed: splice both ends (chosen, no cost); 12-strand rope with a hitch (cost to price); accept 4.0 (changes PR-007, Amish's call). Cost: none | Claude under Amish's standing instruction of 2026-10-23 (STEM fix after the independent review, S18) | BKH-STM-001; BKH-CAL-001 F; BKH-BLD-001 3.6, step 9 |
| 2026-10-25 | D-S7: in very soft beds (hand vane 5 to 10 kPa) the stake's top pin hole is not used; water deeper than 1.0 m at the stake takes the loop out, as for a flood. With the block on the top hole (1.2 m of water) the factor there was 1.91. Options weighed: the operating limit (chosen, no cost); a 4.0 m drive (offered to Amish as O-8, since 3.5 m was his decision 14A). Cost: none | Claude under Amish's standing instruction of 2026-10-23 (STEM fix after the independent review, S15) | BKH-STM-001; BKH-CAL-001 E; BKH-BLD-001 step 7 |
| 2026-10-25 | O-1: Concept selection: option A, the running rope loop (178 of 220, 16 % ahead of C) | Amish: "i concur with your recommendations" | BKH-DDR-004 v0.2; `project.yaml` `concept_chosen: "A"` |
| 2026-10-25 | O-2: Graft from option C: a smooth hardwood bank-edge board 250 x 600 x 25 mm set flush at the bank lip under both legs (BOM line 18, about USD 5, estimate), the pull measured with and without it in the R3 trial; a roller only if the board does not help | Amish: "i concur with your recommendations" | `cad/src/model.py` `_edge_board()`; BOM line 18; BKH-BLD-001 v0.4 section 3.8, step 10, first checks |
| 2026-10-25 | O-3: Fixes of options B (guy anchor, STEM B2) and C (balance, STEM C1): sized on paper only, implemented only if that option is chosen | Amish: "i concur with your recommendations" | BKH-STM-001 (B2, C1 stay as fails with a fix proposed in options not carried forward) |
| 2026-10-25 | O-4: Product render site: the site render on the bank (outdoor scene, mud, still water) as the hero, the studio render second, with the model lifted 560 mm so the photoreal ground is the lake bed | Amish: "i concur with your recommendations" | `cad/src/product_model.py` (no change) |
| 2026-10-25 | O-5: Duplicate record number: keep `0003-amish-requirement-decisions.md` as BKH-DDR-003 and mark `0003-requirement-decisions-round2.md` superseded | Amish: "i concur with your recommendations" | `docs/decisions/0003-requirement-decisions-round2.md` v0.2, status Superseded |
| 2026-10-25 | O-6: Block price: keep the indicative USD 22 a block (BOM line 8) and confirm it with a local rigging supplier | Amish: "i concur with your recommendations" | BOM line 8 (no change); BKH-MKT-001 |
| 2026-10-25 | O-7: Lifting the far stake in a boat: the lowering rope (the 10 m offcut of the loop coil through the top cross hole), two people, so no one holds the 33 kg stake at arm's length over the side; PR-014 at risk to met on paper | Amish: "i concur with your recommendations" | BKH-BLD-001 v0.4 step 6; BKH-PRS-001 v0.5 PR-014; BOM line 6 note |
| 2026-10-25 | O-8: Very soft beds: keep D-S7 (3.5 m drive, top pin hole not used), as Amish's decision 14A set | Amish: "i concur with your recommendations" | No change |
