"""BankHaul sizing calculations (BKH-CAL-001).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every result and writes docs/04-calcs/results.csv. Geometry comes from cad/src/model.py
(PARAMS and derived()), so the calculation, the model and the drawings use the same numbers.
Assumptions are stated next to each figure; values marked "estimate" are first-order.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived  # noqa: E402

g = 9.81
RHO_W = 1000.0
D = derived(P)
R = {}          # results by key
ROWS = []       # (requirement, target, result, status, section)


def out(key, value, unit, note=""):
    R[key] = value
    v = f"{value:,.2f}" if isinstance(value, float) else str(value)
    print(f"{key:34s} {v:>12s} {unit:8s} {note}")


# ----------------------------------------------------------------------------- A. loop and rope
print("\nA. Loop and rope")
span = P["span"] / 1000
rp = D["r_pitch"] / 1000
loop = 2 * span + 2 * math.pi * rp
out("loop_len_30", loop, "m", "two legs plus half a wrap round each sheave")
loop50 = 2 * P["span_max"] / 1000 + 2 * math.pi * rp
out("loop_len_50", loop50, "m", "stretch goal span 50 m")
rope_buy = 2 * (P["span_max"] / 1000 + 5.0) + 10.0
out("rope_bought", rope_buy, "m", "two halves of 55 m (5 m for splices and knots) plus 10 m spare")
out("loop_mass_30", loop * P["rope_kg_m"], "kg", "12 mm polysteel 0.068 kg/m, floats (density about 0.93)")
out("sheave_ratio", P["sheave"][0] / P["rope_d"], "D/d", "100 mm sheave, 12 mm rope; 8 or more advised for fibre rope")

# ----------------------------------------------------------------------------- B. haul force (R3)
print("\nB. Hand pull to haul a 30 m gillnet with catch (R3), estimate")
net_len, net_depth = 30.0, 2.0
m_lead = 0.06 * net_len               # lead line, kg (0.06 kg/m, assumption)
m_net_air = 1.2 + 0.03 * net_len + m_lead   # twine 1.2 kg, float line 0.03 kg/m, lead line
m_net_wet = m_net_air * 1.6           # wet net holds water and silt (assumption)
m_catch, m_weed = 10.0, 5.0           # design catch and weed or debris, kg (assumptions)
mu_bed, mu_land = 0.6, 0.6            # friction of net on mud bed and on wet bank (assumption)
v_haul = 0.4                          # hauling speed, m/s
w_lead_sub = m_lead * g * (1 - 1 / 11.3)
F_bed = mu_bed * w_lead_sub
out("lead_line_friction", F_bed, "N", "lead line submerged weight x 0.6 on the bed")
CdA_net = 0.5                         # bunched net and catch moving through water, m2 (assumption)
F_drag = 0.5 * RHO_W * v_haul ** 2 * CdA_net
out("net_drag_in_water", F_drag, "N", "0.5 rho v^2 CdA at 0.4 m/s, CdA 0.5 m2")
bank_deg = math.degrees(math.atan2(-P["z_water"], 1000.0))
th = math.radians(bank_deg)
share_net = 0.2                       # the fisher stacks the net on the table as it arrives (assumption)
m_slope = m_catch + m_weed + share_net * m_net_wet
F_slope = m_slope * g * (mu_land * math.cos(th) + math.sin(th))
out("bank_edge_slope_deg", bank_deg, "deg", "0.5 m rise over 1 m at the water's edge")
out("drag_up_bank_edge", F_slope, "N", "whole catch, weed and a fifth of the wet net on the bank edge")
eta_block = 0.95
F_loop_follow = 2 * (span * P["rope_kg_m"] * g * 0.3) / eta_block ** 2 + 5.0
out("loop_following", F_loop_follow, "N", "the far end drags the loop round both blocks")
F_haul = F_slope + 0.5 * (F_drag + F_bed) + F_loop_follow
out("peak_haul_pull", F_haul, "N", "worst instant: catch on the bank edge, half the net still in water")
ROWS.append(("R3", "Peak pull under 250 N", f"{F_haul:.0f} N (estimate)", "Met on paper", "B"))

# setting: pulling the loop carries the net's far end out and draws the net off the table
F_set = (F_bed + 0.5 * RHO_W * 0.5 ** 2 * 0.1 + 2 * span * P["rope_kg_m"] * g * 0.3 + 5.0) / eta_block ** 2
out("set_pull", F_set, "N", "loop pulled at 0.5 m/s with the net paying out behind the far end")

# ----------------------------------------------------------------------------- C. weak link (R10) and design loads
print("\nC. Weak link and design loads")
wl_nom, wl_tol = 600.0, 0.15
wl_max = wl_nom * (1 + wl_tol)
wl_min = wl_nom * (1 - wl_tol)
out("weak_link_release", wl_nom, "N", "nominal; +/- 15 % (calibrate three samples per batch)")
F_link_normal = F_set + F_loop_follow
out("weak_link_normal_load", F_link_normal, "N", "largest load the link sees in normal use (setting)")
out("weak_link_margin", wl_min / F_link_normal, "x", "lowest release over normal load; no nuisance breaks")
F_far = 2 * wl_max
out("far_end_design_load", F_far, "N", "both legs at the link's highest release, pulling together")
ROWS.append(("R10", "Weak link releases 500 to 700 N", f"{wl_min:.0f} to {wl_max:.0f} N", "Met on paper; calibrate at TRL 4", "C"))
F_bank = 3000.0
out("bank_design_load", F_bank, "N", "R4: horizontal at the near block; covers 2 x link release, debris and a slipped cleat")

# ----------------------------------------------------------------------------- D. bank station (R4)
print("\nD. Bank post, stays and screw anchors (R4)")
ax, ay = P["anchor_xy"]
lug = D["lug_r"]
th_p = math.radians(180 - D["stay_plan_deg"])
Lp = (lug * math.cos(th_p), lug * math.sin(th_p), D["z_lug"])
A = (ax, ay, 60.0)
d = [A[i] - Lp[i] for i in range(3)]
dl = math.sqrt(sum(c * c for c in d))
u = [c / dl for c in d]
out("stay_length", dl / 1000, "m", "lug hole to anchor eye")
out("stay_elevation_deg", math.degrees(math.asin(-u[2])), "deg", "")
T_stay = (F_bank / 2) / (-u[0])
out("stay_tension", T_stay, "N", "each stay, both sharing the 3 kN pull along the line")
out("stay_rope_factor", P["stay_mbs"] * 0.85 / T_stay, "x", "10 mm polyester 22 kN, 85 % at the eye splice")
V_post = 2 * T_stay * (-u[2])
out("post_compression", V_post, "N", "")
E, ro = 210000.0, P["post"][0] / 2
ri = ro - P["post"][1]
I = math.pi / 4 * (ro ** 4 - ri ** 4)
Pcr = math.pi ** 2 * E * I / (P["post_h"] ** 2)
out("post_buckling_factor", Pcr / V_post, "x", "Euler, pinned both ends, 48.3 x 3.2 tube 1.0 m")
su_soft, su_vsoft = 10e3, 5e3         # undrained shear strength: soft wet soil and very soft mud (assumptions)
A_foot = (P["foot"][0] / 1000) ** 2
q_foot = (V_post + 17.2 * g) / A_foot
out("foot_bearing_pressure", q_foot / 1000, "kPa", "350 mm square foot plate")
q_ult = 5.14 * su_soft
out("foot_bearing_factor", q_ult / q_foot, "x", "Nc 5.14 x su 10 kPa")
hd = P["helix"][0] / 1000
depth = (P["helix"][2] + 30) / 1000 * (-u[2])
out("helix_depth", depth, "m", "rod set in line with the stay")
crit = min(0.107 * su_soft / 1000 + 2.5, 7.0)
Fc = min(9.0, 1.2 * depth / hd * 9.0 / (1.2 * crit)) if depth / hd < crit else 9.0
Q_anchor = Fc * su_soft * math.pi * hd ** 2 / 4
out("anchor_capacity", Q_anchor, "N", f"helix {hd*1000:.0f} mm, Fc {Fc:.1f}, su 10 kPa (deep: H/D {depth/hd:.1f})")
out("anchor_factor", Q_anchor / T_stay, "x", "2 or more taken as 'no visible movement'")
ROWS.append(("R4", "Holds 3 kN in soft wet soil without movement", f"anchor factor {Q_anchor / T_stay:.2f} at su 10 kPa",
             "Met on paper; pull test at TRL 4", "D"))
pl, ph, pt, phole = P["pad_eye"]
edge = ro + pl - P["eye_r"]
tau_pad = (2 * F_bank) / (2 * pt * (edge - phole / 2))
out("pad_eye_shear", tau_pad, "MPa", "block load 2 x 3 kN, two shear planes beyond the hole")
blk_load = 2 * F_bank / 2 + F_bank / 2
out("block_load_factor", P["block_wll"] / (2 * 1500.0), "x", "block working load limit over two legs at 1.5 kN")

# ----------------------------------------------------------------------------- E. far stake (R5)
print("\nE. Far stake lateral capacity (R5), Broms short free-head pile in clay")


def broms(c, dd, L, e):
    lo, hi = 0.0, 50000.0
    for _ in range(100):
        H = (lo + hi) / 2
        f = H / (9 * c * dd)
        gg = L - 1.5 * dd - f
        if gg <= 0:
            hi = H
            continue
        if H * (e + 1.5 * dd + 0.5 * f) < 2.25 * c * dd * gg * gg:
            lo = H
        else:
            hi = H
    return H


dd = P["stake"][0] / 1000
e = (P["water_depth"] + P["z_far_above_water"]) / 1000
L_emb = P["embed"] / 1000
for name, c in (("soft", su_soft), ("very_soft", su_vsoft)):
    H = broms(c, dd, L_emb, e)
    out(f"stake_capacity_{name}", H, "N", f"su {c/1000:.0f} kPa, 76.1 mm tube, {L_emb:.1f} m embedded, load {e:.1f} m above the bed")
    out(f"stake_factor_{name}", H / 1500.0, "x", "on the 1.5 kN of R5; 2 or more taken as 'holds'")
# BKH-DDR-003 (R5 option A): where a hand vane reads under 10 kPa the stake is 5.0 m long and driven 3.5 m
L_vs = P["embed_vsoft"] / 1000
H_vs = broms(su_vsoft, dd, L_vs, e)
out("stake_capacity_very_soft_long", H_vs, "N", f"su 5 kPa, {L_vs:.1f} m embedded (5.0 m stake, BKH-DDR-003)")
out("stake_factor_very_soft_long", H_vs / 1500.0, "x", "on the 1.5 kN of R5")
lo_su, hi_su = 1e3, 10e3                 # weakest bed in which the 3.5 m embedment still gives a factor of 2
for _ in range(60):
    mid = (lo_su + hi_su) / 2
    if broms(mid, dd, L_vs, e) / 1500.0 >= 2.0:
        hi_su = mid
    else:
        lo_su = mid
out("su_min_long_stake", hi_su / 1000, "kPa", "weakest bed for a factor of 2 with 3.5 m embedded")
ROWS.append(("R5", "Holds 1.5 kN horizontal in soft mud",
             f"factor {R['stake_factor_soft']:.2f} at su 10 kPa (2.5 m embedded); {R['stake_factor_very_soft_long']:.2f} at su 5 kPa "
             f"with the 5.0 m stake driven 3.5 m where the vane reads under 10 kPa (BKH-DDR-003)",
             "Met on paper; pull test at TRL 4", "E"))
so_, sw = P["stake"]
Z = math.pi / 32 * (so_ ** 4 - (so_ - 2 * sw) ** 4) / so_
for name, c in (("soft", su_soft), ("very_soft", su_vsoft)):
    f = 1500.0 / (9 * c * dd)
    M = 1500.0 * (e + 1.5 * dd + 0.5 * f)
    out(f"stake_stress_{name}", M * 1000 / Z, "MPa", f"at 1.5 kN; S355 tube factor {355 / (M * 1000 / Z):.1f}")
for L2 in (3.0, 3.5):
    H = broms(su_vsoft, dd, L2, e)
    out(f"opt_embed_{L2:.1f}_very_soft", H / 1500.0, "x", f"factor with {L2:.1f} m embedded in very soft mud")
H_pair = 2 * broms(su_vsoft, dd, L_emb, e) * 0.9
out("opt_twin_stake_very_soft", H_pair / 1500.0, "x", "two stakes 1 m apart, tied at the top, 10 % group loss")
m_stake = 26.8
out("stake_mass", m_stake, "kg", "4.0 m of 76.1 x 3.6 tube with point and cap (model)")
m_stake_long = m_stake + 6.4                  # 1.0 m more of 76.1 x 3.6 tube at 6.4 kg/m
out("stake_mass_long", m_stake_long, "kg", "5.0 m stake for very soft beds (BKH-DDR-003)")

# ----------------------------------------------------------------------------- F. loop rope strength and durability (R7)
print("\nF. Loop rope strength and durability (R7)")
T_leg = max(wl_max, 0.5 * F_bank)
uv = 0.5
out("rope_factor_new", P["rope_mbs"] * P["splice_eff"] / T_leg, "x", "at the larger of link release and half the bank load")
out("rope_factor_end_season", P["rope_mbs"] * P["splice_eff"] * uv / T_leg, "x", "after losing half its strength to sun over a season (assumption)")
passes = 2 * 2 * 180
out("sheave_passes_season", passes, "", "two cycles a day, both directions, 180 days")
ROWS.append(("R7", "One season without rope or pulley failure", f"rope factor {R['rope_factor_end_season']:.1f} after UV loss",
             "Met on paper (estimate); season pilot at TRL 4", "F"))

# ----------------------------------------------------------------------------- G. cycle time (R6)
print("\nG. Cycle time (R6), estimate")
t_haul = net_len / 0.25 / 60
t_unclip = 1.0
t_clip = 1.0
t_set = (span / 0.4) / 60
t_tie = 1.0
t_cycle = t_haul + t_unclip + t_clip + t_set + t_tie
out("cycle_time", t_cycle, "min", "haul at 0.25 m/s with stacking, unclip, re-clip, set at 0.4 m/s, cleat and tie off")
t_clear = m_catch / 0.33 * 20 / 60
out("fish_clearing_time", t_clear, "min", "30 fish at 20 s each; same as today and not set by the loop")
ROWS.append(("R6", "Full haul and reset under 10 min", f"{t_cycle:.1f} min (estimate, without clearing fish)",
             "Met on paper (estimate)", "G"))

# ----------------------------------------------------------------------------- H. relocation (R9)
print("\nH. Relocation of the bank anchor (R9), two people, estimate")
steps = {"unscrew two anchors": 4.0, "lift out post and spike": 2.0, "carry up to 50 m": 3.0,
         "set out new spot": 3.0, "screw in two anchors": 6.0, "stand post, fit and tension stays": 4.0}
t_reloc = sum(steps.values())
out("relocation_time", t_reloc, "min", "; ".join(f"{k} {v:.0f}" for k, v in steps.items()))
out("loop_retie_time", 6.0, "min", "retie both ring knots to the new length, extra to R9")
ROWS.append(("R9", "Relocated by two people in under 30 min", f"{t_reloc:.0f} min (estimate)", "Met on paper (estimate)", "H"))

# ----------------------------------------------------------------------------- I. cost (R8) and value engineering
print("\nI. Cost per station (R8)")
bom = list(csv.DictReader(open(ROOT / "bom" / "bom.csv")))
station = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom if "tool" not in r["notes"].lower())
tools = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom if "tool" in r["notes"].lower())
out("station_cost", station, "USD", "all station lines of bom/bom.csv")
out("prototype_cost", station + tools, "USD", "station plus the driving cap")
cost = {r["item"].split(" ", 1)[0]: float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom}
shared = sum(cost[k] for k in ("1", "4", "5", "10", "11", "12")) + cost["13"] * 3 / 6
per_loop = station - shared
out("opt_shared_bank_per_loop", shared / 3 + per_loop, "USD", "one bank post and table serving three loops")
local = {"hardwood post with bolted fittings": 8, "buried timber deadman and strop": 6, "hardwood far pole 4.5 m": 8,
         "two hand-made hardwood sheaves on steel pins": 16, "loop rope for a 30 m span": 30, "two galvanised rings": 4,
         "bridles and weak links": 6, "hardwood cleats": 2, "pole table": 8, "four shackles": 10}
out("opt_local_materials", float(sum(local.values())), "USD", "; ".join(local))
out("station_cost_very_soft", station + 12.0, "USD", "with the 5.0 m stake (1 m more tube, about USD 12, BKH-DDR-003)")
ROWS.append(("R8", "Parts under USD 80 per station",
             f"USD {station:.0f} for the steel trial station (USD {station + 12:.0f} with the 5.0 m stake); "
             "local-materials costing with the co-design partner before the season pilot (BKH-DDR-003)",
             "Not met for the trial station", "I"))

# ----------------------------------------------------------------------------- J. layout and other requirements
print("\nJ. Layout")
out("working_spot_to_water", (P["x_water"] - 1000.0) / 1000, "m", "fisher stands within 1 m of the post; post 6 m from the water")
ROWS.insert(0, ("R1", "Set and haul with nobody in the water", "No step needs anyone in the water once the far stake is set from a boat",
                "Met on paper; field trial at TRL 4", "J"))
ROWS.insert(1, ("R2", "At least 30 m between pulleys; stretch 50 m", "30 m design case; rope bought for 50 m",
                "Met on paper", "A"))
ROWS.append(("R11", "Working spot at least 5 m from the water's edge", f"{R['working_spot_to_water']:.1f} m",
             "Met by layout", "J"))
masses = {"bank post weldment": 17.2, "far stake": m_stake, "two screw anchors": 14.3, "clearing table": 26.4,
          "swivel collar": 1.6, "two blocks": 2 * 1.1, "loop rope (110 m)": 110 * P["rope_kg_m"]}
out("heaviest_lift", max(masses.values()), "kg", "far stake (two people from a boat)")
out("heaviest_lift_very_soft", m_stake_long, "kg", "5.0 m stake in very soft beds (two people from a boat)")
out("station_mass", sum(masses.values()) + 4.0, "kg", "plus about 4 kg of stays, shackles, cleats and fixings")

with open(ROOT / "docs" / "04-calcs" / "results.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["requirement", "target", "result", "status", "section"])
    for row in sorted(ROWS, key=lambda r: int(r[0][1:])):
        w.writerow(row)
print("\nwrote docs/04-calcs/results.csv")
