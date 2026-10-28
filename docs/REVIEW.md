# Review note: BankHaul

## Session 2026-10-25: decisions

Amish, 2026-10-25 10:19 CT, after a report listing each repo's proposed decisions and recommendations: "i concur with your recommendations". Every decision that carried a recommendation is recorded as decided with the option recommended. All eight open decisions carried one.

### Decided by Amish, 2026-10-25

- **O-1 concept:** option A. `project.yaml` `concept_chosen: "A"`; `CHOSEN` comment in `cad/src/model.py`; BKH-DDR-004 v0.2 decided; BKH-OPT-001 v0.2; PRC, PRS, PLN, README.
- **O-2 bank-edge board:** new part in the D3 model, `_edge_board()` in `cad/src/model.py`: smooth hardwood 250 x 600 x 25 mm, edges rounded 10 mm, set flush into the bank lip under both loop legs (option A now 161 parts). New `bom/bom.csv` line 18, USD 5 (estimate, as recommended). Station USD 394 to **USD 399**, prototype USD 404 to **USD 409** (USD 1,391 under the USD 1,800 target), USD 269 to **USD 274** a loop with a shared bank post. Build plan section 3.8 (the board), step 10 (setting it) and the set-and-haul check (pull measured with and without it). The board is not in the legacy grouped components, so the GA drawings and making sketches do not show it; it appears in `components("A")`, the STEP export and the product model.
- **O-3:** B2 and C1 fixes stay on paper only. No change.
- **O-4:** site render on the bank as the hero. No change.
- **O-5:** `0003-amish-requirement-decisions.md` kept as BKH-DDR-003; `0003-requirement-decisions-round2.md` marked Superseded (v0.2).
- **O-6:** indicative USD 22 a block kept, to confirm locally (MKT, FEA notes).
- **O-7 far stake lift:** the stake is stood against the boat side and let down on the 10 m offcut of the loop coil through its top cross hole, two people on the rope (build plan step 6; BOM line 6 note). PR-014 **at risk to met on paper** (16.6 kg each, to confirm in the TRL 4 drill); STEM S30 text (still Plausible); `sizing.py` note; CAL, RSK H6.
- **O-8:** D-S7 kept (3.5 m drive). No change.
- Documents: BKH-DEC-001 v0.4, BKH-PRS-001 v0.5, BKH-CAL-001 v0.4, BKH-BLD-001 v0.4, BKH-STM-001 v0.2, BKH-RSK-001 v0.2, BKH-FEA-001 v0.2, BKH-MKT-001 v0.2, BKH-PLN-001 v0.2, BKH-PRC-001 v0.5, BKH-OPT-001 v0.2, BKH-DDR-004 v0.2, README, concept media (key figures, regenerated).

### Still open

None of this round's decisions. PR-008 stays not met (local-materials station about USD 98 against USD 80, to cost with the partner).

### Checks

Run in this order on 2026-10-25 after the last edit to `cad/src/` (`model.py`, `concept_media.py`) and `bom/bom.csv`:

- `python3 docs/04-calcs/sizing.py`: runs; station USD 399, prototype USD 409, USD 274 a loop with a shared post.
- `python3 docs/04-calcs/stem_check.py`: open, 21 within, 15 plausible, 2 fail with a fix proposed (B2, C1, options not carried forward, kept on paper by O-3).
- `python3 .kit/trace.py`: RTM regenerated, 0 gaps.
- `python3 .kit/cad_check.py --export`: PASS at D3 (option A with the bank-edge board).
- `python3 .kit/render.py` and `python3 .kit/render.py --check`: pass, no FAIL.
- `python3 -m reuse lint`: compliant.
- Em and en dash scan outside `.kit/` and `LICENSES/`: none.
- `python3 cad/src/concept_media.py` regenerated the concept sheet with the new cost; it also wrote a 34 MB `media/model.glb`, so the committed 3.7 MB web model (unchanged geometry; the board is not in the grouped concept components) was kept.

## Session 2026-10-24: kit 1.9.1 upgrade

Carried out on 2026-10-25 on Amish's instructions of 2026-10-24 ("Kit 1.9.1 rollout - proceed to rollout across the other repos", "I want detailed TRL3 CAD - and in fact want to ensure the CAD is detailed across all TRLs", "Detail every option") and his standing STEM fix instruction of 2026-10-23. Kit 1.9.1 was installed by the coordinator. Option A, the design of 2026-10-03, keeps its working principle and its main dimensions; seven details changed under the fix rule (below), each recorded in BKH-DEC-001.

### What was added or changed

- `docs/01b-stem-check.md` (BKH-STM-001 v0.1) and `docs/04-calcs/stem_check.py` (writes `stem_results.csv` and refreshes the STM table): 38 claims for options A, B and C; `stem_check: open`.
- `docs/02a-concept-options.md` (BKH-OPT-001 v0.1) and `docs/decisions/0004-concept-selection.md` (BKH-DDR-004): options A, B and C, first-order numbers and weighted scoring.
- `docs/03a-user-requirements.md` (BKH-URS-001, 14 URs); `docs/03-requirements.md` is now BKH-PRS-001 v0.4 (R1 to R11 as PR-001 to PR-011 with a "Was" column, PR-012 to PR-016 new); `docs/03b-traceability.md` (BKH-RTM-001, generated, 0 gaps).
- `docs/07-regulatory.md`, `08-feasibility.md`, `09-risk.md` (project risks, preliminary hazard analysis, first-pass design FMEA), `10-market.md`, `11-plan.md` (REG, FEA, RSK, MKT, PLN v0.1). Prices and advice cited and dated 2026-10-25: Rope Services UK 12 mm polysteel GBP 0.55 a metre; GS Products 4 inch swivel block GBP 27.52 ex VAT; GME Supply earth screw anchor USD 291.99; Marlow 10 mm three-strand polyester 1,590 kg and 12 mm 12-strand polysteel 2,740 kg; Northern Territory Be Crocwise, "Stand at least five meters back from the water's edge while fishing". No bank-hauled net product and no enclosure cost were found; both are "to assess".
- PRB v0.3 (users-and-needs and stakeholders tables), PRC v0.4, CAL v0.3 (`sizing.py`: pin-plate checks, long-pile case, top pin hole, stay chain, haul sensitivities, limiting current, both splices), BLD v0.3, DEC v0.3, `bom/bom.csv` (lines 1, 4, 5, 6, 15 respecified; total unchanged at USD 394), README (stage badge, links line, STEM check and Concept options sections, the broken Zenodo badge replaced by the concept DOI badge), `project.yaml` (`stage: P3`, `stem_check: open`, `concept_options`, `concept_chosen: "A (proposed)"`, `trl_evidence` extended).
- `cad/src/model.py` rebuilt to the kit 1.9 interface (`PARAMS`, `OPTIONS`, `PRINCIPLES`, `CHOSEN = "A"`, `OPTION_VIEWS` with `ground_z: 0`, `ALLOWED_CONTACTS`, `components(option)`); every part is a `cad_parts.part()` dict with a material, a kind and, for option A, its BOM line, plus a legacy "key" so `build_components()`, `far_parts()`, `table_parts()` and `context_shapes()` still feed `sizing.py`, `sheets.py`, `build_plan_media.py` and `concept_media.py`. Option A now has every bolt, nut and washer, shackle bow and pin, thimble, turnbuckle jaw, clevis and split pin, block cheek, sheave, axle and swivel head, the welds as beads, the four-plate stake point, pilot-holed table timbers with 44 screws, and rope eyes threaded through the swivel eyes. `components(option)` builds the 7 m picture layout used by every picture and by `cad/fidelity.json`; `components(option, short=False)` builds the 30 m design case.
- `cad/src/bkh_parts.py` (new, repo-specific): frame, rope and weld helpers; shackle, thimble, turnbuckle, swivel block, jam cleat, screw anchor and wire rope grip at catalogue envelope.
- `cad/src/product_model.py` rebuilt from `components(CHOSEN)` plus an earth bank "(site)", a net on the table and a 1.75 m mannequin "(scale)" standing on the bank. `RENDER_VIEWS`: **hero** (outdoor site, mud, still water), **studio**, **exploded**, **detail** (far end).
- `cad/src/options_preview.py` (new, repo-specific): a provisional shaded `media/options.png` from the D3 models, labelled as a preview, because `render.py --check` needs the file and this rollout does not run `.kit/options.py`.
- Regenerated: `cad/fidelity.json`, `cad/step/A/` (one STEP per made or bought part of option A), `cad/step/{A,B,C}-assembly.step`, legacy STEP and STL (tolerance 0.15 mm, was 0.5), BKH-DWG-001 to 003 Rev P4, making sketches BKH-DWG-101 to 107, all build plan pictures, concept media (BKH-DWG-010, hero, exploded, flow, `model.glb`, viewer).

### STEM verdicts and fixes

21 within known science, 15 plausible, 2 fail with a fix proposed (B2, C1, both in options not carried forward), 0 fail. Fixed in option A under the standing instruction and recorded in BKH-DEC-001, none changing the working principle, pitch or scope, none adding cost beyond about USD 1:

- **D-S1** pad eye 64 mm radial (was 60): the hole's end distance was 11.2 mm against 13.2 mm in EN 1993-1-8 Table 3.9 at 1.5 x 3 kN; now 15.2 mm.
- **D-S2** far stake capacity is the lesser of Broms' short and long pile: 4.2 kN in soft mud (factor 2.77), not 6.1 kN (4.05); very soft mud unchanged at 2.03 and governs. No design change.
- **D-S3** back-stays 1,110 mm between thimbles (drawn 1,440 mm), cut 1.52 m, so the chain of shackles and turnbuckle closes; found by the D3 model.
- **D-S4** fits found by the D3 model: table legs 825 mm, end rails 550 mm inside the legs, rail and lip screws, cleat bolts M8 x 35.
- **D-S5** (found by the review) stays checked at the rated 1,590 kg of 10 mm three-strand polyester, not 22 kN: factor 6.4.
- **D-S6** (found by the review) both ends of each loop half eye-spliced; the hitch kept about 60 % and gave 4.0 against 5 at the season's end.
- **D-S7** (found by the review) the stake's top pin hole is not used in very soft beds; with 1.2 m of water the factor there was 1.91.

### Independent review

No subagent tool was available, so the reviewer ran as a separate headless Claude session (`claude -p`) in a scratch folder holding only the STEM check, CAL, PRS and `sizing.py`. It reproduced the arithmetic and refuted or weakened: the stake at the highest water level (it assumed 2.0 m; the top pin hole gives 1.2 m, still a failure in very soft mud: D-S7), the stays' rope strength (D-S5), the loop's knot efficiency (D-S6; its lower rope strength did not hold, Marlow rates 12 mm polysteel higher than assumed), the hand pull in a current (241 N, now stated), the limiting current for the weak link (0.76 m/s, now stated), the team lift (PR-014 now at risk), options B2 and C4. Full table in BKH-STM-001, Table 3.

### Concept options

| Option | Score (of 220) | Parts in `cad/fidelity.json` | Made or bought | Fasteners | Welds | Mass, fidelity check (picture layout) | Mass, design case |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A, running rope loop (current design) | 178 | 160 | 69 | 76 | 15 | 102.0 kg | 107.7 kg |
| B, overhead cableway | 139 | 175 | 73 | 82 | 20 | 201.5 kg | 213.1 kg |
| C, counterweighted shore lift net | 149 | 127 | 59 | 34 | 34 | 394.0 kg | 394.0 kg |

All three pass D3 (no bare primitives, no interference over 5 mm3). A leads C by 16 %, so A is recommended, proposed, awaiting Amish. Masses use the kit densities; BKH-CAL-001 J gives 106 kg for option A from catalogue figures.

### Requirements not met

- **PR-008 not met**: the local-materials station is about USD 98 (first-order estimate) against USD 80; the steel trial station is USD 394, accepted for TRL 4 by decision 15A.
- **PR-014 at risk**: the 33.2 kg stake is 16.6 kg each for two people, but a team lift in a boat counts for less (O-7).
- PR-003 is met in still water (about 200 N) and thin in a 0.3 m/s current (241 N); PR-016 (authority agreement) is verified at TRL 4.
- BOM total USD 394 for the station (USD 404 with the driving cap) against `budget_usd` 1,800, unchanged.

### Decisions proposed, awaiting Amish

1. **O-1 concept selection:** A (178), C (149), B (139); recommended A. The repo stays on A.
2. **O-2 graft from C:** a smooth board or roller at the bank edge, where 157 N of the 200 N peak comes from.
3. **O-3:** implement the fixes of options B (guy anchor) and C (balance) only if one is chosen.
4. **O-4 product render site:** the model is lifted 560 mm so the photoreal ground is the lake bed under 60 mm of still water and the bank is a site part; this departs from "ground level at z = 0" so the water can show.
5. **O-5:** two decision records carry the ID BKH-DDR-003; keep one and supersede or renumber the other.
6. **O-6 block price:** USD 22 in the BOM against about USD 37 found in the UK.
7. **O-7 lifting the far stake** (PR-014): a lowering rope from the boat, with two people.
8. **O-8:** a 4.0 m drive in very soft beds instead of D-S7's limit (3.5 m was Amish's decision 14A).
9. D-S1 to D-S7 were decided under the standing instruction and can be reversed.

### Safety

No new hazard from the fixes. The review added three hazards to BKH-RSK-001: someone going to the water to recover a released net or free a fouled block (H10), an animal striking the loop or stake (H11) and loads on the loop itself that no weak link limits (H8). The station is for still to slow water: a clean net releases its weak link at about 0.76 m/s. BankHaul reduces time in the water; it does not protect anyone from a crocodile that leaves the water.

### Kit and environment issues met

1. No subagent tool was available to this agent; the independent reviewer ran headless with `claude -p` on a folder holding only the four files.
2. `render.py --check` requires `media/options.png`, which only `.kit/options.py` (Cycles) or `--massing` (not allowed by the rollout) can write; worked around with `cad/src/options_preview.py`, which the coordinator's render overwrites.
3. `.kit/stem_check.py` labels every plausible row "Plausible, to confirm at TRL 3", even in a TRL 3 repo whose plausible rows can only be closed by TRL 4 or later field data.
4. `cad_parts.clevis_pin()` fillets the head-to-pin edge, which adds material under the head, so a pin seated on a plate face reports interference; the pins are set 3 mm off their plates.
5. `photoreal.py` site scenes have one ground plane at `--ground-z`; a product on a bank above water cannot show the water at z = 0 (O-4 workaround).
6. `cad_parts` has no polyester, polysteel or nylon density; rope parts use "rope" (1,100 kg/m3), so fidelity masses of ropes read high.
7. `.kit/options.py` will label `CHOSEN` as "CHOSEN" although the choice is only proposed.
8. `.kit/drawing.py` `project_views()` raises "No shapes to export" for a rope sketch 1,100 or 1,110 mm long but not 1,111.2 or 1,440 mm (a degenerate ellipse in one view leaves a layer empty); `build_plan_media.py` uses the exact chain length.
9. `concept_media.py` with the D3 detail wrote a 34.6 MB `model.glb` at the old 1.0 mm deflection; a `--web-only` mode at 3.0 mm and 0.8 rad was added in the repo.
10. The scratchpad folder and the machine are shared with the other fleet agents; logs were prefixed `bankhaul-`, and only this agent's own jobs were waited on.

### Checks

Run in this order on 2026-10-25, after the last edit to `cad/src/` and `bom/bom.csv`:

- `python3 docs/04-calcs/sizing.py`: runs; `results.csv` written. `python3 docs/04-calcs/stem_check.py`: open, 21 within, 15 plausible, 2 fail with a fix proposed, 0 fail.
- `python3 .kit/trace.py`: BKH-RTM-001 v0.1 written, 0 gaps (16 PRs, 14 URs).
- `python3 .kit/cad_check.py --export`: PASS at D3 for A, B and C; 69 per-part STEP files in `cad/step/A/` and three assembly STEPs.
- `python3 .kit/render.py`: every controlled document rendered to `docs/pdf/` (the stale BKH-REQ-001 PDF removed; both BKH-DDR-003 records render to one file name, O-5).
- `python3 .kit/render.py --check`: passes, no FAIL and no warnings.
- `python3 -m reuse lint`: compliant (287 of 287 files); no new annotation needed, `REUSE.toml` covers every file type added.
- No em or en dashes outside `.kit/` and `LICENSES/`. Largest file in the repo 10.5 MB (`cad/step/bankhaul-assembly.step`), none over 45 MB; `media/model.glb` 3.7 MB after a coarser web tessellation (`concept_media.py --web-only`; the full run gave 34.6 MB).
- Not run: `python3 .kit/release_gate.py` (release is not part of this rollout).

Not run, as the rollout asks: `.kit/options.py` without `--export`, `photoreal.py`, `export_views.py`, `cards.py`. `media/render-hero.png`, `render-exploded.png`, `render-detail.png`, `card.png` and `social-preview.png` are the renders of 2026-10-04; `media/render-studio.png` (linked from the README) does not exist yet. The coordinator renders `media/options.png` and the four `RENDER_VIEWS` from the new models.

### Recommended next step

Amish decides O-1 and the other open items; the coordinator renders the options picture and the product views. TRL 4 stays on hold under the cap.


## 2026-10-03: Amish's requirement decisions carried out

Amish, 2026-10-03: "i agree with all the 46 recommendations you provided. please proceed." For BankHaul that decides items 14 and 15 as recommended (14A and 15A). Recorded in `docs/decisions/0003-amish-requirement-decisions.md` (BKH-DDR-003) and `docs/06-design-decisions.md` (BKH-DEC-001 v0.2); open decisions are now none.

**Changes made.**

- **14A, R5: far stake driven 3.5 m.** `cad/src/model.py` embedment 2,500 to 3,500 mm, so the stake is 5.0 m long overall (tube 4,850 mm); constructability checks pass (no overlaps, nothing floating); STEP and STL regenerated. `bom/bom.csv` line 2: USD 48 to USD 60 (same tube price per metre, about USD 12 a metre, for 1.0 m more), 33.2 kg. Build plan (BKH-BLD-001 v0.2) section 3.2 and step 6: cut 4,850 mm, paint ring 3,500 mm above the point, two people lift the stake upright, push and twist it down before driving; safety stop updated.
- **15A, R8 restated.** `docs/03-requirements.md` (BKH-REQ-001 v0.3) quotes Amish: R8 now applies "parts under USD 80 per station" to a local-materials station costed from local prices with the co-design partner before the season pilot; the steel station built for the TRL 4 trials is costed and recorded but not held to that figure. No design change.
- Calculation note BKH-CAL-001 v0.2 and `docs/04-calcs/sizing.py` re-run; `results.csv` updated. Precis BKH-PRC-001 v0.3 and README cost updated.

**New results.**

| Requirement | Target | New result | Status |
| --- | --- | --- | --- |
| R5 | Holds 1.5 kN horizontal in soft mud (factor 2 taken as "holds") | Factor 2.03 in very soft mud (5 kPa, was 1.23); 4.05 in soft mud (10 kPa, was 2.46); bending 162 MPa at 1.5 kN, unchanged | Met on paper in both beds; TRL 4 pull test |
| R8 (restated) | Local-materials station parts under USD 80, costed with the partner; steel trial station recorded | Steel trial station USD 394; local-materials station about USD 98 (first-order estimate) | Trial station accepted; local-materials figure not yet met on the estimate, settled by the partner's costing |

**Cost and mass.** Value-engineering target: USD 1,800. Estimated cost of the constructable design: USD 404 (USD 1,396 under the target); station parts USD 394. Far stake 33.2 kg (6.4 kg more), still the heaviest part; station about 106 kg.

**Pictures changed.** BKH-DWG-002 and BKH-DWG-003 at Rev P3 (BKH-DWG-001 bumped with the shared revision list, content unchanged); making sketch BKH-DWG-102 Rev P2; build plan steps 6, 7 and 8 redrawn; concept blueprint key figures (BKH-DWG-010) and concept media regenerated. The overview and joint pictures show the stake cut short and do not change. Appearance model: the detail view adds a red paint ring at the bed marking 3.5 m driven, since the deeper stake itself is below the bed and out of sight (appearance addition under Amish's decision of 2026-10-03). Scene files re-exported to `/home/claude/renders/bankhaul`; photoreal renders are re-made on Amish's Mac.

**Safety.** Standing a 5.0 m, 33 kg stake upright from a boat is harder than a 4.0 m one; the build plan now has two people lift it and nobody drive it standing higher than the boat's seat. All other safety notes stand.

**Cross-repo actions.** None.

**Open decisions.** None. Nothing new needs Amish.

**Recommended next step.** The design is ready for TRL 4 when the phase allows: build the steel station, run the R4, R5 and R10 proof loads (CalRig or in place), and cost the local-materials station with the co-design partner for R8.

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

## 2026-10-04: photoreal renders redone after the round-2 and round-3 decisions

Views: hero, exploded, detail; cards regenerated; image_qc passes and `render.py --check` has no FAIL.
