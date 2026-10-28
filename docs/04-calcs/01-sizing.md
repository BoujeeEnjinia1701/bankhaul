---
doc_id: BKH-CAL-001
title: BankHaul sizing calculations
project: BankHaul
doc_type: Calculation
version: '0.4'
status: Draft
date: '2026-10-25'
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
- version: "0.3"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Kit 1.8 and 1.9 upgrade: requirements renumbered PR-001 to PR-016 (BKH-PRS-001); STEM fixes D-S1 (pad eye end distance, EN 1993-1-8), D-S2 (stake capacity is the lesser of the short and long pile), D-S3 (stay length), and after the independent review D-S5 (stay rope rated 15.6 kN), D-S6 (both loop ends spliced), D-S7 (top pin hole not used in very soft beds); sensitivities; masses from the D3 model"
- version: '0.4'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Amish''s decisions of 2026-10-25: PR-014 met on paper with the lowering rope (O-7); bank-edge board (O-2) adds USD 5, station USD 399, prototype USD 409, USD 274 a loop with a shared post'
---

# BankHaul sizing calculations

Kit 1.8 and 1.9 upgrade (2026-10-25): the requirements are now product requirements PR-001 to PR-016 in BKH-PRS-001 (R1 to R11 became PR-001 to PR-011); three STEM fixes changed this note under Amish's standing instruction of 2026-10-23 (BKH-DEC-001): the pad eye is 4 mm longer to meet the pin-plate end distance of EN 1993-1-8 (D-S1, section D); the far stake's capacity is the lesser of Broms' short-pile and long-pile cases, so it is 4.2 kN in soft mud, not 6.1 kN, and R5 is still met (D-S2, section E); and the back-stays are 1,110 mm between thimbles so the stay chain fits (D-S3, section D). The independent review (BKH-STM-001, Table 3) led to three more: the stays' rope is rated 15.6 kN, not 22 kN (D-S5, factor 6.4); both ends of each loop half are spliced, since a hitch kept only about 60 % of the rope's strength (D-S6, section F); and the top pin hole is not used in very soft beds, where 1.2 m of water would drop the stake's factor to 1.91 (D-S7, section E). Thirteen of the sixteen product requirements are met on paper or by design; PR-014 (team lift of the far stake) is at risk, PR-008 (cost of a local-materials station) is not yet met, and PR-016 (authority agreement) is verified at TRL 4.

The constructable design meets ten of the eleven original requirements on paper. Amish decided both open items on 2026-10-03 (Amish, 2026-10-03: "i agree with all the 46 recommendations you provided. please proceed."): the far stake is now driven 3.5 m (decision 14A), so R5 is met in very soft mud at a factor of 2.03; and R8 is restated (decision 15A): the steel station is built for the TRL 4 trials at USD 399 in parts, and the under USD 80 figure applies to a local-materials station costed with the co-design partner, estimated here at USD 98 and so not yet met. Every figure below is produced by `docs/04-calcs/sizing.py` from the parameters in `cad/src/model.py`; `docs/04-calcs/results.csv` holds the results table. Values marked "estimate" are first-order and are checked by test at TRL 4.

> **Safety:** These calculations size a rope system that works under load beside crocodile water. They are first-order and are not a substitute for proof-load tests on the anchors, stake, rope splices and weak links before the station is used.

## Results against requirements

Table 1. Results against every requirement

| ID | Was | Target | Result | Status | Section |
| --- | --- | --- | --- | --- | --- |
| PR-001 | R1 | Set and haul with nobody in the water | No step needs anyone in the water once the far stake is set from a boat | Met on paper; field trial at TRL 4 | J |
| PR-002 | R2 | At least 30 m between pulleys; stretch 50 m | 30 m design case; rope bought for 50 m | Met on paper | A |
| PR-003 | R3 | Peak pull under 250 N | 200 N (estimate); 241 N in a 0.3 m/s current | Met on paper in still water; thin in a current | B |
| PR-004 | R4 | Holds 3 kN in soft wet soil without movement | Anchor factor 2.13 at 10 kPa | Met on paper; pull test at TRL 4 | D |
| PR-005 | R5 | Holds 1.5 kN horizontal in soft mud | Factor 2.77 at 10 kPa (stake yields first); 2.03 at 5 kPa (soil fails first), 3.5 m embedded; at the top pin hole 2.51 at 10 kPa, and not used at 5 kPa (D-S7) | Met on paper in soft and very soft mud; pull test at TRL 4 | E |
| PR-006 | R6 | Full haul and reset under 10 min | 6.3 min (estimate, without clearing fish) | Met on paper (estimate) | G |
| PR-007 | R7 | One season without rope or pulley failure | Rope factor 5.7 after sun damage | Met on paper (estimate) | F |
| PR-008 | R8 | Local-materials station parts under USD 80, costed with the partner; steel trial station recorded (restated, decision 15A) | Steel trial station USD 399; local-materials station about USD 98 (estimate) | Steel trial station accepted for TRL 4; **local-materials figure not yet met** (estimate), to be costed with the partner | I |
| PR-009 | R9 | Relocated by two people in under 30 min | 22 min (estimate) | Met on paper (estimate) | H |
| PR-010 | R10 | Weak link releases 500 to 700 N | 510 to 690 N | Met on paper; calibrate at TRL 4 | C |
| PR-011 | R11 | Working spot at least 5 m from the water | 5.0 m | Met by layout | J |
| PR-012 | | Sets and hauls the fisher's own gillnet, up to the span less 2 m, with a bridle at each end | Bridles with snap hooks and weak links on ring 1 and the cleat bar | Met by design | J |
| PR-013 | | Made with welding, drilling, carpentry and rope work; bought parts are commodity rigging | Seven made, seven bought components (bom/bom.csv) | Met by design | I |
| PR-014 | | Heaviest part no more than 25 kg per person for a two-person lift | Far stake 33.2 kg, 16.6 kg each; let down on a lowering rope from the boat side, not held at arm's length (O-7, decided 2026-10-25) | Met on paper | J |
| PR-015 | | Pin-connected plates meet EN 1993-1-8 Table 3.9 at 1.5 times the working load | Least ratio 1.15 (pad eye) | Met on paper (D-S1) | D |
| PR-016 | | Siting and use agreed with the wildlife and fisheries authorities before installation | Not started | To verify at TRL 4 | J |

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

Sensitivity (independent review): with a 0.3 m/s current across the net while hauling the peak is about 241 N, and with friction 0.9 on the bank edge about 243 N; PR-003 is met in still water and thin in a current.

The peak comes at the instant the whole catch is on the bank edge. Hauling is done by the net's near end, so the loop only follows. Setting the net takes about **43 N** at 0.5 m/s.

## C. Weak link (R10) and design loads

The weak link sets the largest load a seized or snagged net can put into the system.

- Release: nominal **600 N**, plus or minus 15 % (510 to 690 N). The cord is chosen by pulling three samples from the batch bought.
- The largest load in normal use is during setting, **62 N**, so the lowest release is **8.3 times** the normal load: no nuisance breaks.
- Hauling is done by the net's near end by hand, so no haul load passes through a weak link; the far link only drags the loop (18 N).
- A clean 30 m net set across a current reaches the link's lowest release at about 0.76 m/s; weed and fish lower that. BankHaul is for still to slow water (0.3 m/s design).
- Far end design load: both legs at the highest release, **1.38 kN**, within the 1.5 kN of R5.
- Bank design load: **3.0 kN** (R4) horizontal at the near block. It covers twice the link release, debris on the loop and a jammed cleat.

## D. Bank post, stays and screw anchors (R4)

Assumptions: soft wet soil with an undrained shear strength of 10 kPa; anchors with a single 250 mm helix on a 1.6 m rod, set in line with the stay; capacity Q = Fc x su x A with Fc = 9 for a deep helix (depth to helix diameter 3.6, at the critical depth for this soil).

| Quantity | Value | Note |
| --- | --- | --- |
| Stay length, lug hole to anchor eye | 1.44 m | Anchor eyes 1,100 mm behind and 450 mm either side |
| Stay elevation | 38.7° | |
| Stay tension at 3 kN | **2,076 N** each | Both stays share the pull along the line |
| Stay rope factor | 6.4 | 10 mm three-strand polyester, 1,590 kg (15.6 kN, Marlow; D-S5, was taken as 22 kN), 85 % at the eye splice |
| Post compression | 2,595 N | Buckling factor 93 (48.3 x 3.2 tube, 1.0 m, pinned) |
| Foot plate bearing | 22.6 kPa | Factor 2.3 on 5.14 x su |
| Helix depth | 0.89 m | |
| Anchor capacity | **4,418 N** each | Factor **2.13** on the stay tension |
| Pad eye shear | 24.8 MPa | Block load 6 kN, two shear planes (64 mm pad eye, D-S1) |
| Block working load factor | 1.67 | 500 kg block, two legs at 1.5 kN |
| Pad eye end distance beyond the hole | 15.2 mm | Needs 13.2 mm (EN 1993-1-8 Table 3.9, 1.5 x 3 kN, S235); was 11.2 mm with the 60 mm pad eye (D-S1) |
| Stay lug end distance | 12.5 mm | Needs 10.8 mm (1.5 x 2.08 kN) |
| Collar lug end distance | 20.5 mm | Needs 12.6 mm (1.5 x 1.38 kN) |
| Stay length between thimble centres | 1,111 mm | 1,440 mm lug to anchor eye less two shackles, two thimble offsets and the turnbuckle at mid take-up (D-S3); cut 1.5 m |

A factor of 2 or more on the anchor's ultimate capacity is taken as "no visible movement", since helical anchors creep noticeably above about half their ultimate load. R4 is met on paper; the TRL 4 pull test on a CalRig-style rig settles it.

## E. Far stake lateral capacity (R5)

Method: Broms' free-head pile in cohesive soil, the lesser of the short-pile case (the soil fails) and the long-pile case (the stake reaches its plastic moment, 6.72 kN m for S355 and a plastic modulus of 18.9 cm3). Version 0.2 used the short-pile case alone, which gave 6.1 kN in soft mud; at that load the stake would already have yielded (D-S2). The load acts 1.2 m above the bed (1.0 m of water plus 0.2 m to the far block). The stake is a 76.1 x 3.6 mm S355 tube, 5.0 m long, embedded 3.5 m (decision 14A, BKH-DDR-003; Amish, 2026-10-03: "i agree with all the 46 recommendations you provided. please proceed.").

| Bed | Undrained shear strength | Short pile (soil) | Long pile (stake yields) | Capacity | Factor on 1.5 kN | Bending stress at 1.5 kN |
| --- | --- | --- | --- | --- | --- | --- |
| Soft mud | 10 kPa | 6,079 N | 4,156 N | 4,156 N | **2.77** | 150 MPa (factor 2.4 on S355) |
| Very soft mud | 5 kPa | 3,040 N | 3,642 N | 3,040 N | **2.03** | 162 MPa (factor 2.2 on S355) |

At the top pin hole (the far block 200 mm above its design level, water 1.2 m deep, load 1.4 m above the bed) the factor is 2.51 in soft mud but 1.91 in very soft mud, and bending at 1.5 kN is 183 MPa. So in very soft beds (hand vane 5 to 10 kPa) the top hole is not used: water deeper than 1.0 m at the stake takes the loop out, as for a flood (D-S7, under Amish's standing instruction). Driving the stake 4.0 m instead would give 2.24; since 3.5 m was Amish's decision 14A, that alternative is his (BKH-DEC-001 O-8).

A 60.3 mm stake would carry the load in soft mud but reach about 250 MPa at 1.5 kN, too close to yield; the 76.1 mm tube was chosen for strength (BKH-DDR-002, item 6). The bending stress at the R5 load does not change with embedment, since the largest moment lies within about 0.6 m of the bed.

At the first TRL 3 embedment of 2.5 m the factor in very soft mud was **1.23**, so R5 was at risk there. Driving the stake 1.0 m deeper raises it to **2.03**: R5 (PR-005) is **met on paper in soft and very soft mud**; very soft mud governs. The stake is 1.0 m longer, 6.4 kg heavier (33.2 kg) and USD 12 dearer. The TRL 4 pull test from the boat settles it.

## F. Loop rope strength and durability (R7)

- The largest leg tension is the larger of the link's highest release and half the bank load: 1.5 kN. The new rope through a splice (85 %) has a factor of **11.3** on it. Both ends of each loop half are eye-spliced round the swivel rings (D-S6); the round turn and two half hitches drawn before kept about 60 % and gave 4.0 at the season's end. 20 kN is taken for 12 mm three-strand polysteel; 12-strand polysteel of 12 mm is rated 2,740 kg (Marlow), and the bought rope's figure is to confirm.
- Assuming the rope loses half its strength to sun over a tropical season, the factor at the end of the season is **5.7**.
- Two set and haul cycles a day for 180 days give about 720 passes over each sheave, far below the bending fatigue life of fibre rope at a sheave ratio of 8.
- Blocks with bushed nylon sheaves in silty water are the less certain part; the season pilot at TRL 4 records bush wear.

R7 is met on paper as an estimate.

## G. Cycle time (R6), estimate

Haul at 0.25 m/s with stacking (2.0 min), unclip (1.0 min), re-clip (1.0 min), set 30 m at 0.4 m/s (1.3 min), cleat and tie off (1.0 min): **6.3 minutes**. Clearing a 10 kg catch of about 30 fish at 20 s each takes a further 10 minutes, as it does today; the loop does not change it, so it is outside this figure.

## H. Relocation (R9), estimate

Two people: unscrew both anchors (4 min), lift out the post and spike (2), carry up to 50 m (3), set out the new spot (3), screw in both anchors (6), stand the post and tension the stays (4): **22 minutes**. Re-splicing both ring eyes for the new loop length takes about 15 minutes more (D-S6) and is outside R9, which covers the bank anchor.

## I. Cost per station (R8) and value engineering

PR-013: every made part is cut, drilled and welded from tube, plate and bar, sawn and screwed from timber, or spliced from rope; the bought parts are commodity rigging. The station parts in `bom/bom.csv` cost **USD 399** (the 5.0 m far stake adds USD 12); with the stake driving cap, the prototype costs USD 409. Value-engineering target: USD 1,800. Estimated cost of the constructable design: USD 409 (USD 1,391 under the target).

The largest cost drivers are the two screw anchors (USD 76), the far stake (USD 60), the rope (USD 54), the two blocks (USD 44), the table (USD 35) and the post (USD 32).

R8 is restated (decision 15A, BKH-DDR-003; Amish, 2026-10-03: "i agree with all the 46 recommendations you provided. please proceed."). The steel station is built for the TRL 4 trials, so the trials test the method with parts of known strength; its USD 399 is recorded, not held to the R8 figure. The USD 80 figure applies to a local-materials station, costed from local prices with the co-design partner before the season pilot. The first-order estimate of that station (hardwood post with bolted fittings, buried timber deadman, hardwood far pole, two hand-made hardwood sheaves on steel pins, rope for a 30 m span only, galvanised rings, hardwood cleats, a pole table) is about **USD 98**, so the restated R8 is **not yet met** on this estimate. For reference, one bank post and table serving three loops would cost about USD 269 per loop.

## J. Layout and masses

- The post stands 6 m back from the water's edge and the fisher works within 1 m of it: **5.0 m** from the water (R11).
- Once the far stake is set from a boat or at low water, setting, hauling, clearing and relocating the bank station are all done from the bank (PR-001).
- The fisher's own gillnet is used (PR-012): a bridle is tied to each end; the net is no longer than the span less 2 m, so no ring reaches a block.
- The heaviest part, the far stake, is 16.6 kg per person for two people (PR-014), within the 25 kg ISO 11228-1 reference mass for one person; a team lift counts for less than the sum and a 5 m tube in a boat is awkward, so Amish decided on 2026-10-25 that the stake is stood against the boat side and let down on a lowering rope through its top cross hole, two people on the rope (BKH-DEC-001 O-7); PR-014 is met on paper, to confirm in the TRL 4 drill. The bank-edge board of O-2 (BOM line 18, USD 5 estimate) takes the station to USD 399; its effect on the 157 N of bank-edge drag is measured in the R3 trial, not calculated.
- PR-016 (agreement of the siting and use with the wildlife and fisheries authorities) is verified with the co-design partner before any installation at TRL 4.
- The D3 model of the design case (`cad/src/model.py`, kit densities) gives 107.7 kg with every fastener and weld, against the 106 kg estimated below; the fidelity check (`cad/fidelity.json`) gives 102.0 kg for the 7 m picture layout, which has a shorter loop.
- Masses: bank post weldment 17.2 kg, far stake 33.2 kg, two screw anchors 14.3 kg, clearing table 26.4 kg, swivel collar 1.6 kg, two blocks 2.2 kg, rope 7.5 kg, small parts about 4 kg: about **106 kg** for the station. The heaviest part is the far stake, handled by two people from a boat.
