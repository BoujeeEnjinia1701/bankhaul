---
doc_id: BKH-CAL-001
title: BankHaul sizing calculations
project: BankHaul
doc_type: Calculation
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First sizing note at TRL 3 for the constructable design (BKH-DDR-002)
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: Amish's decisions 14A and 15A (BKH-DDR-003); far stake driven 3.5 m (R5 met in very soft mud); R8 restated; cost and mass updated
---

# BankHaul sizing calculations

The constructable design meets ten of the eleven requirements on paper. Amish decided both open items on 2026-10-03 (Amish, 2026-10-03: "i agree with all the 46 recommendations you provided. please proceed."): the far stake is now driven 3.5 m (decision 14A), so R5 is met in very soft mud at a factor of 2.03; and R8 is restated (decision 15A): the steel station is built for the TRL 4 trials at USD 394 in parts, and the under USD 80 figure applies to a local-materials station costed with the co-design partner, estimated here at USD 98 and so not yet met. Every figure below is produced by `docs/04-calcs/sizing.py` from the parameters in `cad/src/model.py`; `docs/04-calcs/results.csv` holds the results table. Values marked "estimate" are first-order and are checked by test at TRL 4.

> **Safety:** These calculations size a rope system that works under load beside crocodile water. They are first-order and are not a substitute for proof-load tests on the anchors, stake, rope splices and weak links before the station is used.

## Results against requirements

Table 1. Results against every requirement

| ID | Target | Result | Status | Section |
| --- | --- | --- | --- | --- |
| R1 | Set and haul with nobody in the water | No step needs anyone in the water once the far stake is set from a boat | Met on paper; field trial at TRL 4 | J |
| R2 | At least 30 m between pulleys; stretch 50 m | 30 m design case; rope bought for 50 m | Met on paper | A |
| R3 | Peak pull under 250 N | 200 N (estimate) | Met on paper | B |
| R4 | Holds 3 kN in soft wet soil without movement | Anchor factor 2.13 at 10 kPa | Met on paper; pull test at TRL 4 | D |
| R5 | Holds 1.5 kN horizontal in soft mud | Factor 4.05 at 10 kPa; 2.03 at 5 kPa (3.5 m embedded) | Met on paper in soft and very soft mud; pull test at TRL 4 | E |
| R6 | Full haul and reset under 10 min | 6.3 min (estimate, without clearing fish) | Met on paper (estimate) | G |
| R7 | One season without rope or pulley failure | Rope factor 5.7 after sun damage | Met on paper (estimate) | F |
| R8 | Local-materials station parts under USD 80, costed with the partner; steel trial station recorded (restated, decision 15A) | Steel trial station USD 394; local-materials station about USD 98 (estimate) | Steel trial station accepted for TRL 4; **local-materials figure not yet met** (estimate), to be costed with the partner | I |
| R9 | Relocated by two people in under 30 min | 22 min (estimate) | Met on paper (estimate) | H |
| R10 | Weak link releases 500 to 700 N | 510 to 690 N | Met on paper; calibrate at TRL 4 | C |
| R11 | Working spot at least 5 m from the water | 5.0 m | Met by layout | J |

## A. Loop and rope

Assumptions: 12 mm floating polypropylene and polyethylene blend rope ("polysteel"), 20 kN minimum breaking strength, 0.068 kg/m, density about 0.93; blocks with 100 mm sheaves, so the rope centre runs on a 56 mm radius.

- Loop length for the 30 m design span: 2 x 30 + 2 x pi x 0.056 = **60.4 m**; for the 50 m stretch span, 100.4 m.
- Rope bought: 120 m, cut into two halves of 55 m (each 5 m longer than the 50 m span for splices and knots), leaving 10 m spare. The surplus of each half is coiled at its ring, which never passes a block.
- The loop for 30 m weighs 4.1 kg and floats.
- Sheave to rope diameter ratio: 100 / 12 = **8.3**, at the usual minimum of 8 for fibre rope.

## B. Hand pull to haul a 30 m net with catch (R3), estimate

Assumptions: a 30 m by 2 m gillnet with a 0.06 kg/m lead line, 1.2 kg of twine and a 0.03 kg/m float line; the wet net is 1.6 times its dry mass; 10 kg of catch and 5 kg of weed or debris; friction 0.6 on the bed and the wet bank; hauling at 0.4 m/s; the bank edge rises 0.5 m over 1 m (27 degrees); the fisher stacks the net on the table as it arrives, so about a fifth of the net is on the bank edge at once.

| Load | Value | Basis |
| --- | --- | --- |
| Lead line friction on the bed | 9.7 N | Submerged weight of the lead line x 0.6 |
| Drag of the bunched net and catch | 40.0 N | 0.5 x 1,000 x 0.4² x 0.5 m² |
| Catch, weed and a fifth of the net up the bank edge | 156.8 N | 15.9 kg x 9.81 x (0.6 cos 27° + sin 27°) |
| Loop following round both blocks | 18.3 N | Rope friction on the ground, block efficiency 0.95 each |
| **Peak hand pull** | **200 N** | Bank edge load, half the water loads, loop |

The peak comes at the instant the whole catch is on the bank edge. Hauling is done by the net's near end, so the loop only follows. Setting the net takes about **43 N** at 0.5 m/s.

## C. Weak link (R10) and design loads

The weak link sets the largest load a seized or snagged net can put into the system.

- Release: nominal **600 N**, plus or minus 15 % (510 to 690 N). The cord is chosen by pulling three samples from the batch bought.
- The largest load in normal use is during setting, **62 N**, so the lowest release is **8.3 times** the normal load: no nuisance breaks.
- Far end design load: both legs at the highest release, **1.38 kN**, within the 1.5 kN of R5.
- Bank design load: **3.0 kN** (R4) horizontal at the near block. It covers twice the link release, debris on the loop and a jammed cleat.

## D. Bank post, stays and screw anchors (R4)

Assumptions: soft wet soil with an undrained shear strength of 10 kPa; anchors with a single 250 mm helix on a 1.6 m rod, set in line with the stay; capacity Q = Fc x su x A with Fc = 9 for a deep helix (depth to helix diameter 3.6, at the critical depth for this soil).

| Quantity | Value | Note |
| --- | --- | --- |
| Stay length, lug hole to anchor eye | 1.44 m | Anchor eyes 1,100 mm behind and 450 mm either side |
| Stay elevation | 38.7° | |
| Stay tension at 3 kN | **2,076 N** each | Both stays share the pull along the line |
| Stay rope factor | 9.0 | 10 mm polyester, 22 kN, 85 % at the eye splice |
| Post compression | 2,595 N | Buckling factor 93 (48.3 x 3.2 tube, 1.0 m, pinned) |
| Foot plate bearing | 22.6 kPa | Factor 2.3 on 5.14 x su |
| Helix depth | 0.89 m | |
| Anchor capacity | **4,418 N** each | Factor **2.13** on the stay tension |
| Pad eye shear | 33.6 MPa | Block load 6 kN, two shear planes |
| Block working load factor | 1.67 | 500 kg block, two legs at 1.5 kN |

A factor of 2 or more on the anchor's ultimate capacity is taken as "no visible movement", since helical anchors creep noticeably above about half their ultimate load. R4 is met on paper; the TRL 4 pull test on a CalRig-style rig settles it.

## E. Far stake lateral capacity (R5)

Method: Broms' short free-head pile in cohesive soil. The load acts 1.2 m above the bed (1.0 m of water plus 0.2 m to the far block). The stake is a 76.1 x 3.6 mm S355 tube, 5.0 m long, embedded 3.5 m (decision 14A, BKH-DDR-003; Amish, 2026-10-03: "i agree with all the 46 recommendations you provided. please proceed.").

| Bed | Undrained shear strength | Ultimate lateral load | Factor on 1.5 kN | Bending stress at 1.5 kN |
| --- | --- | --- | --- | --- |
| Soft mud | 10 kPa | 6,079 N | **4.05** | 150 MPa (factor 2.4 on S355) |
| Very soft mud | 5 kPa | 3,040 N | **2.03** | 162 MPa (factor 2.2 on S355) |

A 60.3 mm stake would carry the load in soft mud but reach about 250 MPa at 1.5 kN, too close to yield; the 76.1 mm tube was chosen for strength (BKH-DDR-002, item 6). The bending stress at the R5 load does not change with embedment, since the largest moment lies within about 0.6 m of the bed.

At the first TRL 3 embedment of 2.5 m the factor in very soft mud was **1.23**, so R5 was at risk there. Driving the stake 1.0 m deeper raises it to **2.03**: R5 is now **met on paper in soft and very soft mud**. The stake is 1.0 m longer, 6.4 kg heavier (33.2 kg) and USD 12 dearer. The TRL 4 pull test from the boat settles it.

## F. Loop rope strength and durability (R7)

- The largest leg tension is the larger of the link's highest release and half the bank load: 1.5 kN. The new rope through a splice (85 %) has a factor of **11.3** on it.
- Assuming the rope loses half its strength to sun over a tropical season, the factor at the end of the season is **5.7**.
- Two set and haul cycles a day for 180 days give about 720 passes over each sheave, far below the bending fatigue life of fibre rope at a sheave ratio of 8.
- Blocks with bushed nylon sheaves in silty water are the less certain part; the season pilot at TRL 4 records bush wear.

R7 is met on paper as an estimate.

## G. Cycle time (R6), estimate

Haul at 0.25 m/s with stacking (2.0 min), unclip (1.0 min), re-clip (1.0 min), set 30 m at 0.4 m/s (1.3 min), cleat and tie off (1.0 min): **6.3 minutes**. Clearing a 10 kg catch of about 30 fish at 20 s each takes a further 10 minutes, as it does today; the loop does not change it, so it is outside this figure.

## H. Relocation (R9), estimate

Two people: unscrew both anchors (4 min), lift out the post and spike (2), carry up to 50 m (3), set out the new spot (3), screw in both anchors (6), stand the post and tension the stays (4): **22 minutes**. Re-tying both ring knots for the new loop length takes about 6 minutes more and is outside R9, which covers the bank anchor.

## I. Cost per station (R8) and value engineering

The station parts in `bom/bom.csv` cost **USD 394** (the 5.0 m far stake adds USD 12); with the stake driving cap, the prototype costs USD 404. Value-engineering target: USD 1,800. Estimated cost of the constructable design: USD 404 (USD 1,396 under the target).

The largest cost drivers are the two screw anchors (USD 76), the far stake (USD 60), the rope (USD 54), the two blocks (USD 44), the table (USD 35) and the post (USD 32).

R8 is restated (decision 15A, BKH-DDR-003; Amish, 2026-10-03: "i agree with all the 46 recommendations you provided. please proceed."). The steel station is built for the TRL 4 trials, so the trials test the method with parts of known strength; its USD 394 is recorded, not held to the R8 figure. The USD 80 figure applies to a local-materials station, costed from local prices with the co-design partner before the season pilot. The first-order estimate of that station (hardwood post with bolted fittings, buried timber deadman, hardwood far pole, two hand-made hardwood sheaves on steel pins, rope for a 30 m span only, galvanised rings, hardwood cleats, a pole table) is about **USD 98**, so the restated R8 is **not yet met** on this estimate. For reference, one bank post and table serving three loops would cost about USD 269 per loop.

## J. Layout and masses

- The post stands 6 m back from the water's edge and the fisher works within 1 m of it: **5.0 m** from the water (R11).
- Once the far stake is set from a boat or at low water, setting, hauling, clearing and relocating the bank station are all done from the bank (R1).
- Masses: bank post weldment 17.2 kg, far stake 33.2 kg, two screw anchors 14.3 kg, clearing table 26.4 kg, swivel collar 1.6 kg, two blocks 2.2 kg, rope 7.5 kg, small parts about 4 kg: about **106 kg** for the station. The heaviest part is the far stake, handled by two people from a boat.
