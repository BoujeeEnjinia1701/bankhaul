---
doc_id: BKH-REQ-001
title: BankHaul requirements
project: BankHaul
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 3; targets made measurable, R10 (weak link) and R11 (working distance) added, status from BKH-CAL-001
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: R5 and R8 status after Amish's round 2 decisions (BKH-DDR-003); targets unchanged
---

# BankHaul requirements

Measurable requirements for the first prototype station. Each status comes from the calculation note BKH-CAL-001 (`docs/04-calcs/01-sizing.md`); "on paper" means calculated, not yet tested. R10 and R11 were added at the TRL 2 review (BKH-DDR-001, items 3 and 4).

Table 1. Requirements

| ID | Requirement | Target | Verification (TRL 4 or later) | Status at TRL 3 |
| --- | --- | --- | --- | --- |
| R1 | Set and haul a gillnet with nobody entering the water | 10 of 10 set and haul cycles completed from the bank | Field trial with partner fishers | Met on paper: once the far stake is set from a boat, no step needs anyone in the water |
| R2 | Working span | At least 30 m (98 ft) between pulleys; stretch goal 50 m (164 ft) | Measured at the trial site | Met on paper: 30 m design case; rope bought for 50 m |
| R3 | Hand pull force | Peak pull under 250 N (56 lbf) to haul a 30 m net with catch | Spring scale or load cell during trials | Met on paper: about 200 N (estimate) |
| R4 | Bank anchor holding | Holds at least 3 kN (675 lbf) in soft wet soil without visible movement | Pull-out test on a CalRig-style rig | Met on paper: screw anchors at factor 2.1 on capacity in soil of 10 kPa shear strength |
| R5 | Offshore stake or float holding | Holds at least 1.5 kN (337 lbf) horizontal load in soft mud | Pull-out tests in a representative bed | Met on paper: factor 2.5 in soft mud with the stake driven 2.5 m; factor 2.0 in very soft mud (5 kPa) with a 5.0 m stake driven 3.5 m wherever a hand vane reads under 10 kPa (BKH-CAL-001, E; BKH-DDR-003) |
| R6 | Cycle time | Full haul and reset under 10 minutes for a 30 m net | Timed trials | Met on paper: about 6 minutes (estimate, without clearing fish) |
| R7 | Durability | One fishing season (6 months) of daily use without rope or pulley failure | Season-long pilot with inspection log | Met on paper (estimate): rope factor 5.7 after sun damage |
| R8 | Cost | Parts under USD 80 per station | Costed bill of materials from local prices | Not met for the steel trial station: USD 382 (USD 394 with the long stake); a local-materials station is costed with the co-design partner before the season pilot (BKH-DDR-003) |
| R9 | Level change | Bank anchor relocatable by two people in under 30 minutes as the shoreline moves | Timed relocation | Met on paper: about 22 minutes (estimate) |
| R10 | Weak link | The net's bridle releases between 500 and 700 N, so a net seized by an animal or snag cannot load the loop, stake or fisher beyond that | Pull three samples of each cord batch to release | Met on paper; cord chosen by test when parts are bought |
| R11 | Working distance | The fisher's working spot is at least 5 m (16 ft) from the water's edge at the day's level | Measured at the trial site | Met by layout: 5.0 m |

## Assumptions

- Fishers can shift from wading-set nets to loop-set nets without losing much catch.
- Most attack hotspots have banks where a screw anchor can hold (soft wet soil of about 10 kPa undrained shear strength or firmer).
- A boat or low-water window exists to place the far stake once per season.
- Nets can be fitted with a bridle at each end to clip to the loop and the bank post.
- Design case: a 30 m by 2 m gillnet, 10 kg of catch and 5 kg of weed; water 1.0 m deep at the far stake.

> **Safety:** R10 and R11 are safety requirements. They limit what a seized net can do to the fisher and keep the fisher back from the water. Neither makes it safe to stand at the water's edge.
