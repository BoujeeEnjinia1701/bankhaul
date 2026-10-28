---
doc_id: BKH-RSK-001
title: BankHaul risk register and hazard analysis
project: BankHaul
doc_type: Risk register and hazard analysis
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First risk register, preliminary hazard analysis (stage P1) and first-pass design FMEA (stage P3) for option A (kit 1.8 upgrade)
- version: '0.2'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'H6 controls as decided by Amish (O-2 board, O-7 lowering rope), 2026-10-25'
---

# BankHaul risk register and hazard analysis

The top project risk is that no co-design partner and trial site are found, so the soil, the nets and the users' pull all stay assumptions. The top hazard is a crocodile attack on someone at the water's edge, above all while the far stake is placed; the station reduces time in the water but cannot protect anyone who is at the edge. The highest design FMEA scores are a weak link replaced with stronger cord (RPN 60) and the far stake leaning over in a bed softer than assumed (RPN 48). Method: STANDARDS section 23 and ISO 12100. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection 1 (certain to be caught) to 5 (unlikely to be caught).

> **Safety:** BankHaul is a rope system worked beside crocodile water. It does not protect anyone from a crocodile that leaves the water. Every control below assumes the local wildlife authority's advice is followed.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | No co-design partner or trial site | Candidate not yet approached (BKH-DDR-001, item 10) | Requirements, soils and nets stay desk assumptions; no TRL 4 | 3 | 5 | Amish | Approach the Lake Kariba research group and an inshore cooperative before TRL 4 |
| P2 | Fishing rules do not allow a fixed set line | Gear or zoning rules (BKH-REG-001 G1) | Stations cannot be sited where attacks happen | 2 | 5 | Partner | Ask the fisheries authority before siting (PR-016) |
| P3 | Fishers do not adopt the loop | Catch, habit, shared stations (STEM S26) | No safety benefit | 3 | 4 | Partner | Co-design with fishers; trial both shared and household stations |
| P4 | Local-materials station costs more than USD 80 | Rated rigging and rope prices (PR-008) | The station is out of reach for households | 3 | 3 | Partner | Cost it locally; share a bank post between loops (USD 269 a loop) |
| P5 | Parts stolen | Steel and rope have resale value | Station out of use | 3 | 3 | Association | Remove the loop when not fishing; mark parts; community ownership |
| P6 | Bed softer than 5 kPa at the site | Silt and organic mud (STEM S15) | Far stake cannot hold the design load | 3 | 4 | Partner | Hand vane from the boat before siting (BKH-DEC-001 item 7) |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Crocodile attack while placing the far stake | Working on or near the water from a boat or a dry bed | Death or serious injury | 5 | 2 | Boat on two anchors or a dry bed at low water; two people and a lookout; wildlife authority's advice; never wade (BKH-BLD-001 step 6) | 3 |
| H2 | Crocodile attack at the bank | Fisher near the edge at night or dawn | Death or serious injury | 5 | 2 | Working spot 5 m back (PR-011); hauling from the table; the station never asks anyone to the edge | 3 |
| H3 | Fisher pulled toward the water | A crocodile or snag takes the net | Dragged in | 5 | 2 | Weak links release at 500 to 700 N (PR-010); never tie the loop or net to the body; let go | 2 |
| H4 | Rope or stay snap-back | Overload, cut or worn rope, failed splice | Struck by the rope or a shackle | 4 | 2 | Factors of 9 (stays) and 11 (loop); nobody in the bight of the loop or in line with a loaded stay; inspect before each use | 2 |
| H5 | Hand caught in a block or cleat | Hand near the sheave while hauling | Crushed or burnt fingers | 3 | 2 | Haul by the net's near end, not the loop; hands at least 0.5 m from the blocks | 1 |
| H6 | Back strain | 200 N peak pull; 33 kg stake | Injury | 3 | 3 | Peak only at the bank edge, over the smooth bank-edge board (O-2, decided 2026-10-25); the stake let down on a lowering rope by two people, not held at arm's length (O-7, decided 2026-10-25) | 2 |
| H7 | Drowning | Working from a boat; falling in during installation | Death | 5 | 2 | Life jackets; two people; installation in daylight (BKH-REG-001 G12) | 2 |
| H8 | Boat, swimmer or floating debris caught on the loop | A floating line across the water; the weak links do not limit a load on the loop itself | Capsize, entanglement; the stake or bank station loaded beyond design | 4 | 2 | Mark the loop and stake; take the loop out when not fishing and before floods; inspect after any hard pull | 2 |
| H10 | Someone goes to the water to recover a released net or free a fouled far block | The weak link released, or the loop jammed at the far block | Exposure to crocodiles while wading or reaching from a boat | 5 | 3 | Recover only from a boat with two people and a lookout, by daylight; otherwise abandon the net; never wade (BKH-BLD-001 safety stops) | 3 |
| H11 | Crocodile or hippo strikes the floating loop or the stake | Animals in the water at the station | Loop or stake overloaded; a person near the bank pulled | 4 | 2 | Nobody holds the loop while it is loaded by something unseen; let go; inspect the stake and anchors afterwards | 2 |
| H9 | Welding burns and fumes | Building the post, stake and collar | Burns, eye injury | 3 | 3 | Competent welder, PPE, ventilation | 1 |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Weak link (BOM 7) | Limit the pull of a seized net | Replaced with stronger cord | A seized net can pull the station or the fisher | Nuisance breaks; wrong cord | 5 | 3 | 4 | 60 | Paint the link; batch test (BKH-BLD-001 3.7); spare links in the kit |
| F2 | Far stake (BOM 2) | Hold the far block | Leans over or pulls out | Loop slackens; net lost | Bed softer than 5 kPa; the top pin hole used in a very soft bed (D-S7); scour round the stake; a firm layer stops driving short of 3.5 m | 4 | 3 | 4 | 48 | Hand vane and probe before driving (BKH-DEC-001 items 7, 12); a stake stopped short of 3.5 m gets a new check before use; check the lean each season |
| F3 | Screw anchors (BOM 11) | Hold the stays | Creep under sustained load | Post leans toward the water | Factor near 2 in soft soil | 3 | 3 | 3 | 27 | Pull test at TRL 4 (PR-004); re-tension the turnbuckles; inspect each week |
| F4 | Loop rope (BOM 6) | Carry the net | UV loss and abrasion | Rope breaks under load | Sun over a season (STEM S19) | 4 | 2 | 3 | 24 | Inspect before each use; replace after a season or at the first fuzzing |
| F5 | Block bushes (BOM 8) | Let the sheave turn | Wear in silty water | Sheave wobbles, rope rubs a cheek | Silt (STEM S22) | 3 | 3 | 3 | 27 | Record wear in the season pilot; spare blocks |
| F6 | Stop pin (BOM 14) | Hold the collar | Nut works loose, pin lost | Collar slides down the stake | Vibration, corrosion | 3 | 2 | 3 | 18 | Nyloc nut; spare pin; inspect from the boat each season |
| F7 | Stays and turnbuckles (BOM 5, 12) | Hold the post | Turnbuckle unwinds | Post leans | Vibration of the loop | 3 | 2 | 2 | 12 | Wire the turnbuckles after tensioning |
| F8 | Swivel rings (BOM 9) | Join the halves; act as stops | Ring reaches a block | Loop jams | Net longer than the span less 2 m | 2 | 2 | 2 | 8 | Net length rule in the build plan (PR-012) |

## Sources

- Matanzima, Marowa and Nhiwatiwa, *Oryx* (attack activity and timing), as cited in BKH-PRB-001.
- Northern Territory Government, Be Crocwise, fishing and boating advice (checked 2026-10-25).
- BKH-CAL-001 for the loads, factors and masses quoted.
