"""BankHaul STEM check calculations (BKH-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv and refreshes Table 1 of docs/01b-stem-check.md. Each row is a
first-order screen of one claim; the sizing itself is the calculation note BKH-CAL-001 (docs/04-calcs/sizing.py),
which this script imports so the rows follow the design. Rows S1 to S30 are option A (the current design);
B1 to B4 option B (overhead cableway); C1 to C4 option C (counterweighted shore lift net).
"""
import contextlib
import io
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "docs" / "04-calcs")]
from stem_check import Check, G, WITHIN, PLAUSIBLE, FIX  # noqa: E402

with contextlib.redirect_stdout(io.StringIO()):
    import sizing as CAL  # noqa: E402  BKH-CAL-001, reads cad/src/model.py PARAMS
R, P, D = CAL.R, CAL.P, CAL.D

c = Check(ROOT / "docs/04-calcs/stem_results.csv")

# ------------------------------------------------------------------ option A: mechanics of the loop and the net
c.order_of_magnitude("S1", "Loop length for the 30 m design span is 60.4 m", "Mathematics", "Units and dimensional analysis",
                     claimed=60.4, estimate=2 * 30 + 2 * math.pi * 0.056, unit="m",
                     law="Two legs plus half a wrap of the rope centre line (56 mm radius) round each sheave",
                     closed_by="BKH-CAL-001 A")
est_pull = 15.9 * G * (0.6 * math.cos(math.radians(26.6)) + math.sin(math.radians(26.6))) + 0.5 * 1000 * 0.4 ** 2 * 0.5 / 2
c.order_of_magnitude("S2", "Peak hand pull to haul a 30 m gillnet with 10 kg of catch is about 200 N", "Physics",
                     "Mechanics and statics", claimed=round(R["peak_haul_pull"]), estimate=est_pull, unit="N",
                     law=f"Coulomb friction (0.6) and lift of catch, weed and a fifth of the wet net up a 27 degree bank edge, plus half the water drag; still water. Sensitivity: {R['peak_haul_pull_current']:.0f} N in a 0.3 m/s current, {R['peak_haul_pull_mu09']:.0f} N at friction 0.9",
                     closed_by="BKH-CAL-001 B")
c.order_of_magnitude("S3", "Pull to set the net (loop and net paying out at 0.5 m/s) is about 43 N", "Physics",
                     "Mechanics and statics", claimed=43.0,
                     estimate=(2 * 30 * P["rope_kg_m"] * G * 0.3 + 1.8 * G * (1 - 1 / 11.3) * 0.6 + 0.5 * 1000 * 0.25 * 0.1 + 5) / 0.95 ** 2,
                     unit="N", law="Rope friction on the ground, lead line friction on the bed and drag, through two blocks at 0.95 each",
                     closed_by="BKH-CAL-001 B")
c.cited("S4", "A person can make a 200 N peak hand-over-hand pull on a rope, briefly, twice a day", "Biology",
        "Ergonomics", "Manual pulling forces of the working population (ISO 11228-2 method, to assess for the users); the peak lasts the few seconds the catch crosses the bank edge",
        "No population data for the partner fishers; the R3 trial measures the pull with a spring scale", PLAUSIBLE)
c.claim("S5", "The weak link never breaks in normal use: its lowest release is at least twice the largest normal load",
        "Engineering and technology", "Standards practice", "Lowest release 510 N over the largest load in normal use (setting, 62 N); hauling is by the net's near end by hand, so the far link only drags the loop (18 N) and no haul load passes a link",
        round(R["weak_link_margin"], 2), 2.0, "x", rule="above", closed_by="BKH-CAL-001 C")
c.cited("S6", "A braided cord loop can be chosen to release between 500 and 700 N (600 N plus or minus 15 %)",
        "Engineering and technology", "Manufacturing tolerances",
        "Breaking strength scatter of one batch of braided polyester cord; calibrated by pulling three samples (BKH-BLD-001 3.7)",
        "Batch scatter to measure at TRL 4 on CalRig", PLAUSIBLE)
c.claim("S7", "A seized net cannot load the far end beyond 1.5 kN (both legs at the link's highest release)", "Physics",
        "Mechanics and statics", "Statics of the far block: two legs at 690 N", R["far_end_design_load"] / 1000, 1.5, "kN",
        closed_by="BKH-CAL-001 C")
q_net = 0.5 * 1000 * 0.3 ** 2 * 1.2 * (30 * 2 * 0.0125) + 0.5 * 1000 * 0.3 ** 2 * 1.2 * 30 * 0.012 * 2
c.claim("S8", "A set gillnet in a 0.3 m/s current stays below the weak link's lowest release", "Physics", "Fluid mechanics",
        f"Drag 0.5 rho v^2 Cd A on the twine (solidity about 0.0125 for 0.25 mm twine at 40 mm bar) and on the head and foot ropes, Cd 1.2; a clean net reaches the link's release at {R['current_to_release_link']:.2f} m/s, so the station is for still to slow water",
        round(q_net, 1), 510.0, "N", closed_by="BKH-CAL-001 C (design loads)")

# ------------------------------------------------------------------ option A: bank station
c.claim("S9", "The 10 mm polyester stays carry the 3 kN bank load with a factor of 5 or more on breaking strength",
        "Physics", "Strength of materials", "Stay tension from statics of two splayed stays (2.08 kN); 10 mm three-strand polyester 1,590 kg (15.6 kN) minimum break load (Marlow), 85 % at the eye splice",
        round(R["stay_rope_factor"], 2), 5.0, "x", rule="above", closed_by="BKH-DEC-001 D-S5; BKH-CAL-001 D")
c.claim("S10", "The post does not buckle under the stays' downward pull", "Physics", "Strength of materials",
        "Euler buckling, 48.3 x 3.2 tube 1.0 m, pinned both ends, against 2.6 kN", round(R["post_buckling_factor"], 1), 3.0, "x",
        rule="above", closed_by="BKH-CAL-001 D")
c.claim("S11", "The 350 mm foot plate bears on soft wet soil (10 kPa) with a factor of 2", "Physics", "Mechanics and statics",
        "Undrained bearing capacity Nc su with Nc 5.14 (Terzaghi, strip; conservative for a square plate)",
        round(R["foot_bearing_factor"], 2), 2.0, "x", rule="above", closed_by="BKH-CAL-001 D")
c.claim("S12", "Each 250 mm screw anchor holds its stay with a factor of 2 in soft soil of 10 kPa", "Physics",
        "Mechanics and statics", "Helical anchor breakout Q = Fc su A, Fc 9 at H/D at the critical ratio 0.107 su + 2.5 (Das, Earth Anchors), loaded along its axis; at the creep threshold, so the TRL 4 pull test settles it; factor 1.07 if the bank were 5 kPa",
        round(R["anchor_factor"], 2), 2.0, "x", rule="above", closed_by="BKH-CAL-001 D")
c.claim("S13", "The pad eye, stay lugs and collar lug meet the pin-plate geometry rules", "Engineering and technology",
        "Standards practice", "EN 1993-1-8 Table 3.9 type A: a >= F gM0 / (2 t fy) + 2 d0 / 3, c >= F gM0 / (2 t fy) + d0 / 3, S235, 1.5 x working load; least ratio of the three plates",
        round(R["pin_plates_min_ratio"], 2), 1.0, "ratio", rule="above", closed_by="BKH-DEC-001 D-S1; BKH-CAL-001 D")
c.claim("S14", "The near block's working load limit covers both legs at 1.5 kN", "Engineering and technology", "Standards practice",
        "Catalogue working load limit 500 kg (4.9 kN) against 3.0 kN", round(R["block_load_factor"], 2), 1.0, "x", rule="above",
        closed_by="BKH-CAL-001 D")

# ------------------------------------------------------------------ option A: far stake
c.claim("S15", "The far stake, driven 3.5 m, holds 1.5 kN with a factor of 2 in soft and very soft mud", "Physics",
        "Mechanics and statics", f"Broms lateral capacity in clay, the lesser of the short pile (soil fails) and the long pile (stake yields at its S355 plastic moment); very soft mud at 1.0 m of water governs; at the top pin hole (1.2 m of water) {R['stake_factor_top_hole_soft']:.2f} in soft mud and {R['stake_factor_top_hole_very_soft']:.2f} in very soft mud, so the top hole is not used in very soft beds (D-S7)",
        round(min(R["stake_factor_very_soft"], R["stake_factor_top_hole_soft"]), 2), 2.0, "x", rule="above", closed_by="BKH-DEC-001 D-S2, D-S7; BKH-CAL-001 E")
c.claim("S16", "The stake stays elastic at the R5 load", "Physics", "Strength of materials",
        "Bending at the largest moment, M = H (e + 1.5 d + 0.5 f), elastic modulus of the 76.1 x 3.6 tube, water 1.2 m deep at the top hole; limit 355 / 1.5 MPa; no corrosion allowance (S23)",
        round(R["stake_stress_top_hole_very_soft"], 1), 355 / 1.5, "MPa", closed_by="BKH-CAL-001 E")
c.cited("S17", "A 76.1 mm stake can be driven 3.5 m into a soft bed from a boat with a post driver or sledge", "Engineering and technology",
        "Manufacturing tolerances", "Driving resistance of soft clay is low; the cap disc and driving cap spread the blows (BKH-BLD-001 step 6)",
        "Driving effort and verticality to confirm at the trial site; a firm layer would stop it short of 3.5 m (to confirm by probing)", PLAUSIBLE)

# ------------------------------------------------------------------ option A: rope, hardware and materials
c.cited("S18", "The loop rope keeps a factor of 5 on its working tension at the end of a season", "Physics", "Strength of materials",
        f"20 kN taken for 12 mm three-strand polysteel (12-strand polysteel is 2,740 kg, Marlow), 85 % at the splices with both ends of each half spliced (D-S6; a hitch at about 60 % gave {R['rope_factor_end_season_hitched']:.1f}), half lost to sun: factor {R['rope_factor_end_season']:.2f}",
        "Rests on the UV loss of S19 and the bought rope's breaking strength; both to confirm", PLAUSIBLE, closed_by="")
c.cited("S19", "UV-stabilised polysteel rope loses no more than half its strength in one tropical season", "Chemistry",
        "Materials and polymer chemistry",
        "Photo-oxidation of polypropylene and polyethylene in sunlight; the stabiliser and the season's dose set the loss. The factor stays above 2 unless 80 % is lost",
        "Loss rate for the rope bought to measure in the season pilot (R7)", PLAUSIBLE)
c.claim("S20", "The polysteel loop floats in fresh and brackish water", "Chemistry", "Materials and polymer chemistry",
        "Density of the polypropylene and polyethylene blend about 0.93 g/cm3 (rope maker's data) against water at 1.00 to 1.01",
        0.93, 1.0, "g/cm3", closed_by="BKH-CAL-001 A")
c.cited("S21", "The 100 mm sheave suits 12 mm fibre rope at this load", "Engineering and technology", "Standards practice",
        f"Sheave to rope diameter ratio {R['sheave_ratio']:.2f} on the tread, at the commonly quoted minimum of about 8 for fibre rope (source to confirm with the rope maker); working tension under 8 % of breaking strength",
        "Ratio on the margin of the guidance; bending wear observed in the season pilot", PLAUSIBLE)
c.cited("S22", "Bushed nylon sheaves last a season in silty water", "Engineering and technology", "Manufacturing tolerances",
        "Abrasive wear of a plain bush by silt; 720 passes a season at low load",
        "Bush wear to record in the season pilot (R7)", PLAUSIBLE)
c.cited("S23", "The painted steel post and stake, galvanised rigging and stainless stop pin last several seasons in fresh or brackish water",
        "Chemistry", "Electrochemistry and batteries",
        "Corrosion of carbon steel at a waterline and in mud; the small stainless bolt is the cathode against a large painted steel area, the favourable galvanic ratio",
        "Corrosion rate in the trial water to confirm; inspect the stake at the waterline each season (BKH-RSK-001)", PLAUSIBLE)

# ------------------------------------------------------------------ option A: people, fish and crocodiles
c.cited("S24", "Working 5 m or more back from the water's edge meets published crocodile-safety advice for fishing", "Biology",
        "Ecology and agronomy", "Northern Territory Government, Be Crocwise: \"Stand at least five meters back from the water's edge while fishing\" (checked 2026-10-25)",
        "The layout gives 5.0 m (R11); the local wildlife authority's advice for the site may ask for more", WITHIN,
        closed_by="BKH-CAL-001 J")
c.cited("S25", "Setting and hauling from the bank removes most of the fishers' exposure", "Biology", "Epidemiology",
        "At Kariba 58 % of 60 sampled attacks happened while fishing (Matanzima et al., Oryx); exposure while wading and setting is removed, exposure at the bank is not",
        "The share of fishing attacks that happen while wading, rather than from canoes or the bank, is not known for the trial site", PLAUSIBLE)
c.cited("S26", "Nets set and hauled on the loop catch about as many fish as nets set by wading", "Biology", "Plant and animal biology",
        "Gillnet catch depends on where and how long the net is set; the loop sets the net along one line from the bank",
        "Catch per set to compare in field trials with partner fishers (TRL 5)", PLAUSIBLE)

# ------------------------------------------------------------------ option A: mathematics and constructability
c.order_of_magnitude("S27", "A full haul and reset takes about 6 minutes without clearing fish", "Mathematics", "Orders of magnitude",
                     claimed=6.3, estimate=30 / 0.25 / 60 + 30 / 0.4 / 60 + 3.0, unit="min", law="Rope speed and the fixed handling steps",
                     closed_by="BKH-CAL-001 G")
c.order_of_magnitude("S28", "Each screw anchor holds about 4.4 kN", "Mathematics", "Units and dimensional analysis",
                     claimed=4.4, estimate=9 * 10e3 * math.pi * 0.125 ** 2 / 1000, unit="kN",
                     law="Q = Fc su A in N with su in Pa and A in m2", closed_by="BKH-CAL-001 D")
c.claim("S29", "Every part of the design fits its neighbours: the D3 model has no interference, and the stay chain closes within the turnbuckle's take-up",
        "Engineering and technology", "Manufacturing tolerances",
        f"cad_check interference (no overlap over 5 mm3) and the stay chain: {D['stay_chain']:.0f} mm lug to anchor eye less {D['stay_chain'] - D['stay_eyes']:.0f} mm of shackles and turnbuckle leaves {D['stay_eyes']:.0f} mm between thimbles (the stay was drawn 1,440 mm); check: difference from the 1,110 mm made, against the 75 mm half take-up",
        round(abs(D["stay_eyes"] - 1110.0), 1), 75.0, "mm", closed_by="BKH-DEC-001 D-S3, D-S4; cad/fidelity.json")
c.cited("S30", "Two people can lift the heaviest part (the far stake, 33.2 kg) upright in a boat", "Biology", "Ergonomics",
        "ISO 11228-1 reference mass 25 kg per person in ideal conditions; a team lift counts for less than the sum, and a 5 m tube in a boat is awkward",
        "16.6 kg each; lowered on a rope through the top cross hole from the boat side, decided by Amish 2026-10-25 (BKH-DEC-001 O-7); PR-014 met on paper, to confirm in the TRL 4 drill", PLAUSIBLE)

# ------------------------------------------------------------------ option B: overhead cableway
F_wl, span, sag = 690.0, 30.0, 1.0
T_cab = F_wl * span / (4 * sag) + 0.25 * G * span ** 2 / (8 * sag)
c.claim("B1", "Option B: the 8 mm wire track cable carries a seized net at mid-span with a factor of 5", "Physics", "Strength of materials",
        f"Cable tension T = F L / (4 s) + w L^2 / (8 s), the 690 N link release taken as a downward pull at mid-span of 30 m with 1.0 m sag: {T_cab / 1000:.1f} kN; 8 mm galvanised wire rope about 40 kN minimum breaking force (catalogue order, to confirm), 80 % at grip terminations",
        round(40e3 * 0.8 / T_cab, 2), 5.0, "x", rule="above")
gy = T_cab / math.cos(math.atan2(3780, 2400))
c.cited("B2", "Option B: the far mast's guy anchor holds the cable's pull in a soft bed", "Physics", "Mechanics and statics",
        f"Guy tension {gy / 1000:.1f} kN at about 58 degrees; one 250 mm helix holds 4.4 kN at 10 kPa and 2.2 kN at 5 kPa (S12 method), so the guy needs about 4.6 to 9.3 times one anchor for a factor of 2; four anchors on a spreader give 1.7 at 10 kPa, a 2.5 m sag (4 m masts) 1.07 on one anchor. Fix sized on paper: a buried timber deadman of about 20 kN or a site with a firm bed; not modelled because option B is not carried forward",
        "Fails; the tensioned span multiplies the net-end pull about eight times into the guy", FIX)
c.cited("B3", "Option B: the carriage wheels run on the 8 mm wire without wearing it out in a season", "Engineering and technology", "Standards practice",
        "Wheel groove 9 mm wide for an 8 mm wire; wheel to wire ratio 60 / 8 = 7.5, far below the ratios wire rope makers ask for sheaves the wire bends round, but the carriage rolls along the wire rather than bending it",
        "Wire and wheel wear to assess if option B is carried forward", PLAUSIBLE)
c.cited("B4", "Option B: masts 2.6 m and 3.0 m high keep the cable and carriage clear of the water", "Mathematics", "Orders of magnitude",
        "Sag of 1.0 m at 30 m with the carriage at mid-span leaves about 1.0 m over the water", "To confirm with the site's flood level", PLAUSIBLE)

# ------------------------------------------------------------------ option C: counterweighted lift net
m_boom = 9.6     # kg per m, RHS 100 x 60 x 4
M_long = m_boom * G * 8 * 4 + 25 * G * 8
M_short = m_boom * G * 3 * 1.5 + (6 * 19.2 + 20) * G * 2.55
pull = (M_long - M_short) / 3.0
c.claim("C1", "Option C: the hand line raises a wet 3 m net with 10 kg of catch at no more than 250 N", "Physics", "Mechanics and statics",
        "Moments about the pivot: boom 9.6 kg/m over 8 m and 3 m arms, 25 kg of net, spreaders and catch at the tip, six 19 kg blocks and a 20 kg basket at 2.55 m; pull at 3 m. Fix sized on paper: two more blocks and a second line to lower the empty net; not modelled because option C is not carried forward",
        round(pull), 250.0, "N")
c.rows[-1]["verdict"] = FIX
I_rhs = (60 * 100 ** 3 - 52 * 92 ** 3) / 12
c.claim("C2", "Option C: the 40 mm pivot pin carries the boom, counterweight and net", "Physics", "Strength of materials",
        "Simply supported over the 710 mm between head plates, 2.7 kN at mid-span; S235, limit 235 / 1.5 MPa",
        round(32 * (2700 * 0.71 / 4) / (math.pi * 0.040 ** 3) / 1e6, 1), 235 / 1.5, "MPa")
c.cited("C3", "Option C: a 3 m lift net 5 m out catches enough fish for a household", "Biology", "Plant and animal biology",
        "Shore lift nets work where fish come close inshore, often to a light at night; reach 5 m beyond the edge", "Catch to assess with partner fishers; changes the fishing method", PLAUSIBLE)
tip = (m_boom * G * 8 ** 4 / (8 * 210e9 * I_rhs * 1e-12) + 25 * G * 8 ** 3 / (3 * 210e9 * I_rhs * 1e-12)) * 1000
c.cited("C4", "Option C: the stayed 8 m boom is stiff enough to hold the net level over the water", "Physics", "Strength of materials",
        f"Unstayed, the root moment is about {M_long / 1000:.1f} kN m against an elastic moment of {I_rhs / 50 * 355 / 1e6:.1f} kN m (S355), so strength holds, but the tip sags about {tip:.0f} mm; the king post stays stiffen it",
        "Stay loads and tip sag with the stays to calculate if option C is carried forward", PLAUSIBLE)


def table():
    head = "| # | Claim | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n"
    return head + "".join(f"| {r['id']} | {r['claim']} | {r['field']} | {r['branch']} | {r['law']} | {r['check']} | {r['verdict']} | {r['closed_by'] or 'Open'} |\n" for r in c.rows)


if __name__ == "__main__":
    state = c.write()
    doc = ROOT / "docs/01b-stem-check.md"
    if doc.exists():
        t = doc.read_text()
        a, b = t.index("<!-- STM_TABLE -->") + len("<!-- STM_TABLE -->\n"), t.index("<!-- /STM_TABLE -->")
        doc.write_text(t[:a] + table() + t[b:])
        print("refreshed Table 1 of docs/01b-stem-check.md")
