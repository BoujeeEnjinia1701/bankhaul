---
doc_id: BKH-DDR-002
title: BankHaul design for construction
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
  change: Constructability review and changes that make the design buildable, decided under Amish's pre-approvals of 2026-10-03
---

# 0002: Design for construction

- **Date:** 2026-10-03
- **Status:** accepted

## Context

STANDARDS section 18 asks for every part to be makeable by its stated process and to fit and fasten to its neighbours (Amish, 2026-09-30: "fix the design assumptions to match and be physically feasible"). The TRL 2 concept (BKH-PRC-001, BKH-DDR-001) was reviewed part by part in `cad/src/model.py`: how each part is made, how it joins each neighbour, and build123d checks for overlapping parts and for parts that do not touch what holds them. The checks now report no overlaps and no floating parts; the only contacts allowed are a pin or rope eye passing through the hole or eye it is fitted to. Amish pre-approved every recommendation on 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." and "Proceed with the remaining 15 scaffolds". No change alters what BankHaul does or its pitch; the safety-related changes all take the conservative side.

## Options considered

For each problem the simplest physically sound fix was chosen; the alternatives are noted in Table 1.

## Decision

*Table 1. Changes made for construction.*

| # | Part | Problem found | Change | Why |
| --- | --- | --- | --- | --- |
| 1 | Bank anchor post | The concept's "screw or deadman anchor carrying the pulley at waist height" put a 3 kN pull 1 m above soft soil, which a post alone cannot resist | A 48.3 x 3.2 mm tube welded to a 350 mm foot plate with a 400 mm ground spike, held back by two splayed stays to two screw anchors | The post only carries compression (2.6 kN, buckling factor 93); foot bearing factor 2.3 |
| 2 | Near block mounting | No fixing for the pulley was defined | An 8 mm pad eye with an 18 mm hole at 950 mm; the bought swivel block hangs on a 10 mm shackle and lines up with the loop by itself | Commodity parts; pad eye shear 34 MPa at 6 kN |
| 3 | Stay attachment | No stay fixing | Two 8 mm lugs with 15 mm holes at 960 mm, splayed 22 degrees either side of straight back, each with a shackle | The stays meet the post square to the lug, so the shackle is not side-loaded |
| 4 | Cleat and brake | A cleat on a round post has no flat face to bolt to | A 130 x 500 x 8 mm cleat bar with a 48.9 mm hole, slipped over the post and welded all round at 850 mm; two jam cleats on M8 bolts and a 15 mm tie-off hole | Gives the bought cleats a flat seat beside each leg |
| 5 | Screw anchors | A vertical anchor pulled at 39 degrees bends its rod in soft soil | Each anchor is screwed in line with its stay, so the rod is in tension; helix 0.9 m deep | Anchor factor 2.13 on the stay tension (BKH-CAL-001, D) |
| 6 | Far stake | A light stake would yield in bending at the R5 load | A 76.1 x 3.6 mm S355 tube, 2.5 m in the bed; a 60.3 mm tube would reach about 250 MPa at 1.5 kN | Bending factor 2.4 on yield; capacity factor 2.46 in soft mud |
| 7 | Stake ends | An open tube cannot be driven without splitting its top | A welded four-plate cone point and a 6 mm cap disc; a separate driving cap tool (BOM 17) | Drivable from a boat with a post driver or sledge |
| 8 | Far block mounting and swivel | The concept's "far pulley and swivel" had no defined way to turn or follow the water level | An 88.9 x 3.2 mm collar that turns on the stake with 3 mm clearance and rests on an M12 stop pin; five pin holes at 200 mm pitch | The collar is the swivel; the pin follows the season's level |
| 9 | Blocks | The rope wrap must not touch the block's spacer or cheeks | Blocks specified with the eye and spacer outside the rope wrap (cheeks 65 mm radius over a 56 mm rope circle); the loop leaves each block level for about 100 mm | Checked in the model: no rope contact with cheeks or spacer |
| 10 | Loop | An endless spliced loop cannot change length as the shoreline moves | Two halves of 55 m, each with an eye splice on one swivel ring and a round turn and two half hitches on the other; surplus coiled at the ring | Spans from 30 to 50 m with the same rope; nothing but the sheave-side rope passes a block |
| 11 | Net clips | "Quick clips" were not defined and had no load limit | A bridle at each net end with a calibrated weak link and a 60 mm stainless snap hook; far end to ring 1, near end to the tie-off hole | R10; the link stays out of the hauling load |
| 12 | Clearing table | A flat table lets a wet net slide off | Slatted top 1,200 x 600 mm at 850 mm with two lip boards; placed landward on the +Y side, clear of the stays | Net stays on the table; the table is at least 5 m from the water |

## Consequences

- `cad/src/model.py`, the drawings BKH-DWG-001 to 003 (Rev P2), the concept media and the build plan pictures are regenerated from the constructable model.
- Bill of materials: the cleat bar, stays, turnbuckles, shackles, stop pin, fixings, rope work kit and driving cap are added. Station parts: USD 382.
- `project.yaml` is set to `design_state: constructable`.
