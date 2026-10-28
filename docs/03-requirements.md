---
doc_id: BKH-PRS-001
title: BankHaul product requirements and specifications
project: BankHaul
doc_type: Product requirements and specifications
version: '0.5'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold (as BKH-REQ-001)
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 3; targets made measurable, R10 (weak link) and R11 (working distance) added, status from BKH-CAL-001
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: Amish's decisions 14A (far stake driven 3.5 m; R5 status) and 15A (R8 restated), BKH-DDR-003
- version: "0.4"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Kit 1.8: BKH-REQ-001 becomes BKH-PRS-001; R1 to R11 migrated to PR-001 to PR-011 with tolerance, units and the user requirement each traces to (BKH-URS-001); PR-012 to PR-016 added; PR-005 status from D-S2; PR-015 from D-S1"
- version: '0.5'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Amish''s decisions of 2026-10-25: PR-014 at risk to met on paper with the lowering rope (O-7); PR-003 note on the bank-edge board (O-2); concept A chosen (O-1)'
---

# BankHaul product requirements and specifications

What the station must do, each requirement traced to a user need in BKH-URS-001 (links in BKH-RTM-001). The requirements describe option A, the running rope loop, which is the current design; Amish chose it on 2026-10-25 (BKH-DDR-004). Status is from the calculation note BKH-CAL-001 v0.3 (`python docs/04-calcs/sizing.py`): **14 of the 16 are met on paper or by design (PR-014, the far stake as a team lift in a boat, since the lowering rope Amish decided on 2026-10-25); PR-008 (parts under USD 80 for a local-materials station) is not yet met on the first-order estimate, and PR-016 (authority agreement) is verified with the partner at TRL 4.** "On paper" means calculated, not yet tested. The targets remain proposals for review with a co-design partner, who is not yet agreed (BKH-DDR-001, item 10).

**Design case** used throughout: a 30 m by 2 m gillnet, 10 kg of catch and 5 kg of weed; 30 m between the blocks; water 1.0 m deep at the far stake; soft wet soil of 10 kPa undrained shear strength on the bank and soft (10 kPa) or very soft (5 kPa) mud in the bed.

Table 1. Product requirements and specifications. "Was" gives the number in BKH-REQ-001.

| ID | Was | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | R1 | UR-001, UR-013 | Safety | No one in the water | Setting, hauling, clearing and relocating shall need no one in the water once the far stake is set from a boat or at low water | 10 of 10 cycles from the bank | Pass or fail | cycles | Analysis of the build plan (TRL 3); field trial with partner fishers (TRL 4) | Met on paper |
| PR-002 | R2 | UR-005 | Performance | Working span | The station shall work at 30 m between the blocks, with rope for 50 m | 30; stretch 50 | min | m | Analysis, BKH-CAL-001 A; measured at the trial site (TRL 4) | Met on paper: rope bought for 50 m |
| PR-003 | R3 | UR-004 | Usability | Hand pull | The peak hand pull to haul a 30 m net with the design catch shall be under 250 N | 250 | max | N | Analysis, BKH-CAL-001 B; spring scale in trials (TRL 4) | Met on paper in still water: about 200 N (estimate); thin in a 0.3 m/s current (241 N) or on a stickier bank (243 N at friction 0.9); a smooth bank-edge board (BOM 18, O-2) is fitted and the R3 trial measures the pull with and without it |
| PR-004 | R4 | UR-008 | Physical architecture | Bank anchor holding | The bank station shall hold 3 kN horizontal at the near block in soft wet soil without visible movement, taken as a factor of 2 on the anchors' ultimate capacity | 3.0 at factor 2 | min | kN | Analysis, BKH-CAL-001 D; pull test on a CalRig-style rig (TRL 4) | Met on paper: anchor factor 2.13 at 10 kPa |
| PR-005 | R5 | UR-008 | Physical architecture | Far stake holding | The far stake shall hold 1.5 kN horizontal in soft and very soft mud with a factor of 2 on the lesser of the soil and stake capacities | 1.5 at factor 2 | min | kN | Analysis, BKH-CAL-001 E; pull test from the boat (TRL 4) | Met on paper: factor 2.77 at 10 kPa (stake yields first, D-S2), 2.03 at 5 kPa; at the top pin hole (1.2 m of water) 2.51 at 10 kPa, and the top hole is not used at 5 kPa (D-S7) |
| PR-006 | R6 | UR-007 | Usability | Cycle time | A full haul and reset of a 30 m net shall take under 10 minutes, without clearing fish | 10 | max | min | Analysis, BKH-CAL-001 G; timed trials (TRL 4) | Met on paper: about 6.3 minutes (estimate) |
| PR-007 | R7 | UR-009 | Materials | Season durability | Rope and blocks shall last one season (6 months) of daily use; rope factor 5 or more at the season's end | 6; factor 5 | min | months; ratio | Analysis, BKH-CAL-001 F; season pilot with an inspection log (TRL 5) | Met on paper (estimate): rope factor 5.7 after sun damage with both loop ends spliced (D-S6); UV loss, rope strength and bush wear plausible (STEM S18, S19, S22) |
| PR-008 | R8 | UR-011 | Cost | Cost per station (restated, decision 15A) | Parts under USD 80 per station for a local-materials station, costed from local prices with the co-design partner before the season pilot; the steel station built for the TRL 4 trials is costed and recorded but not held to this figure | 80 | max | USD | Bill of materials priced with the partner | **Not met**: local-materials station about USD 98 (first-order estimate); steel trial station USD 399, accepted for TRL 4 |
| PR-009 | R9 | UR-010 | Usability | Level change | The bank station shall be relocatable by two people in under 30 minutes as the shoreline moves; the far block shall follow the water level in 200 mm steps | 30; 200 | max | min; mm | Analysis, BKH-CAL-001 H; timed relocation (TRL 4) | Met on paper: about 22 minutes (estimate); five pin holes at 200 mm |
| PR-010 | R10 | UR-006 | Safety | Weak link | Each net bridle shall release between 500 and 700 N, so a net seized by an animal or snag cannot load the loop, stake or fisher beyond that | 600 | plus or minus 100 | N | Analysis, BKH-CAL-001 C; pull three samples of each cord batch (TRL 4) | Met on paper; cord chosen by test when bought (STEM S6) |
| PR-011 | R11 | UR-003 | Safety | Working distance | The fisher's working spot shall be at least 5 m from the water's edge at the day's level | 5 | min | m | Inspection of the layout (TRL 3); measured at the trial site (TRL 4) | Met by layout: 5.0 m, as the Be Crocwise advice asks (STEM S24) |
| PR-012 | | UR-002 | Performance | Own nets | The station shall set and haul the fisher's own gillnet, up to the span less 2 m long, with a bridle tied to each end | 28 | max | m of net | Inspection of the model and build plan (TRL 3); trials with partner nets (TRL 4) | Met by design |
| PR-013 | | UR-012 | Physical architecture | Local making | Every made part shall be cut, drilled and welded from tube, plate and bar, sawn and screwed from timber, or spliced from rope; bought parts shall be commodity rigging | No machining | Pass or fail | n/a | Inspection of the BOM and build plan (TRL 3) | Met by design |
| PR-014 | | UR-013 | Usability | Two-person lift | No part handled on site shall weigh more than 25 kg per person carrying it | 25 | max | kg per person | Analysis, BKH-CAL-001 J | Met on paper with the lowering rope (BKH-DEC-001 O-7, decided by Amish 2026-10-25): far stake 33.2 kg, two people, 16.6 kg each; the stake is stood up against the boat side and let down on a rope through its top cross hole, so no one holds it at arm's length over the side; to confirm in the TRL 4 drill |
| PR-015 | | UR-008 | Physical architecture | Pin plates | The pad eye, stay lugs and collar lug shall meet the pin-plate geometry of EN 1993-1-8 Table 3.9 at 1.5 times their working load | 1.0 | min | ratio | Analysis, BKH-CAL-001 D | Met on paper: least ratio 1.15 (pad eye, D-S1) |
| PR-016 | | UR-014 | Regulatory | Authority agreement | The siting and use of each station shall be agreed with the local wildlife and fisheries authorities before it is installed | Written agreement | Pass or fail | n/a | Demonstration with the co-design partner (TRL 4) | To verify at TRL 4 |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software, cost, regulatory. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Restated by Amish's decisions

- **PR-008, was R8 (decision 15A, 2026-10-03).** Amish: "i agree with all the 46 recommendations you provided. please proceed." The steel station is built for the TRL 4 trials, so they test the method with parts of known strength, and a local-materials station is costed with the co-design partner. R8 was "Parts under USD 80 per station"; it now applies the USD 80 figure to the local-materials station costed from local prices, and records the steel trial station's cost without holding it to that figure.
- **PR-005, was R5 (decision 14A, 2026-10-03).** The target is unchanged; the far stake is driven 3.5 m, so it is met on paper in very soft mud as well as soft mud. The tolerance now names the lesser of the soil and stake capacities (D-S2, under Amish's standing instruction of 2026-10-23).

## Assumptions

- Fishers can shift from wading-set nets to loop-set nets without losing much catch (STEM S26, plausible).
- Most attack hotspots have banks where a screw anchor can hold (soft wet soil of about 10 kPa undrained shear strength or firmer).
- A boat or low-water window exists to place the far stake once per season.
- Nets can be fitted with a bridle at each end to clip to the loop and the bank post.
- Steel S235 for plates, S355 for the stake tube; polyester stays of 15.6 kN (1,590 kg, D-S5) and polysteel loop rope of 20 kN minimum breaking strength, to confirm when bought (BKH-DEC-001, to confirm).
- Still to slow water: the design current is 0.3 m/s; a clean net releases its weak link at about 0.76 m/s (BKH-CAL-001 C).
- In very soft beds the water at the stake is no more than 1.0 m deep while fishing (D-S7).

> **Safety:** PR-001, PR-010 and PR-011 are safety requirements. They keep the fisher out of the water and back from its edge, and limit what a seized net can do. None makes it safe to stand at the water's edge.
