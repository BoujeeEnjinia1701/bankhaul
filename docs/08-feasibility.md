---
doc_id: BKH-FEA-001
title: BankHaul feasibility assessment
project: BankHaul
doc_type: Feasibility
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First assessment, closed at TRL 3 from BKH-CAL-001 v0.3, the STEM check and the D3 model (kit 1.8 upgrade)
- version: '0.2'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Station USD 399 with the bank-edge board; O-6 decided (2026-10-25)'
---

# BankHaul feasibility assessment

**Closed at TRL 3: feasible.** The calculations (BKH-CAL-001) show the loop sets and hauls a 30 m gillnet at about 200 N with the bank station and far stake at a factor of about 2 in soft ground, and the D3 model shows every part fits (`cad/fidelity.json`). What remains unproven is the ground, the people and the season, not the physics: the bed and bank strength at a real site, the pull the users can give, the weak link's scatter, driving the stake, and UV and bush wear (BKH-STM-001 S4, S6, S17, S19, S22). Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | A slack floating loop on two blocks; peak pull about 200 N; far end at most 1.4 kN through the weak links; bank 3 kN | High | Factors near 2 on the soil (anchors 2.13, stake 2.03 in very soft mud); a softer bed needs a new check | BKH-STM-001 S2 to S16; BKH-CAL-001 B to E |
| Materials | Painted steel tube and plate, galvanised rigging, polyester and polysteel rope, timber | Medium | UV loss of the loop rope over a season; corrosion of the stake at the waterline; grades to confirm | BKH-STM-001 S19, S23; BKH-DEC-001 items 5, 11 |
| Manufacturing and assembly | Saw, drill, MIG or stick welder for 3 to 8 mm steel, carpentry and eye splicing; 11 assembly steps | High | Squareness of the post and the stake's straightness; splicing skill | BKH-BLD-001; PR-013 |
| Power and controls | None; hand-worked | High | None | |
| Supply of parts | Tube, plate and timber locally; blocks, shackles, turnbuckles, anchors and rope from rigging and fencing suppliers; USD 399 in parts | Medium | Rated rigging may be scarce near the sites; the block price may be low; kept as indicative and to confirm with a local rigging supplier (BKH-DEC-001 O-6, decided 2026-10-25) | bom/bom.csv; BKH-MKT-001 |
| Site and installation | A bank of soft wet soil 6 m or more deep from the edge; a bed of 5 kPa or firmer; a boat or low water to drive the stake | Medium | Bed strength and layering unknown at every site; placing the stake is the most exposed job | BKH-STM-001 S17; BKH-RSK-001 H1 |
| Users | One person hauls; two lift the stake | Medium | Pull strength of the users and their acceptance of loop-set nets not yet known | BKH-STM-001 S4, S26 |

Ratings: High, Medium, Low.
