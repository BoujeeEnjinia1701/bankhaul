# Review note: BankHaul

## Session 2026-10-03: TRL 3 (kit 1.7.0, /to-trl3 under Amish's pre-approvals)

Amish, 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." and, for this second batch, "Proceed with the remaining 15 scaffolds". Every design recommendation in this session is therefore recorded as decided, dated 2026-10-03, in `docs/06-design-decisions.md`. Requirements not met or at risk are not decided; they are posed below under "Decisions for Amish" (Amish, 2026-10-03: "A simple statement doesn't add value - ensure you are identifying a state and posing it as a clear recommendation for me to decide on."). Kit 1.7.0 was installed from the kit source; `.kit/PHASE.yaml` kept as installed.

### TRL 2

**What was done.**

- `docs/01-problem.md` (BKH-PRB-001 v0.2): first co-design candidate with a checklist, safety section.
- `docs/03-requirements.md` (BKH-REQ-001 v0.2): measurable targets with status; R10 (weak link) and R11 (working distance) added.
- `docs/02-concept.md` (BKH-PRC-001 v0.2): how it works, components, key design choices, first-order numbers, safety.
- `docs/decisions/0001-trl2-review-decisions.md` (BKH-DDR-001): twelve TRL 2 review items decided.

**Results.** A hand-pulled loop on two blocks can set and haul a 30 m gillnet from the bank; the hauling pull is set by dragging the catch up the bank edge, not by the loop. The open structural questions were the bank anchor (a 3 kN pull at waist height in soft soil) and the far stake in soft mud.

**Requirements not met.** None decided at TRL 2; R8 (cost) was already doubtful with bought blocks and anchors.

**Decisions made under the pre-approvals.** BKH-DDR-001, items 1 to 12: stayed post on screw anchors; driven stake for the prototype (float kept as a variant); weak links and R10; 5 m working distance and R11; 12 mm floating polysteel; swivel rings as clip rings and stops; jam cleats; haul by the near end; loop out before floods; Lake Kariba researchers with an inshore cooperative as first co-design candidate (not agreed); CalRig as first proof-load rig and no capstan; budget kept.

**Safety concerns.** Placing the far stake; rope snap-back; a net seized by a crocodile pulling the fisher; standing at the water's edge at night.

### TRL 3

**What was done.**

- `docs/04-calcs/01-sizing.md`, `docs/04-calcs/sizing.py` and `docs/04-calcs/results.csv` (BKH-CAL-001 v0.1).
- `cad/src/model.py`: parametric build123d model with constructability checks (no overlaps, nothing floating); STEP and STL in `cad/step` and `cad/stl` (bank station, far end, table; assembly STEP at the 30 m design case).
- `cad/src/sheets.py`: BKH-DWG-001 (bank station GA), BKH-DWG-002 (far end GA) and BKH-DWG-003 (layout, shortened), Rev P2.
- `bom/bom.csv`: 17 lines, all priced, with suppliers by type.
- `cad/src/concept_media.py`: `media/hero.png`, `exploded.png`, `flow.png`, `concept-blueprint.png` and `.pdf` (BKH-DWG-010), `model.glb` (about 1 MB, coarse tessellation) and `viewer.html`. No cutaway (the inside does not matter).
- `docs/decisions/0002-design-for-construction.md` (BKH-DDR-002); `design_state: constructable`.
- `cad/src/build_plan_media.py`: overview, seven making sketches (BKH-DWG-101 to 107), eight joint close-ups and eleven step pictures; `docs/05-build-plan.md` (BKH-BLD-001) and `docs/06-design-decisions.md` (BKH-DEC-001).
- `cad/src/product_model.py` (`product_parts()`, `TITLE`, `RENDER_VIEWS` hero, exploded, detail); scenes exported to `/home/claude/renders/bankhaul` (three .npz and .json, `bankhaul__jobs.json`). Photoreal renders, captions and cards are made on Amish's Mac; the README already leads with `media/render-hero.png`.
- `README.md`, `project.yaml` (trl 3, trl_target 3).

**Results (BKH-CAL-001).** Loop 60.4 m for the 30 m span; peak hand pull about 200 N to haul a 30 m net with 10 kg of catch; setting pull about 43 N; weak link 510 to 690 N, 8.3 times the normal load; far end design load 1.38 kN; stays 2.1 kN each at the 3 kN bank load; screw anchors 4.4 kN each (factor 2.13); far stake 3.7 kN in soft mud (factor 2.46) and 1.8 kN in very soft mud (factor 1.23), bending 150 to 162 MPa in S355; rope factor 5.7 after a season's sun; cycle 6.3 minutes without clearing fish; relocation 22 minutes; station about 100 kg, heaviest part the 26.8 kg stake. Value-engineering target: USD 1,800. Estimated cost of the constructable design: USD 392 (USD 1,408 under the target); station parts USD 382.

**Requirements not met or at risk.**

- **R5, at risk in very soft mud:** met in soft mud (factor 2.46) but factor 1.23 where the bed is very soft.
- **R8, not met:** USD 382 per station.
- R1, R3, R4, R6, R7, R9 and R10 are met on paper or as estimates and are settled by the TRL 4 trials; R6 excludes clearing fish (about 10 minutes for a 10 kg catch), which the loop does not change.

**Decisions for Amish.**

*Decision 1: R5, far stake holding in very soft mud.* State: in a bed with about 5 kPa shear strength, the 76.1 mm stake driven 2.5 m holds an ultimate 1,845 N, a factor of 1.23 on the R5 load, against the factor of 2 used as "holds"; in soft mud (10 kPa) it holds 3,689 N, factor 2.46. Cause: lateral capacity in clay falls in proportion to its strength, and the load acts 1.2 m above the bed.

| Option | Effect on R5 (very soft mud) | Cost | Mass |
| --- | --- | --- | --- |
| A: drive 3.5 m into very soft beds (stake 5.0 m long) | Factor 2.03, met | About USD 12 more per stake | 6.4 kg more (33 kg stake) |
| B: two stakes 1 m apart, tied at the top with a bar carrying the collar | Factor 2.21, met | About USD 56 more | About 28 kg more; two to drive from the boat |
| C: keep 2.5 m and site stations only where a hand vane shows 10 kPa or more | Factor 2.46 where used; very soft beds excluded | None | None |

**Recommendation: A.** It keeps one stake and one driving method, meets R5 in very soft mud for USD 12, and the 1 m extra is cut only for sites that the vane test shows need it.

*Decision 2: R8, cost per station.* State: the constructable station costs USD 382 in parts, about 4.8 times the R8 figure. Cause: bought rated hardware (two screw anchors USD 76, two blocks USD 44, shackles and turnbuckles USD 27) and steel stake and post (USD 80) dominate; the rope is USD 54.

| Option | Effect on R8 | Cost | Mass |
| --- | --- | --- | --- |
| A: build this steel station for the TRL 4 trials; cost a local-materials station with the co-design partner from local prices before the season pilot | Not met for the trial station; a local figure replaces the estimate | USD 382 now | About 100 kg |
| B: switch the prototype now to local materials: hardwood post and far pole, buried timber deadman, two hand-made hardwood sheaves, rope cut to a 30 m span, hardwood cleats, pole table | About USD 98: not met, close; R7 (sheave wear, timber rot) and R9 (digging a deadman, about 45 minutes) become at risk | About USD 98 | About 30 kg more (timber pole and deadman) |
| C: one bank post and table serve three loops at a landing site (post head with three pad eyes) | About USD 257 per loop: not met | About USD 257 per loop | About 60 kg per loop |

**Recommendation: A.** The steel station has known strengths, so the TRL 4 trials test the method rather than the materials; the local-materials costing then gives a real R8 figure for the season pilot.

**Decisions made under the pre-approvals.** BKH-DDR-002, the twelve design-for-construction changes (listed below); the appearance model additions (below). All in `docs/06-design-decisions.md`. Open decisions: the two above, "Proposed, awaiting Amish".

**Build plan findings (design changes made for construction, BKH-DDR-002).**

1. Bank post as a 48.3 mm tube on a 350 mm foot plate and spike, held back by two stays: the post only carries compression.
2. Pad eye at 950 mm with the near block on a shackle.
3. Two stay lugs splayed 22 degrees, 960 mm up.
4. Cleat bar slipped over the post for the jam cleats and the tie-off hole.
5. Screw anchors set in line with the stays, helix 0.9 m deep.
6. Far stake 76.1 x 3.6 mm S355; a 60.3 mm tube would reach about 250 MPa at the R5 load.
7. Welded point and cap disc on the stake; a driving cap tool added.
8. Swivel collar with 3 mm clearance on a moveable M12 stop pin, five holes at 200 mm.
9. Block eye and spacer outside the rope wrap; loop leaves each block level.
10. Loop as two halves joined by swivel rings, one end spliced and one hitched, so the span can change.
11. Net bridles with calibrated weak links and snap hooks.
12. Slatted table with lip boards, landward of the post and clear of the stays.

**Appearance model.** `product_model.py` uses the `model.py` solids in the shortened layout. Additions not in `model.py`: the loop and rings cut into a bank part and a far part, the stake shown above the bed only, a net stacked on the table, and a 1.75 m mannequin (`mannequin()`, standing, facing the water) beside the post and to the left of it as seen by the hero camera, never between the camera and the station. Decided under the pre-approvals.

**Safety concerns.**

- Placing the far stake from a boat in crocodile water is the most exposed job; it is a safety stop in the build plan, with two people and a lookout.
- A net seized by a large crocodile: the weak link bounds the load at about 700 N, but only if the link is never replaced with stronger cord; it is painted and tested by batch.
- Rope and stay snap-back: anchors sized at factor 2; nobody in the bight of the loop or in line with a stay.
- Floating debris can load the loop beyond its design; the loop comes out before floods.
- The 5 m working distance is a judgement, not data; the wildlife authority's advice may call for more at a given site.

**Recommended next step.** After Amish decides the two items above, the design is ready for TRL 4 when the phase allows: build one station, run the R4, R5 and R10 proof loads on CalRig or in place, then set and haul trials with the first co-design candidate. Suggestion not added to the repo: a float-and-mooring far end for beds deeper than 1.5 m.

## Session 2026-09-30: scaffolded

### What was done

- Repository created from kit 1.6.0 at TRL 1, target TRL 2.
- `docs/01-problem.md` (BKH-PRB-001 v0.1): problem with cited evidence, users, environment, constraints, prior work, open questions.
- `docs/02-concept.md` (BKH-PRC-001 v0.1): how it works, components, patent design-arounds, shared blocks, safety.
- `docs/03-requirements.md` (BKH-REQ-001 v0.1): 9 proposed requirements.
- `README.md` with concept rationale, burning platform, where it could be used, and what sparked the idea.

### Next

- Run `/populate` to bring the repo to a strong TRL 2 with concept media.

## 2026-10-03: photoreal renders

Rendered with Blender Cycles on Amish's Mac from `cad/src/product_model.py`; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` made with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes and `render.py --check` has no FAIL.
