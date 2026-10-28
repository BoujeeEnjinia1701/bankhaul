---
doc_id: BKH-DDR-004
title: BankHaul concept selection
project: BankHaul
doc_type: Design decision record
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: Concept selection between options A, B and C (BKH-OPT-001); recommendation proposed, awaiting Amish
- version: '0.2'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Decided by Amish (2026-10-25): option A'
---

# 0004: Concept selection

- **Date:** 2026-10-25
- **Status:** decided by Amish, 2026-10-25 ("i concur with your recommendations"): option A, with the bank-edge board graft (O-2).

## Context

Kit 1.8 asks every design for at least two concept options with different working principles, scored against the user requirements (STANDARDS section 21). BankHaul was designed before kit 1.8, so its design is option A. Two other principles that keep fishers out of the water were developed and modelled to D3 (BKH-OPT-001): a tensioned overhead cableway (B) and a counterweighted shore lift net (C).

## Options considered

| Option | Working principle | Score (of 220) | Key numbers | Main weakness |
| --- | --- | --- | --- | --- |
| A, running rope loop | A slack floating loop on two blocks carries the net's far end out and back | **178** | USD 399; 107.7 kg; 200 N peak pull; 30 m reach (50 m rope) | One placement in the water (the far stake, from a boat) |
| B, overhead cableway | A tensioned wire on two masts carries a wheeled carriage and the net's far end | 139 | About USD 600; 213 kg; cable about 5.4 kN, far guy about 10 kN | The span multiplies the net-end pull; the guy anchor fails in soft mud (STEM B2) |
| C, counterweighted shore lift net | A balanced boom on a bank pivot lowers and raises a 3 m lift net 5 m out | 149 | About USD 400; 394 kg; 390 N to raise a loaded net | Changes the fishing method; 5 m reach; balance (STEM C1) |

A leads C by 16 %, outside the 10 % band in which both would go to Amish without a pick.

## Decision

Decided: **option A**, as recommended (Amish, 2026-10-25). It is the only option that sets the fishers' own gillnets at the reach where fish are with loads that screw anchors and a driven stake can hold in soft ground, and its weak links bound what a seized net can do. Graft from the runner-up (C): lift the catch over the bank edge instead of dragging it (a roller or smooth board at the edge), which would cut the peak pull; decided separately on 2026-10-25 as a smooth hardwood board (O-2, BOM line 18).

## Consequences

- Amish confirmed A on 2026-10-25: `concept_chosen: A` in `project.yaml`; no design change from O-1 itself.
- If Amish chooses C: a new design for lift nets, with the balance fix of STEM C1 first and a new set of requirements for reach and catch; the pitch changes, which is his decision.
- If Amish chooses B: the guy anchor fix of STEM B2 first (four anchors on a spreader, or 4 m masts for a 2.5 m sag).
- In every case options B and C stay in `cad/src/model.py` at D3.
