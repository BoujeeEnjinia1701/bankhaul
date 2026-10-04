---
doc_id: BKH-DDR-003
title: BankHaul requirement decisions, round 2
project: BankHaul
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: R5 (far stake in very soft mud) and R8 (cost per station) decided by Amish on 2026-10-03, both as recommended
---

# 0003: Requirement decisions, round 2

- **Date:** 2026-10-03
- **Status:** decided. Decided by Amish Chadha, 2026-10-03: "i approve all of the 47 recommendations provided by you. Execute them." Both decisions below were the recommended options in `docs/REVIEW.md` (TRL 3, Decisions for Amish) and in the design decisions register, taken exactly as worded there.

## Context

At TRL 3 (BKH-CAL-001 v0.1) two requirements were not met or at risk on paper. R5 (far stake holding) was met in soft mud but at risk in very soft mud: in a bed of about 5 kPa the 76.1 mm stake driven 2.5 m holds an ultimate 1,845 N, a factor of 1.23 on the 1.5 kN load, against the factor of 2 used as "holds", because lateral capacity in clay falls with its strength and the load acts 1.2 m above the bed. R8 (parts under USD 80 per station) was not met: the constructable station costs USD 382, driven by bought rated hardware and the steel stake and post.

> **Safety:** Neither decision relaxes a safety provision. The long stake is heavier (33.2 kg) and is handled by two people from a boat held on two anchors, with a lookout, as before; the hand vane reading of the bed is taken under the same rules. The steel trial station keeps the rated rigging that carries the safety case.

## Options considered

*Table 1. Options for each decision.*

| Requirement | A | B | C |
| --- | --- | --- | --- |
| R5, far stake holding in very soft mud | Drive 3.5 m into very soft beds (5.0 m stake): factor 2.03, met, about USD 12 more per stake and 6.4 kg more (33 kg stake) | Two stakes 1 m apart tied at the top with a bar carrying the collar: factor 2.21, met, about USD 56 more and about 28 kg more, two to drive from the boat | Keep 2.5 m and site stations only where a hand vane shows 10 kPa or more: factor 2.46 where used, very soft beds excluded, no cost or mass |
| R8, cost per station | Build this steel station for the TRL 4 trials and cost a local-materials station with the co-design partner before the season pilot: R8 not met for the trial station, USD 382 now, about 100 kg | Switch the prototype now to local materials: about USD 98, not met but close, about 30 kg more, R7 and R9 at risk | One bank post and table serve three loops at a landing site: about USD 257 per loop, not met, about 60 kg per loop |

## Decision

*Table 2. Decisions taken.*

| # | Requirement | Option chosen | Effect | Condition |
| --- | --- | --- | --- | --- |
| 5 | R5, far stake holding in very soft mud | A: drive 3.5 m into very soft beds with a 5.0 m stake | Factor 2.03 at 5 kPa (ultimate 3,040 N), 2.46 at 10 kPa with the standard 2.5 m: R5 met on paper. Long stake 33.2 kg (26.8 kg standard), about USD 12 more; station USD 394 at a very soft site. Bending stress unchanged (162 MPa, factor 2.2 on S355) | The extra 1 m is cut only where a hand vane test of the bed, from the boat down to 2.5 m, reads under 10 kPa. It gives a factor of 2 only down to 4.9 kPa; weaker beds are a new open question |
| 6 | R8, cost per station | A: build the steel station for the TRL 4 trials; cost a local-materials station with the co-design partner before the season pilot | R8 not met for the trial station (USD 382, or USD 394 with the long stake; about 100 kg). No change to the design or the bill of materials | The local-materials costing, from local prices with the co-design partner, is made before the season pilot and gives the real R8 figure |

## Consequences

- `cad/src/model.py`: `embed_vsoft` (3,500 mm) and `su_vane_min` (10 kPa) added, with the derived length of the long stake (5,000 mm). The model and the STEP files still show the 2.5 m design case, so they were not re-exported.
- `cad/src/sheets.py`: far end general arrangement BKH-DWG-002 to Rev P3 with the long stake note; `cad/src/build_plan_media.py`: making sketch BKH-DWG-102 with the long stake's cut length and paint ring.
- `docs/04-calcs/sizing.py` and `results.csv` (BKH-CAL-001 v0.2): R5 met on paper; the weakest bed covered (4.9 kPa); station cost and heaviest lift for the long stake; R8 restated as not met for the trial station.
- `bom/bom.csv`: line 2 note gives the long stake's cut length, mass and extra cost; the costed station stays the standard one (USD 382).
- Build plan BKH-BLD-001 v0.2: hand vane reading of the bed before the stake is cut, the long stake's cut length and paint ring, and the vane reading added to the safety stop before driving.
- `docs/03-requirements.md` v0.3: R5 and R8 status updated; no target restated.
