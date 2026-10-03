---
doc_id: BKH-PRB-001
title: BankHaul problem statement
project: BankHaul
doc_type: Problem statement
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 2 update; first co-design candidate, safety note, open questions routed to the decisions register
---

# BankHaul problem statement

Small-scale fishers often work gillnets and traps close to shore, in the shallows or from canoes. In crocodile water, fishing is the activity during which most recorded attacks happen.

## The problem

Attack studies across Africa and Asia point to the same activity. At Kariba, fishing accounted for 58 % of sampled attacks, ahead of domestic chores at 27 % ([Oryx](https://www.cambridge.org/core/journals/oryx/article/negative-humancrocodile-interactions-in-kariba-zimbabwe-data-to-support-potential-mitigation-strategies/E7F0BCD336ECFE79877214CCE7D589C5)). In northern Mozambique victims were collecting water, bathing, wading across rivers, falling from canoes and fishing with gill nets, rod and line, or nets and traps ([Oryx, 2010](https://www.cambridge.org/core/journals/oryx/article/humanwildlife-conflict-in-mozambique-a-national-perspective-with-emphasis-on-wildlife-attacks-on-humans/434EEAAF88F3C10E9FA6B55F2C3ACE39)). In Timor-Leste, fishing and crabbing account for about 80 % of reported attacks ([ABC News, 2025](https://www.abc.net.au/news/2025-01-09/crocodile-management-nt-lessons-for-timor-leste/104522096)).

The main engineered answer so far is the crocodile exclusion enclosure, a fenced area at the water's edge. Enclosures work well for bathing, collecting water and washing, but are far less useful for fishers ([CrocAttack](https://crocattack.org/crocodile-exclusion-enclosures-cees/)). The Uganda Wildlife Authority built enclosures on Yuwe Island in Lake Victoria in 2019 after about 10 deaths, mainly to protect water collection ([PML Daily, 2019](https://www.pmldaily.com/news/2019/10/yuwe-island-gets-crocodile-exclusion-enclosures.html)). Commercial setnet fishers already use running lines, a pulley system from shore to deeper water, to moor skiffs ([Northwest Setnetters](https://www.northwestsetnetters.org/what-we-do)), but that practice assumes boats and has not been packaged as a no-wade method for subsistence fishers.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Subsistence and small-scale fishers | Set, check and haul nets from the bank at night and at dawn | Lake shores, river banks, estuaries and mangrove edges |
| Fisher associations and village committees | A shared set of stations at known hotspots | Landing sites and fishing camps |
| Wildlife authorities | A mitigation measure they can promote alongside patrols and closures | Human-wildlife conflict programmes |
| NGOs and livelihood programmes | A low-cost, locally made kit | Households in conflict hotspots |

## Operating environment

- Fresh or brackish water, still to slow flowing; banks from firm to soft mud and sand.
- Working span from bank anchor to offshore pulley of 10 to 50 m (33 to 164 ft) (target).
- Water depth at the offshore pulley up to about 3 m (10 ft) for a stake, deeper with a float (estimate).
- Seasonal level change of the shoreline; banks move as water rises and falls.
- Night and dawn use, sun, UV and floating debris; hippos and crocodiles present.

## Constraints

- Prototype budget ceiling USD 1,800 for all prototypes and test rigs.
- No powered hauler; hand pull only (IP screen design-around).
- Parts cost target below USD 80 per station (target), using commodity rope, pulleys and anchors.
- Installable without anyone standing in crocodile water; the offshore point is placed from a boat, at low water, or by a trained team with protection.
- Open hardware under CERN-OHL-S-2.0.

## Out of scope

- Crocodile deterrence, capture or culling.
- Protection for bathing and water collection, already covered by exclusion enclosures.
- Motorised line haulers or winches.
- Changes to fishing regulations or zoning.

## Prior work

| Prior work | What it does | Gap for these users | Source |
| --- | --- | --- | --- |
| Crocodile exclusion enclosures (CEEs) | Metal or wire fenced areas at the water's edge for bathing, washing and collecting water | Far less useful for fishers, who need to reach water beyond the fence | [link](https://crocattack.org/crocodile-exclusion-enclosures-cees/) |
| Yuwe Island enclosures, Uganda Wildlife Authority (2019) | Crocodile exclusion enclosure for residents who depend on Lake Victoria for water | Protects a fixed water point, not fishing | [link](https://www.pmldaily.com/news/2019/10/yuwe-island-gets-crocodile-exclusion-enclosures.html) |
| Setnet running lines | A pulley line from shore to deeper water used by commercial setnetters to moor skiffs | Assumes boats and crew; not documented as a no-wade method for subsistence nets | [link](https://www.northwestsetnetters.org/what-we-do) |
| EP1429601B1, device for hauling a fishing line (expired 2022) | A hydraulic motorised pulley and capstan line hauler | Powered and boat-mounted; BankHaul stays manual and bank-based | [link](https://patents.google.com/patent/EP1429601B1/en) |

## Co-design

First candidate to approach (not agreed): the Lake Kariba research group behind the Oryx study (Matanzima, Marowa and Nhiwatiwa), together with an inshore fishing cooperative on the Zimbabwean shore of the lake, because the researchers hold attack locations and times and can site a trial station where attacks happen (BKH-DDR-001, item 10).

Checklist for the co-design work:

- [ ] Confirm the net types, lengths and depths used at the trial site.
- [ ] Map the bank, bed and water level over a season at two candidate stations.
- [ ] Agree who places and inspects the far stake, and from which boat.
- [ ] Agree the safety briefing with the local wildlife authority.

The original brief: a fisher association in a documented attack hotspot, working with the wildlife authority or a human-wildlife conflict researcher who already holds local attack data, so the station is sited where attacks happen and tested with the nets people actually use.

## Safety

> **Safety:** BankHaul is a rope system worked beside crocodile water. It reduces time in the water; it does not protect anyone from a crocodile that leaves the water. Placing the far stake is the most dangerous step and is done from a boat or at low water, never by wading. A loaded rope can snap back, and a net seized by a large animal can pull hard on the loop: the design limits that pull with a weak link, keeps the fisher at least 5 m from the water and never ties the loop to anyone. BankHaul is published as an open engineering reference, not certified equipment.

## Open questions

The questions below are answered, or routed to the design decisions register (`docs/06-design-decisions.md`), at TRL 3.


- How can the offshore stake or float be placed safely where no boat is available?
- Does a moving loop disturb fish or crocodiles more than a static net?
- Which net types (gillnet, seine, traps) suit the loop, and which do not?
- Will fishers use shared stations, or does each household need its own?
- How does anchor pull-out behave in soft, saturated beds over a season?
