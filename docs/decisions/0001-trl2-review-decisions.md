---
doc_id: BKH-DDR-001
title: BankHaul TRL 2 review decisions
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
  change: TRL 2 review items decided under Amish's pre-approvals of 2026-10-03
---

# 0001: TRL 2 review decisions

- **Date:** 2026-10-03
- **Status:** accepted

## Context

The TRL 2 review (`docs/REVIEW.md`, TRL 2 section) raised the items below. On 2026-10-03 Amish wrote: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." He then wrote: "Proceed with the remaining 15 scaffolds", under the same pre-approval, which covers BankHaul. Every design recommendation below is therefore decided as recommended. Choices that touch safety take the conservative option, with the evidence that would relax them stated. Partners and regions are the first candidates to approach, not agreements. Requirements that are not met or at risk on paper (R5 in very soft mud, R8) are not decided here; they are posed to Amish in `docs/REVIEW.md` under "Decisions for Amish".

## Options considered

Table 1 lists the options for each item and the one chosen.

## Decision

*Table 1. Items decided on 2026-10-03 under Amish's pre-approvals.*

| # | Item | Options | Decision | What would relax a safety choice |
| --- | --- | --- | --- | --- |
| 1 | Bank anchor | (a) post driven or concreted in as a cantilever; (b) buried timber deadman; (c) post on a foot plate held back by two stays to screw ground anchors | (c), conservative: the stays take the pull as tension and the anchors can be moved in about 22 minutes (R9). Anchors sized at a factor of 2 on the R4 load | Pull tests at the trial site showing a holding factor above 3 would allow one anchor in firm soil |
| 2 | Far end for the first prototype | (a) driven stake; (b) float held by a sinker | (a) for the prototype, because a float that holds 1.5 kN sideways needs a sinker or anchor heavier than two people can place from a canoe. The float is kept as a variant for deep beds, not built in the first prototype | Not a safety choice |
| 3 | Load limit on the net | (a) none, size everything on what a crocodile can pull; (b) a weak link at each net end | (b), conservative: R10 added, release 500 to 700 N. The far end then sees 1.4 kN at most | Release tests showing a tighter scatter could narrow the band, never raise its top above 700 N |
| 4 | Where the fisher works | At the water's edge; 3 m back; 5 m back | At least 5 m back, conservative: R11 added; the post stands 6 m from the water | Local attack-distance data from the wildlife authority could support a different distance at a given site |
| 5 | Loop rope | 10 mm sinking polyester; 12 mm floating polysteel | 12 mm floating polysteel: a hand-hauling grip, stays visible and clear of the bed, factor 5.7 after a season's sun | Not relaxed |
| 6 | Clip points | (a) knots or hitches tied anywhere on the loop; (b) two swivel rings half a loop apart that join the loop halves | (b): the rings are the clip rings and the end stops and never run round a block if the net is at least 2 m shorter than the span | Not a safety choice |
| 7 | Bank brake | (a) horn cleat; (b) ratchet block; (c) a jam cleat for each leg | (c): either leg drops into its cleat between pulls and holds against an offshore pull | Not relaxed |
| 8 | How the net is hauled | (a) by the loop, far end first; (b) by the net's near end, with the loop following | (b): the net comes in straight onto the table without doubling back; the weak links stay out of the hauling load | Not a safety choice |
| 9 | Floods | Leave the loop in; take it out | Take the loop out before a flood; floating debris can load it far beyond its design | Not relaxed |
| 10 | Co-design partner | A wildlife authority; a researcher with local attack data; a fisher association | First candidate to approach: the Lake Kariba research group behind the Oryx study (Matanzima, Marowa and Nhiwatiwa), together with an inshore fishing cooperative on the Zimbabwean shore (not agreed) | |
| 11 | Shared blocks | CalRig for proof loads; hand capstan from SaltDrag and SiltHaul | CalRig is the first candidate rig for the anchor, stake and weak link tests at TRL 4. The hand capstan is not used: the peak pull is about 200 N, and the design-around excludes powered hauling | |
| 12 | Budget | Keep `budget_usd` at 1,800 | Kept; it is a value-engineering target, not a limit | |

## Consequences

- R10 (weak link) and R11 (working distance) are added to BKH-REQ-001.
- The design for construction (BKH-DDR-002) works from these choices.
- R5 in very soft mud and R8 are posed to Amish as decisions; they are listed as "Proposed, awaiting Amish" in `docs/06-design-decisions.md`.
