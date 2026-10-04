---
doc_id: BKH-DDR-003
title: BankHaul requirement decisions of 2026-10-03
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
  change: Amish's decisions 14A (R5, far stake driven 3.5 m) and 15A (R8, steel trial station and local-materials costing) recorded and carried out
---

# 0003: Requirement decisions of 2026-10-03 (far stake depth and cost per station)

- **Date:** 2026-10-03
- **Status:** accepted
- **Decided by:** Amish Chadha, 2026-10-03: "i agree with all the 46 recommendations you provided. please proceed." For BankHaul these are decisions 14A and 15A, each the recommended option.

## Context

The TRL 3 review left two requirements open (`docs/REVIEW.md`, TRL 3, "Decisions for Amish"):

1. **R5, far stake holding in very soft mud.** The 76.1 mm stake driven 2.5 m held an ultimate 1,845 N in a bed of about 5 kPa shear strength, a factor of 1.23 on the 1.5 kN of R5 against the factor of 2 taken as "holds".
2. **R8, cost per station.** The constructable station cost USD 382 in parts against "parts under USD 80 per station".

## Options considered

| Item | Options | Recommended |
| --- | --- | --- |
| 14 (R5) | A: drive the stake 3.5 m (5.0 m stake); B: two stakes 1 m apart, tied at the top; C: keep 2.5 m and use only sites with a firmer bed | A |
| 15 (R8) | A: build the steel station for the TRL 4 trials and cost a local-materials station with the co-design partner; B: switch the prototype to local materials now (about USD 98); C: one bank post and table for three loops | A |

## Decision

- **14A.** The far stake is a 76.1 x 3.6 mm S355 tube 5.0 m long overall (tube 4,850 mm plus the 150 mm point), driven 3.5 m into the bed. The paint ring that marks the driven depth moves to 3,500 mm above the point; the stop pin holes stay where they were relative to the cap.
- **15A.** The steel station is built for the TRL 4 trials. A local-materials station is costed from local prices with the co-design partner before the season pilot. R8 is restated: "Parts under USD 80 per station for a local-materials station, costed from local prices with the co-design partner before the season pilot. The steel station built for the TRL 4 trials is costed and recorded but not held to this figure."

## Consequences

| Item | Requirement | New result | Against the target |
| --- | --- | --- | --- |
| 14A | R5 | Factor 2.03 in very soft mud (3,040 N ultimate); 4.05 in soft mud (6,079 N); bending 162 MPa at 1.5 kN, unchanged | Met on paper in both beds; the TRL 4 pull test settles it |
| 15A | R8 (restated) | Steel trial station USD 394; local-materials station about USD 98 (first-order estimate) | Trial station accepted; the local-materials figure is not yet met on the estimate and is settled by the partner's costing |

- **Mass.** The stake is 33.2 kg, 6.4 kg more; it remains the heaviest part and is lifted by two people from the boat. The station is about 106 kg.
- **Cost.** The stake line rises from USD 48 to USD 60 (the same tube price per metre, about USD 12 a metre, for 1.0 m more). Value-engineering target: USD 1,800. Estimated cost of the constructable design: USD 404 (USD 1,396 under the target). Station parts USD 394.
- **Build.** The stake is cut 4,850 mm long and driven to a paint ring 3,500 mm above the point. In soft mud it sinks part of the way under its own weight and is pushed and twisted down before driving. Drawings BKH-DWG-002 and BKH-DWG-003 are at Rev P3 (BKH-DWG-001 bumped with them, no change to its content); making sketch BKH-DWG-102 is at Rev P2; build plan steps 6 to 8 are redrawn.
- **Safety.** A 5.0 m stake is longer to stand up from a boat. The build plan's safety stop now says two people lift it upright and nobody drives it from a standing position higher than the boat's seat.
