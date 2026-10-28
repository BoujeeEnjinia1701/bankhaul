---
doc_id: BKH-STM-001
title: BankHaul STEM check
project: BankHaul
doc_type: STEM check
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First STEM check (kit 1.8 upgrade of a TRL 3 repo); seven detail failures in option A fixed under Amish's standing instruction (BKH-DEC-001 D-S1 to D-S7, three after the independent review); options B and C checked; independent review recorded
- version: '0.2'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'S30 with the lowering rope decided by Amish (O-7, 2026-10-25); verdict unchanged'
---

# BankHaul STEM check

Verdict: the working principle of option A, the current design (a floating rope loop on two blocks that carries a net's far end out from the bank and back), sits within known science. Seven details failed and were fixed under Amish's standing instruction of 2026-10-23, four found by the author and three by the independent review: the pad eye was 4 mm short of the pin-plate end distance in EN 1993-1-8 (D-S1); the far stake's capacity in soft mud was stated for the soil alone, although the stake yields first (D-S2); the back-stays were drawn about 330 mm too long to fit between the shackles and the turnbuckle (D-S3); the table, cleat bolts and screws did not fit their neighbours (D-S4); the stays' rope was taken at 22 kN where 10 mm three-strand polyester is rated 15.6 kN (D-S5); the hitched second end of each loop half kept only about 60 % of the rope's strength (D-S6); and at the top pin hole, with 1.2 m of water, the stake's factor in very soft mud fell to 1.91 (D-S7). Of the 38 claims, **21 are within known science, 15 are plausible, to confirm at TRL 4 or later, and 2 fail with a fix proposed, both in options not carried forward** (B2, the cableway's guy anchor; C1, the lift net's hand line pull). The plausible rows need field data or the bought parts' data (users' pull, weak link scatter, driving the stake, UV loss, rope strength, sheave ratio, bush wear, corrosion, a team lift in a boat, exposure and catch), so `stem_check` stays **open**. No row fails outright. Method: STANDARDS section 20. Calculations: `docs/04-calcs/stem_check.py`, which imports `docs/04-calcs/sizing.py` (BKH-CAL-001).

> **Safety:** This check tests the physics, not the safety of working beside crocodile water. Rows S24 and S25 show the station meets published advice for working distance and removes wading; neither makes the water's edge safe.

## Claims checked

Table 1. Claims, governing science and verdicts (generated from `docs/04-calcs/stem_results.csv`). The kit's label "Plausible, to confirm at TRL 3" is used for every plausible row; each says which trial or later work confirms it.

<!-- STM_TABLE -->
| # | Claim | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | Loop length for the 30 m design span is 60.4 m | Mathematics | Units and dimensional analysis | Two legs plus half a wrap of the rope centre line (56 mm radius) round each sheave | claimed 60.4 m, estimate 60.4 m (ratio 1.00) | Within known science | BKH-CAL-001 A |
| S2 | Peak hand pull to haul a 30 m gillnet with 10 kg of catch is about 200 N | Physics | Mechanics and statics | Coulomb friction (0.6) and lift of catch, weed and a fifth of the wet net up a 27 degree bank edge, plus half the water drag; still water. Sensitivity: 241 N in a 0.3 m/s current, 243 N at friction 0.9 | claimed 200 N, estimate 173 N (ratio 1.15) | Within known science | BKH-CAL-001 B |
| S3 | Pull to set the net (loop and net paying out at 0.5 m/s) is about 43 N | Physics | Mechanics and statics | Rope friction on the ground, lead line friction on the bed and drag, through two blocks at 0.95 each | claimed 43 N, estimate 43.4 N (ratio 0.99) | Within known science | BKH-CAL-001 B |
| S4 | A person can make a 200 N peak hand-over-hand pull on a rope, briefly, twice a day | Biology | Ergonomics | Manual pulling forces of the working population (ISO 11228-2 method, to assess for the users); the peak lasts the few seconds the catch crosses the bank edge | No population data for the partner fishers; the R3 trial measures the pull with a spring scale | Plausible, to confirm at TRL 3 | Open |
| S5 | The weak link never breaks in normal use: its lowest release is at least twice the largest normal load | Engineering and technology | Standards practice | Lowest release 510 N over the largest load in normal use (setting, 62 N); hauling is by the net's near end by hand, so the far link only drags the loop (18 N) and no haul load passes a link | 8.27 x >= 2 x | Within known science | BKH-CAL-001 C |
| S6 | A braided cord loop can be chosen to release between 500 and 700 N (600 N plus or minus 15 %) | Engineering and technology | Manufacturing tolerances | Breaking strength scatter of one batch of braided polyester cord; calibrated by pulling three samples (BKH-BLD-001 3.7) | Batch scatter to measure at TRL 4 on CalRig | Plausible, to confirm at TRL 3 | Open |
| S7 | A seized net cannot load the far end beyond 1.5 kN (both legs at the link's highest release) | Physics | Mechanics and statics | Statics of the far block: two legs at 690 N | 1.38 kN <= 1.5 kN | Within known science | BKH-CAL-001 C |
| S8 | A set gillnet in a 0.3 m/s current stays below the weak link's lowest release | Physics | Fluid mechanics | Drag 0.5 rho v^2 Cd A on the twine (solidity about 0.0125 for 0.25 mm twine at 40 mm bar) and on the head and foot ropes, Cd 1.2; a clean net reaches the link's release at 0.76 m/s, so the station is for still to slow water | 79.4 N <= 510 N | Within known science | BKH-CAL-001 C (design loads) |
| S9 | The 10 mm polyester stays carry the 3 kN bank load with a factor of 5 or more on breaking strength | Physics | Strength of materials | Stay tension from statics of two splayed stays (2.08 kN); 10 mm three-strand polyester 1,590 kg (15.6 kN) minimum break load (Marlow), 85 % at the eye splice | 6.39 x >= 5 x | Within known science | BKH-DEC-001 D-S5; BKH-CAL-001 D |
| S10 | The post does not buckle under the stays' downward pull | Physics | Strength of materials | Euler buckling, 48.3 x 3.2 tube 1.0 m, pinned both ends, against 2.6 kN | 92.5 x >= 3 x | Within known science | BKH-CAL-001 D |
| S11 | The 350 mm foot plate bears on soft wet soil (10 kPa) with a factor of 2 | Physics | Mechanics and statics | Undrained bearing capacity Nc su with Nc 5.14 (Terzaghi, strip; conservative for a square plate) | 2.28 x >= 2 x | Within known science | BKH-CAL-001 D |
| S12 | Each 250 mm screw anchor holds its stay with a factor of 2 in soft soil of 10 kPa | Physics | Mechanics and statics | Helical anchor breakout Q = Fc su A, Fc 9 at H/D at the critical ratio 0.107 su + 2.5 (Das, Earth Anchors), loaded along its axis; at the creep threshold, so the TRL 4 pull test settles it; factor 1.07 if the bank were 5 kPa | 2.13 x >= 2 x | Within known science | BKH-CAL-001 D |
| S13 | The pad eye, stay lugs and collar lug meet the pin-plate geometry rules | Engineering and technology | Standards practice | EN 1993-1-8 Table 3.9 type A: a >= F gM0 / (2 t fy) + 2 d0 / 3, c >= F gM0 / (2 t fy) + d0 / 3, S235, 1.5 x working load; least ratio of the three plates | 1.15 ratio >= 1 ratio | Within known science | BKH-DEC-001 D-S1; BKH-CAL-001 D |
| S14 | The near block's working load limit covers both legs at 1.5 kN | Engineering and technology | Standards practice | Catalogue working load limit 500 kg (4.9 kN) against 3.0 kN | 1.67 x >= 1 x | Within known science | BKH-CAL-001 D |
| S15 | The far stake, driven 3.5 m, holds 1.5 kN with a factor of 2 in soft and very soft mud | Physics | Mechanics and statics | Broms lateral capacity in clay, the lesser of the short pile (soil fails) and the long pile (stake yields at its S355 plastic moment); very soft mud at 1.0 m of water governs; at the top pin hole (1.2 m of water) 2.51 in soft mud and 1.91 in very soft mud, so the top hole is not used in very soft beds (D-S7) | 2.03 x >= 2 x | Within known science | BKH-DEC-001 D-S2, D-S7; BKH-CAL-001 E |
| S16 | The stake stays elastic at the R5 load | Physics | Strength of materials | Bending at the largest moment, M = H (e + 1.5 d + 0.5 f), elastic modulus of the 76.1 x 3.6 tube, water 1.2 m deep at the top hole; limit 355 / 1.5 MPa; no corrosion allowance (S23) | 183.2 MPa <= 236.7 MPa | Within known science | BKH-CAL-001 E |
| S17 | A 76.1 mm stake can be driven 3.5 m into a soft bed from a boat with a post driver or sledge | Engineering and technology | Manufacturing tolerances | Driving resistance of soft clay is low; the cap disc and driving cap spread the blows (BKH-BLD-001 step 6) | Driving effort and verticality to confirm at the trial site; a firm layer would stop it short of 3.5 m (to confirm by probing) | Plausible, to confirm at TRL 3 | Open |
| S18 | The loop rope keeps a factor of 5 on its working tension at the end of a season | Physics | Strength of materials | 20 kN taken for 12 mm three-strand polysteel (12-strand polysteel is 2,740 kg, Marlow), 85 % at the splices with both ends of each half spliced (D-S6; a hitch at about 60 % gave 4.0), half lost to sun: factor 5.67 | Rests on the UV loss of S19 and the bought rope's breaking strength; both to confirm | Plausible, to confirm at TRL 3 | Open |
| S19 | UV-stabilised polysteel rope loses no more than half its strength in one tropical season | Chemistry | Materials and polymer chemistry | Photo-oxidation of polypropylene and polyethylene in sunlight; the stabiliser and the season's dose set the loss. The factor stays above 2 unless 80 % is lost | Loss rate for the rope bought to measure in the season pilot (R7) | Plausible, to confirm at TRL 3 | Open |
| S20 | The polysteel loop floats in fresh and brackish water | Chemistry | Materials and polymer chemistry | Density of the polypropylene and polyethylene blend about 0.93 g/cm3 (rope maker's data) against water at 1.00 to 1.01 | 0.93 g/cm3 <= 1 g/cm3 | Within known science | BKH-CAL-001 A |
| S21 | The 100 mm sheave suits 12 mm fibre rope at this load | Engineering and technology | Standards practice | Sheave to rope diameter ratio 8.33 on the tread, at the commonly quoted minimum of about 8 for fibre rope (source to confirm with the rope maker); working tension under 8 % of breaking strength | Ratio on the margin of the guidance; bending wear observed in the season pilot | Plausible, to confirm at TRL 3 | Open |
| S22 | Bushed nylon sheaves last a season in silty water | Engineering and technology | Manufacturing tolerances | Abrasive wear of a plain bush by silt; 720 passes a season at low load | Bush wear to record in the season pilot (R7) | Plausible, to confirm at TRL 3 | Open |
| S23 | The painted steel post and stake, galvanised rigging and stainless stop pin last several seasons in fresh or brackish water | Chemistry | Electrochemistry and batteries | Corrosion of carbon steel at a waterline and in mud; the small stainless bolt is the cathode against a large painted steel area, the favourable galvanic ratio | Corrosion rate in the trial water to confirm; inspect the stake at the waterline each season (BKH-RSK-001) | Plausible, to confirm at TRL 3 | Open |
| S24 | Working 5 m or more back from the water's edge meets published crocodile-safety advice for fishing | Biology | Ecology and agronomy | Northern Territory Government, Be Crocwise: "Stand at least five meters back from the water's edge while fishing" (checked 2026-10-25) | The layout gives 5.0 m (R11); the local wildlife authority's advice for the site may ask for more | Within known science | BKH-CAL-001 J |
| S25 | Setting and hauling from the bank removes most of the fishers' exposure | Biology | Epidemiology | At Kariba 58 % of 60 sampled attacks happened while fishing (Matanzima et al., Oryx); exposure while wading and setting is removed, exposure at the bank is not | The share of fishing attacks that happen while wading, rather than from canoes or the bank, is not known for the trial site | Plausible, to confirm at TRL 3 | Open |
| S26 | Nets set and hauled on the loop catch about as many fish as nets set by wading | Biology | Plant and animal biology | Gillnet catch depends on where and how long the net is set; the loop sets the net along one line from the bank | Catch per set to compare in field trials with partner fishers (TRL 5) | Plausible, to confirm at TRL 3 | Open |
| S27 | A full haul and reset takes about 6 minutes without clearing fish | Mathematics | Orders of magnitude | Rope speed and the fixed handling steps | claimed 6.3 min, estimate 6.25 min (ratio 1.01) | Within known science | BKH-CAL-001 G |
| S28 | Each screw anchor holds about 4.4 kN | Mathematics | Units and dimensional analysis | Q = Fc su A in N with su in Pa and A in m2 | claimed 4.4 kN, estimate 4.42 kN (ratio 1.00) | Within known science | BKH-CAL-001 D |
| S29 | Every part of the design fits its neighbours: the D3 model has no interference, and the stay chain closes within the turnbuckle's take-up | Engineering and technology | Manufacturing tolerances | cad_check interference (no overlap over 5 mm3) and the stay chain: 1440 mm lug to anchor eye less 329 mm of shackles and turnbuckle leaves 1111 mm between thimbles (the stay was drawn 1,440 mm); check: difference from the 1,110 mm made, against the 75 mm half take-up | 1.2 mm <= 75 mm | Within known science | BKH-DEC-001 D-S3, D-S4; cad/fidelity.json |
| S30 | Two people can lift the heaviest part (the far stake, 33.2 kg) upright in a boat | Biology | Ergonomics | ISO 11228-1 reference mass 25 kg per person in ideal conditions; a team lift counts for less than the sum, and a 5 m tube in a boat is awkward | 16.6 kg each; lowered on a rope through the top cross hole from the boat side, decided by Amish 2026-10-25 (BKH-DEC-001 O-7); PR-014 met on paper, to confirm in the TRL 4 drill | Plausible, to confirm at TRL 3 | Open |
| B1 | Option B: the 8 mm wire track cable carries a seized net at mid-span with a factor of 5 | Physics | Strength of materials | Cable tension T = F L / (4 s) + w L^2 / (8 s), the 690 N link release taken as a downward pull at mid-span of 30 m with 1.0 m sag: 5.5 kN; 8 mm galvanised wire rope about 40 kN minimum breaking force (catalogue order, to confirm), 80 % at grip terminations | 5.87 x >= 5 x | Within known science | Open |
| B2 | Option B: the far mast's guy anchor holds the cable's pull in a soft bed | Physics | Mechanics and statics | Guy tension 10.2 kN at about 58 degrees; one 250 mm helix holds 4.4 kN at 10 kPa and 2.2 kN at 5 kPa (S12 method), so the guy needs about 4.6 to 9.3 times one anchor for a factor of 2; four anchors on a spreader give 1.7 at 10 kPa, a 2.5 m sag (4 m masts) 1.07 on one anchor. Fix sized on paper: a buried timber deadman of about 20 kN or a site with a firm bed; not modelled because option B is not carried forward | Fails; the tensioned span multiplies the net-end pull about eight times into the guy | Fails, fix proposed | Open |
| B3 | Option B: the carriage wheels run on the 8 mm wire without wearing it out in a season | Engineering and technology | Standards practice | Wheel groove 9 mm wide for an 8 mm wire; wheel to wire ratio 60 / 8 = 7.5, far below the ratios wire rope makers ask for sheaves the wire bends round, but the carriage rolls along the wire rather than bending it | Wire and wheel wear to assess if option B is carried forward | Plausible, to confirm at TRL 3 | Open |
| B4 | Option B: masts 2.6 m and 3.0 m high keep the cable and carriage clear of the water | Mathematics | Orders of magnitude | Sag of 1.0 m at 30 m with the carriage at mid-span leaves about 1.0 m over the water | To confirm with the site's flood level | Plausible, to confirm at TRL 3 | Open |
| C1 | Option C: the hand line raises a wet 3 m net with 10 kg of catch at no more than 250 N | Physics | Mechanics and statics | Moments about the pivot: boom 9.6 kg/m over 8 m and 3 m arms, 25 kg of net, spreaders and catch at the tip, six 19 kg blocks and a 20 kg basket at 2.55 m; pull at 3 m. Fix sized on paper: two more blocks and a second line to lower the empty net; not modelled because option C is not carried forward | 390 N <= 250 N | Fails, fix proposed | Open |
| C2 | Option C: the 40 mm pivot pin carries the boom, counterweight and net | Physics | Strength of materials | Simply supported over the 710 mm between head plates, 2.7 kN at mid-span; S235, limit 235 / 1.5 MPa | 76.3 MPa <= 156.7 MPa | Within known science | Open |
| C3 | Option C: a 3 m lift net 5 m out catches enough fish for a household | Biology | Plant and animal biology | Shore lift nets work where fish come close inshore, often to a light at night; reach 5 m beyond the edge | Catch to assess with partner fishers; changes the fishing method | Plausible, to confirm at TRL 3 | Open |
| C4 | Option C: the stayed 8 m boom is stiff enough to hold the net level over the water | Physics | Strength of materials | Unstayed, the root moment is about 5.0 kN m against an elastic moment of 11.5 kN m (S355), so strength holds, but the tip sags about 264 mm; the king post stays stiffen it | Stay loads and tip sag with the stays to calculate if option C is carried forward | Plausible, to confirm at TRL 3 | Open |
<!-- /STM_TABLE -->

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3**, **Fails, fix proposed**, **Fails**.

## Fixes made under the standing instruction

Each fix keeps the working principle, the pitch and the scope. All are recorded in BKH-DEC-001 as decided under Amish's standing instruction of 2026-10-23, and he can reverse them.

Table 2. Fixes.

| Item | What failed | Fix (BKH-DEC-001) | Result | Cost |
| --- | --- | --- | --- | --- |
| Pad eye (S13) | The hole was 11.2 mm from the plate's end in the direction of the pull; EN 1993-1-8 Table 3.9 asks for 13.2 mm at 1.5 times the 3 kN bank load | D-S1: pad eye 64 mm radial (plate 64 x 100 mm, end 88 mm from the post axis), hole unchanged | End distance 15.2 mm, ratio 1.15; shear 24.8 MPa | None (4 mm more plate) |
| Far stake capacity (S15) | BKH-CAL-001 v0.2 gave 6.1 kN in soft mud (factor 4.05) from Broms' short-pile case; at that load the tube's moment is about 10.7 kN m, well past its plastic moment of 6.7 kN m, so the stake yields first | D-S2: the calculation takes the lesser of the short-pile and long-pile capacities; no design change | Soft mud 4.2 kN (factor 2.77); very soft mud unchanged at 3.0 kN (factor 2.03, governs) | None |
| Back-stays (S29) | Lug hole to anchor eye is 1,440 mm; the stay was drawn with 1,440 mm between its eyes, leaving no room for the two shackles and the turnbuckle (329 mm), more than the turnbuckle's 150 mm take-up | D-S3: stays 1,110 mm between thimble centres, cut 1.5 m (was 1.8 m) | The chain closes at mid take-up | None (4 m of rope still bought) |
| Stay rope strength (S9, independent review) | The stays were checked at 22 kN; 10 mm three-strand polyester is rated 1,590 kg (15.6 kN, Marlow) | D-S5: the rated figure used; no design change | Factor 6.4 (was 9.0), above 5 | None |
| Loop splices (S18, independent review) | The second end of each loop half was hitched to its ring (round turn and two half hitches, about 60 % of the rope's strength): factor 4.0 at the season's end against 5 | D-S6: both ends of each half eye-spliced, the second at installation with the rope work kit; a span change means re-splicing (about 15 minutes) | Factor 5.67 at the season's end, still resting on the UV loss (S19) | None |
| Stake at the top pin hole (S15, independent review) | With the far block on the top hole (water 1.2 m deep, load 1.4 m above the bed) the factor in very soft mud is 1.91 | D-S7: in very soft beds (vane 5 to 10 kPa) the top hole is not used; water deeper than 1.0 m at the stake takes the loop out, as for a flood. Driving 4.0 m instead (factor 2.24) is offered to Amish (BKH-DEC-001 O-8), since 3.5 m was his decision 14A | 2.03 in very soft mud at 1.0 m, 2.51 in soft mud at 1.2 m; bending 183 MPa at the top hole | None |
| Fits found by the D3 model (S29) | Table legs stopped at 750 mm, below the rails they were screwed to; end rails clashed with the legs; the cleat bolts were M8 x 50 where 35 mm grips; the lip boards had no fixing | D-S4: legs 825 mm, end rails 550 mm inside the legs, cleat bolts M8 x 35, eight 6 x 100 mm screws through the lips | No interference in `cad/fidelity.json` | About USD 1 (screws) |

## Options B and C: rows that fail with a fix proposed

- **B2, cableway guy anchor.** A seized net at mid-span pulls 690 N on a 30 m cable sagging 1.0 m, so the cable carries about 5.4 kN and the far mast's guy about 10 kN. One 250 mm screw anchor holds 4.4 kN in soft mud and 2.2 kN in very soft mud; four anchors on a spreader reach only 1.7 at 10 kPa, and a 2.5 m sag with 4 m masts 1.07 on one anchor (independent review). The fix sized on paper is a buried timber deadman of about 20 kN, or siting B only where the bed is firm; it is not modelled, because option B is not carried forward. If Amish chooses B, the fix comes first.
- **C1, lift net hand line.** With six counterweight blocks the hand line needs about 390 N to raise a wet net with 10 kg of catch, against the 250 N of PR-003. Two more blocks balance the loaded net, but then the empty net will not lower without a second line. Not modelled, for the same reason.

## Fields not relevant

None. Every field is touched: physics (statics, friction, rope and steel strength, soil bearing and lateral capacity, drag), chemistry (polymer UV ageing, density, corrosion), biology (ergonomics, crocodile exposure, catch), mathematics (lengths, units, times) and engineering (pin-plate rules, rigging ratings, fits). There are no electrical, thermal, optical or radiation claims, since the station has no power or electronics.

## Concept options

- **Option A, running rope loop:** rows S1 to S30. Within known science after D-S1 to D-S7; open on field data.
- **Option B, overhead cableway:** B1 to B4. The principle holds, but a tensioned span multiplies the net-end pull about eight times into the masts and guy (B2 fails with a fix proposed).
- **Option C, counterweighted shore lift net:** C1 to C4. The principle holds and nothing is placed in the water, but it changes the fishing method from gillnets to a lift net, and the balance needs rework (C1 fails with a fix proposed).

## Independent review

A second agent was run on 2026-10-25 as a separate headless Claude session (`claude -p`, no subagent tool was available) with read-only access to a folder holding only this document, the calculation note BKH-CAL-001, the product requirements BKH-PRS-001 and `sizing.py`, and none of the author's reasoning. It was asked to refute the headline results and every "Within known science" verdict. Its findings and what changed are recorded below.

<!-- REVIEW_TABLE -->
Table 3. Independent review findings (2026-10-25) and what changed.

| Row | Finding | Change |
| --- | --- | --- |
| S1, S3, S10, S14, S20, C2 | Upheld; S14 is 1.64 with 500 kg at 9.81 m/s2 rather than 5,000 N | None; the rounding is noted |
| S2, PR-003 | Weakened: 200 N reproduced, but a 0.3 m/s current gives about 241 N and friction 0.9 about 243 N | Sensitivity added to BKH-CAL-001 B and S2; PR-003 met in still water, thin in a current |
| S4 | Plausible verdict right; 200 N is not a safe repeated pull for every user | PR-003 to review with the partner's users |
| S5 | Weakened if the haul load passed through a link | It does not: hauling is by the net's near end by hand, and the far link only drags the loop (18 N); stated in S5 and CAL C |
| S6, S7 | Link-to-link scatter is wider than batch scatter; the 1.5 kN far-end basis has about 10 points of headroom | S6 stays plausible; per-link testing is a TRL 4 item (BKH-BLD-001 3.7); S7 depends on S6, as stated |
| S8 | A clean net releases the link at about 0.76 m/s; fouling lowers this | Limiting current added (CAL C); still to slow water only (PRS assumptions) |
| S9 | Weakened: 10 mm polyester is about 12 to 15 kN, not 22 kN | Checked: 1,590 kg (15.6 kN, Marlow); D-S5; factor 6.4 |
| S11 | Factor 2.28 is below the usual 3 for bearing; settlement possible | Kept within: the 2.6 kN is the rare 3 kN design event, not a sustained load; settlement watched at TRL 4 |
| S12, S28 | Fc at the critical ratio and at the creep threshold; 1.07 if the bank were 5 kPa | Noted in S12; PR-004 is for 10 kPa soil and is settled by the pull test |
| S13 | The note's shear row uses 6 kN; at 6 kN the pin-plate ratio is 1.06 | Both stated; the pad eye's load is the 3 kN at the block, the 6 kN shear row is a margin |
| S15, S16 | Refuted at the block's top position: the reviewer took 2.0 m of water; the top pin hole gives 1.2 m, where very soft mud gives 1.91 and bending 183 MPa | D-S7 (top hole not used in very soft beds); O-8 offers a 4.0 m drive to Amish; S16 now at the top hole |
| S17 | Refusal criterion and fallback missing | BKH-DEC-001 item 12 (probe first); refusal short of 3.5 m means a new check, recorded in RSK F2 |
| S18 | Refuted: 20 kN looked high and the hitch keeps about 55 % | Rope strength checked high, not low: 12-strand 12 mm polysteel is 2,740 kg (Marlow), so 20 kN for three-strand stands, to confirm; the hitch was the real gap: D-S6 splices both ends; S18 now plausible, as it rests on S19 |
| S21 | On the margin of an unsourced guidance figure | Now plausible, source to confirm with the rope maker |
| S24 | Zero margin on 5 m; Northern Territory advice is for saltwater crocodiles | Kept within on the published advice; the local authority's figure governs at the site (PR-016) |
| S25 | Recovering a released net or freeing a fouled block takes someone to the water | Added to BKH-RSK-001 (H10) |
| S27 | Cycle excludes clearing fish | As PR-006 states; clearing (about 10 minutes) is reported beside it in CAL G |
| S29 | Cut length 1,516 mm against 1.5 m | Cut 1.52 m (bom/bom.csv) |
| S30, PR-014 | A team lift in a boat counts for less than twice one person | Now plausible; lifting method to Amish (O-7), decided 2026-10-25: the lowering rope, two people |
| B1 | Load direction and terminations | 690 N taken as a downward pull; 80 % at the grips: factor 5.93 |
| B2 | Failure understated; neither fix gives a factor of 2 | Text corrected: a buried deadman or a firm bed |
| B3 | Ratio limit unsourced | Now plausible |
| C4 | Refuted logic: the unstayed boom is strong enough | Rewritten: strength holds; the stays are for stiffness (tip sag about 260 mm unstayed) |
| Missing | A snag or boat on the loop; a crocodile striking the loop or stake; retrieving a released net | Added to BKH-RSK-001 (H8, H10, H11) |

The reviewer's three main findings were the stake at the highest water level, the dependence of the headline loads on the weak link and a slow, clean current, and thinner rope and anchor factors. The first and the rope findings led to D-S5 to D-S7; the second is now stated as an operating limit (still to slow water) and a TRL 4 test of the links.
<!-- /REVIEW_TABLE -->

## Sources

- Broms, B. B. "Lateral Resistance of Piles in Cohesive Soils." *Journal of the Soil Mechanics and Foundations Division* 90, no. SM2 (1964): 27 to 63 (short and long free-head piles; S15).
- Das, Braja M. *Earth Anchors*. Amsterdam: Elsevier, 1990 (breakout factor and critical embedment of plate anchors in clay; S12, S28).
- EN 1993-1-8, *Eurocode 3: Design of steel structures, Part 1-8: Design of joints*, Table 3.9 (geometry of pin-connected plates; S13). The formulas are as commonly quoted; the text of the standard was not consulted for this check and is to be confirmed by the design lead.
- ISO 11228-1 and ISO 11228-2, *Ergonomics: Manual handling* (lifting and carrying; pushing and pulling). Cited by number and title for S4 and S30; texts not consulted.
- Marlow Ropes. "3STR Polyester 10mm White 100mR" (minimum break load 1,590 kg) and "12 Strand Polysteel" (12 mm, 2,740 kg). https://www.shopusa.marlowropes.com/en-us/3str-polyester-10mm-white-100mr-ab0042 and https://www.shopusa.marlowropes.com/en-us/12-strand-polysteel-jtq (checked 2026-10-25; S9, S18).
- Matanzima, J., I. Marowa and T. Nhiwatiwa. "Negative Human-Crocodile Interactions in Kariba, Zimbabwe: Data to Support Potential Mitigation Strategies." *Oryx*. https://www.cambridge.org/core/journals/oryx/article/negative-humancrocodile-interactions-in-kariba-zimbabwe-data-to-support-potential-mitigation-strategies/E7F0BCD336ECFE79877214CCE7D589C5 (S25).
- Northern Territory Government. "Stay Safe While Fishing and Boating." Be Crocwise. https://becrocwise.nt.gov.au/crocodiles-and-me/stay-safe-while-fishing-and-boating (checked 2026-10-25): "Stand at least five meters back from the water's edge while fishing" (S24).
- Terzaghi, K. *Theoretical Soil Mechanics*. New York: Wiley, 1943 (bearing capacity factor Nc; S11).
- BKH-CAL-001 for every load, mass and factor quoted.
