"""BankHaul parametric model, kit 1.9 interface (STANDARDS section 24), detail level D3 for every option.

Run from the repo root:
    python .kit/cad_check.py --export     fidelity check; STEP per part (chosen option) and per option assembly
    python cad/src/model.py               part counts and masses per option, constructability checks, and the
                                          legacy STEP and STL of the design case in cad/step and cad/stl
    python cad/src/model.py --check       constructability checks only

Axes (site): X runs from the bank post (x = 0) out toward the far stake (+X), Y is across the line, Z is up
with the bank ground at z = 0 and the water surface at z = -500 mm. The loop's two legs run side by side
112 mm apart (y = +56 and y = -56); the clearing table stands landward on the +Y side.

Options (BKH-OPT-001; the choice is proposed, awaiting Amish, BKH-DDR-004):
    A  running rope loop (the current design, BKH-DDR-002 and BKH-DDR-003): a stayed steel post on the bank
       and a driven steel stake carry a swivel block each; a floating loop of two rope halves joined by two
       swivel rings runs between them and carries the net's far end out and back
    B  overhead cableway: a tensioned 8 mm wire rope between a stayed bank mast and a guyed far mast carries a
       two-wheel carriage, hauled out and back by an endless line; the net's far end hangs from the carriage
    C  counterweighted shore lift net: a stayed boom on a bank pivot frame, balanced by a concrete
       counterweight, lowers a 3 m square lift net into the water 5 m out and raises it with a hand line

Every part is a cad_parts.part() dict (made, bought, fastener, weld or context) with an extra "key" naming the
legacy component it belongs to, so docs/04-calcs/sizing.py, cad/src/sheets.py, cad/src/build_plan_media.py and
cad/src/concept_media.py read the same geometry through build_components(). BOM line numbers are given for
option A only. components(option) builds the station in the picture layout (PARAMS "short": 7 m between the
blocks, post 3 m from the water), the layout of every picture, drawing BKH-DWG-003 and cad/fidelity.json;
components(option, short=False) builds the design case (30 m span, post 6 m back). Every part is the same in
both; only the loop, the cable and the far end's position change.

Design changes made in this model are recorded in BKH-DEC-001 (D-S1 to D-S4, under Amish's standing
instruction of 2026-10-23); every other dimension is as decided on 2026-10-03 (BKH-DDR-002, BKH-DDR-003).
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import (Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, Solid, Torus, Vector, Rectangle,  # noqa: E402
                       extrude, loft, export_step, export_stl)
import cad_parts as cp  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402
import bkh_parts as bk  # noqa: E402
from bkh_parts import frame, seg, rope_path, ring_weld, line_weld  # noqa: E402

TITLE = "BankHaul"

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # site layout, design case (R2): span between pulley centres, waterline, water and bed levels
    "edge_board": (250.0, 600.0, 25.0),                 # bank-edge board L (along X) x W x t, BOM 18 (O-2)
    "span": 30000.0, "x_water": 6000.0, "z_water": -500.0, "water_depth": 1000.0,
    "short": {"span": 7000.0, "x_water": 3000.0},       # picture layout
    "span_max": 50000.0,                                  # stretch goal (R2)
    # 6 loop rope: 12 mm floating polypropylene and polyethylene blend ("polysteel"), MBS in N
    "rope_d": 12.0, "rope_mbs": 20000.0, "rope_kg_m": 0.068, "splice_eff": 0.85,
    # 8 blocks: sheave OD, sheave thickness, cheek radius; working load limit in N
    "sheave": (100.0, 16.0), "cheek_r": 65.0, "block_wll": 5000.0,
    # 1 bank post weldment: tube OD x wall, head height; foot plate; spike; cleat bar; lugs
    "post": (48.3, 3.2), "post_h": 1000.0, "foot": (350.0, 8.0), "spike": (20.0, 400.0),
    "cleat_bar": (130.0, 500.0, 8.0, 850.0),     # X depth, Y length, thickness, top height
    "cleat_y": 200.0,                            # jam cleat centres from the post centre line
    "pad_eye": (64.0, 100.0, 8.0, 18.0),         # radial length, height, thickness, hole (D-S1: was 60 long)
    "lug": (60.0, 80.0, 8.0, 15.0),
    "eye_r": 64.0,                                # pad eye hole centre from the post axis (+X)
    "z_block": 950.0,                             # near block sheave plane height
    # 11 screw ground anchors and 5 back-stays: anchor eye plan position, rod, helix
    "anchor_xy": (-1100.0, 450.0), "anchor_rod": (20.0, 1600.0), "helix": (250.0, 8.0, 1400.0),
    "stay_d": 10.0, "stay_mbs": 15600.0,      # D-S5: 1,590 kg three-strand polyester (was taken as 22 kN)
    "turnbuckle": (12.0, 200.0),
    # 2 far stake: tube OD x wall, embedment below the bed, top above the water, point length
    "stake": (76.1, 3.6), "embed": 3500.0, "stake_top": 500.0, "point": 150.0, "pin_d": 12.0,
    "pin_pitch": 200.0,
    # 3 swivel collar: tube OD x wall x length, lug; far block sheave height above the water
    "collar": (88.9, 3.2, 200.0), "z_far_above_water": 200.0, "far_eye_r": 75.0,
    # 4 clearing table: top L x W, height, centre (x, y)
    "table": (1200.0, 600.0, 850.0), "table_xy": (-600.0, 1000.0),
    # 9 swivel rings: body length, eye OD; distance of ring 1 from the near sheave when ready to set
    "swivel": (90.0, 30.0), "ring_gap": 450.0,
    # materials (kg per m^3), used by the legacy mass report
    "rho_steel": 7850.0, "rho_timber": 750.0,
    # option B, overhead cableway (first-order sizes, BKH-OPT-001)
    "B": {"mast_h": 2600.0, "mast": (76.1, 3.6), "far_mast": (114.3, 6.3), "cable_d": 8.0, "sag": 300.0,
          "haul_d": 8.0, "anchor_xy": (-1800.0, 750.0), "guy_dx": 2400.0},
    # option C, counterweighted shore lift net
    "C": {"pivot_z": 2000.0, "arm_long": 8000.0, "arm_short": 3000.0, "boom": (60.0, 100.0, 4.0),
          "frame_y": 350.0, "shaft_d": 40.0, "kingpost_h": 1500.0, "net": 3000.0, "blocks": 6},
}
P = PARAMS

OPTIONS = {"A": "Running rope loop", "B": "Overhead cableway", "C": "Counterweighted shore lift net"}
PRINCIPLES = {
    "A": "A floating rope loop runs round a block on a stayed bank post and a block on a stake driven into the "
         "bed; pulling one leg from the bank carries the net's far end out, and the net is hauled back by hand.",
    "B": "A tensioned wire rope between a stayed bank mast and a guyed far mast carries a wheeled carriage; an "
         "endless haul line pulls the carriage, and the net's far end hanging from it, out and back.",
    "C": "A boom balanced on a pivot frame at the bank, with a concrete counterweight, swings a 3 m square lift "
         "net down into the water 5 m out and back up with a hand line; no line crosses the water.",
}
CHOSEN = "A"      # option A, decided by Amish on 2026-10-25 (BKH-DEC-001 O-1)
OPTION_VIEWS = {
    "A": {"el": 24, "az": -50, "scale": "person", "ground_z": 0},
    "B": {"el": 18, "az": -55, "scale": "person", "ground_z": 0},
    "C": {"el": 20, "az": -60, "scale": "person", "ground_z": 0},
}
# Contacts that are fits by design: a weld bead fused into the plates it joins, and a thimble seated in a
# shackle bow. Pins, bolts and rope eyes have modelled holes and clearances.
ALLOWED_CONTACTS = [("Weld, cap disc", "Pad eye"), ("Weld, cap disc", "Stay lug"), ("thimble", "shackle bow"),
                    ("Weld, mast cap", "lug"), ("Weld, mast cap", "Pad eye")]

STEEL, GALV, SS, TIMBER, ROPE = "painted_steel", "galvanised", "stainless", "hardwood", "rope"


# ----------------------------------------------------------------------------- legacy helpers (other scripts)
def bx(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def ycyl(x, z, r, y0, y1):
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def xcyl(y, z, r, x0, x1):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def zcyl(x, y, r, z0, z1):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def ztube(x, y, ro, ri, z0, z1):
    return zcyl(x, y, ro, z0, z1) - zcyl(x, y, ri, z0 - 1, z1 + 1)


def rod(a, b, r):
    return seg(a, b, r)


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out.fuse(s)
    return out.clean() if hasattr(out, "clean") else out


def rot_z(shape, deg, x=0.0, y=0.0):
    return Pos(x, y, 0) * Rot(0, 0, deg) * Pos(-x, -y, 0) * shape


def ring_xz(x, y, z, ro, ri, t):
    """Flat ring lying in the XZ plane (axis along Y)."""
    return ycyl(x, z, ro, y - t / 2, y + t / 2) - ycyl(x, z, ri, y - t, y + t)


# ----------------------------------------------------------------------------- derived figures
def derived(P=PARAMS):
    D = {}
    so, st = P["sheave"]
    D["r_pitch"] = so / 2 + P["rope_d"] / 2             # rope centre radius round a sheave: 56
    D["leg_y"] = D["r_pitch"]
    D["x_near"] = P["eye_r"] + 152.0                     # near sheave centre: pad eye hole, shackle, block eye, cheeks
    ax, ay = P["anchor_xy"]
    D["stay_plan_deg"] = math.degrees(math.atan2(ay, -ax))
    D["lug_r"] = P["post"][0] / 2 + P["lug"][0] - 20.0
    D["z_lug"] = P["post_h"] - 40.0
    D["stake_len"] = P["water_depth"] + P["embed"] + P["stake_top"]
    D["z_bed"] = P["z_water"] - P["water_depth"]
    D["z_far"] = P["z_water"] + P["z_far_above_water"]
    D["loop_len"] = 2 * P["span"] + 2 * math.pi * D["r_pitch"]
    D["half_len"] = D["loop_len"] / 2
    # far end as assembled: the stop pin sits 6 mm below the collar's nominal bottom (pin holes as drawn), and
    # the collar rests on the stop pin's bolt head and washers, 12.5 mm above the pin's axis (D3 fit)
    co, cw, cl = P["collar"]
    D["z_pin"] = D["z_far"] - cl / 2 - P["pin_d"] / 2
    D["z_collar0"] = D["z_pin"] + 12.5
    D["z_far_m"] = D["z_collar0"] + cl / 2
    D["pin_holes"] = [D["z_pin"] + k * P["pin_pitch"] for k in range(-3, 2)]
    # back-stay chain (D-S3): thimble centres along the stay, from the lug hole to the anchor eye
    th = math.radians(180 - D["stay_plan_deg"])
    L = (D["lug_r"] * math.cos(th), D["lug_r"] * math.sin(th), D["z_lug"])
    A = (ax, ay, 60.0)
    D["stay_chain"] = math.dist(L, A)
    D["stay_eyes"] = D["stay_chain"] - CHAIN_HW
    return D


SH = bk.SHACKLE
# lug pin to upper thimble centre (bow apex + 1.5), lower thimble to its shackle pin (0.5), that shackle's apex
# (51), turnbuckle upper jaw pin (apex + 11), pin to pin (200), lower jaw pin to the anchor eye centre (14)
CHAIN_HW = (SH["apex"] + 1.5) + 0.5 + SH["apex"] + 11.0 + bk.TB["length"] + 14.0


def site(P=PARAMS, short=False):
    L = dict(P)
    if short:
        L.update(P["short"])
    return L


# ----------------------------------------------------------------------------- small builders
def _add(out, name, shape, mat, kind, bom, key, group="bank", explode=(0, 0, 0)):
    p = part(name, shape, mat, kind=kind, bom=bom, group=group, explode=explode)
    p["key"] = key
    out.append(p)
    return p


def _bolt_set(out, d, grip, loc, bom, key, mat=SS, label="", group="bank"):
    for nm, shp in cp.hex_bolt_set(int(d), grip):
        _add(out, f"{nm}{label}", loc * shp, mat, "fastener", bom, key, group)


def _plate_xz(w, h, t, cx, cz, y0, holes=(), r=3.0):
    """Plate w (X) x h (Z) x t (Y from y0 to y0 + t), centred on (cx, cz); holes [(x, z, d)] in site X, Z."""
    loc_holes = [(x - cx, -(z - cz), d) for x, z, d in holes]
    s = cp.sheet(w, h, t, holes=loc_holes, r_corner=r)
    return frame((cx, y0, cz), (0, 1, 0), (1, 0, 0)) * s


def _shackle(out, origin, z_dir, x_dir, name, bom, key, group="bank"):
    """Bow shackle with its pin along the local Y of the frame (z_dir x x_dir) and the bow toward x_dir."""
    bow, pin = bk.shackle()
    # local frame: X = x_dir (bow), Y = pin axis, Z = z_dir
    loc = frame(origin, z_dir, x_dir)
    _add(out, f"{name} shackle bow, 10 mm, galvanised", loc * bow, GALV, "bought", bom, key, group)
    _add(out, f"{name} shackle pin, galvanised", loc * pin, GALV, "fastener", bom, key, group)


def _ring_eye_loop(ring_x, y, z, side, rope_d, axis):
    """A rope's eye threaded through a swivel eye at ring_x: returns (torus, attach point). side -1: the rope
    comes from -X; axis 'y': eye hole along Y (loop lies in XY); axis 'z': eye hole along Z (loop in XZ)."""
    R = 20.0
    c = (ring_x + side * R, y, z)
    tor = Torus(R, rope_d / 2)
    tor = Pos(*c) * (tor if axis == "y" else Rot(90, 0, 0) * tor)
    return tor, (ring_x + side * 2 * R, y, z)


# ----------------------------------------------------------------------------- stay chain (A and B)
def stay_chain(out, L, n_hole, A, rope_d, rope_mat, names, boms, keys, group="bank", wire=False):
    """Lug shackle, upper thimble, stay (rope or wire with grips), lower thimble, lower shackle, jaw-and-jaw
    turnbuckle and the anchor eye's position. L: lug hole centre; n_hole: hole axis; A: anchor eye centre.
    Returns the frame of the anchor eye (local X along the stay toward the anchor, hole axis along local Z)."""
    d = (Vector(*A) - Vector(*L)).normalized()
    n = Vector(*n_hole).normalized()
    zl = d.cross(n)
    dist = (Vector(*A) - Vector(*L)).length
    loc = frame(L, zl, d)                         # local X = d, local Y = n, local Z = d x n
    b_sh, b_th, b_st, b_tb = boms
    k_sh, k_st, k_tb = keys
    bow, pin = bk.shackle()
    _add(out, f"{names} lug shackle bow, 10 mm, galvanised", loc * bow, GALV, "bought", b_sh, k_sh, group)
    _add(out, f"{names} lug shackle pin, galvanised", loc * pin, GALV, "fastener", b_sh, k_sh, group)
    x_t1 = SH["apex"] + 1.5
    x_t2 = dist - (CHAIN_HW - x_t1)
    th = bk.thimble(rope_d)
    _add(out, f"{names} upper thimble, galvanised", loc * Pos(x_t1, 0, 0) * th, GALV, "bought", b_th, k_st, group)
    _add(out, f"{names} lower thimble, galvanised", loc * Pos(x_t2, 0, 0) * th, GALV, "bought", b_th, k_st, group)
    re_ = 6.5 + 2.0 + rope_d / 2
    pieces = [Pos(x_t1, 0, 0) * bk.rope_eye(rope_d), Pos(x_t2, 0, 0) * bk.rope_eye(rope_d)]
    rr = rope_d / 2 + 0.5
    pieces.append(seg((x_t1 + re_ - 1, 0, 0), (x_t2 - re_ + 1, 0, 0), rope_d / 2))
    if wire:     # wire rope: each eye's tail turned back beside the standing part, held by two grips
        for xe, s in ((x_t1 + re_, 1), (x_t2 - re_, -1)):
            pieces.append(seg((xe, 2 * rr, 0), (xe + s * 170, 2 * rr, 0), rope_d / 2))
    _add(out, f"{names} {'wire' if wire else 'rope'}", loc * Compound(pieces), rope_mat, "made", b_st, k_st, group)
    if wire:
        for xe, s in ((x_t1 + re_, 1), (x_t2 - re_, -1)):
            for k in (60, 130):
                for nm, shp, kind in bk.wire_grip(rope_d):
                    _add(out, f"{names} {nm}", loc * Pos(xe + s * k, rr, 0) * shp, GALV, kind, b_st, k_st, group)
    # lower shackle: pin through the lower thimble, bow toward the anchor
    x_p2 = x_t2 + 0.5
    _add(out, f"{names} turnbuckle shackle bow, 10 mm, galvanised", loc * Pos(x_p2, 0, 0) * bow, GALV, "bought",
         b_sh, k_sh, group)
    _add(out, f"{names} turnbuckle shackle pin, galvanised", loc * Pos(x_p2, 0, 0) * pin, GALV, "fastener", b_sh,
         k_sh, group)
    x_j = x_p2 + SH["apex"] + 11.0
    for nm, shp, kind in bk.turnbuckle():
        _add(out, f"{names} {nm}", loc * Pos(x_j, 0, 0) * shp, GALV, kind, b_tb, k_tb, group)
    return loc * Pos(x_j + bk.TB["length"] + 14.0, 0, 0)


# ----------------------------------------------------------------------------- option A
def _bank_weldment(out, P, D):
    ro = P["post"][0] / 2
    H, (fs, ft) = P["post_h"], P["foot"]
    k, b = "post", 1
    tube = cp.round_tube(P["post"][0], P["post"][1], H - ft)
    _add(out, "Post tube 48.3 x 3.2, 992 long", Pos(0, 0, ft) * tube, STEEL, "made", b, k)
    _add(out, "Foot plate 350 x 350 x 8", cp.sheet(fs, fs, ft, r_corner=6), STEEL, "made", b, k)
    sd, sl = P["spike"]
    spike = Pos(0, 0, -(sl - 40)) * cp.round_bar(sd, sl - 40) + \
        Pos(0, 0, -sl) * Solid.make_cone(1.0, sd / 2, 40)
    _add(out, "Ground spike 20 round bar, pointed", spike, STEEL, "made", b, k)
    cap = break_edges(Pos(0, 0, H + 4) * Cylinder(ro + 6, 8), 1.0)
    _add(out, "Cap disc 60 x 8", cap, STEEL, "made", b, k)
    pl, ph, pt, phole = P["pad_eye"]
    pad = _plate_xz(pl, ph, pt, ro + pl / 2, H - ph / 2, -pt / 2, holes=[(P["eye_r"], P["z_block"], phole)])
    _add(out, f"Pad eye 8 mm plate {pl:.0f} x {ph:.0f}, 18 hole", pad, STEEL, "made", b, k)
    ll, lh, lt, lhole = P["lug"]
    lugs = []
    for s in (1, -1):
        lug = _plate_xz(ll, lh, lt, ro + ll / 2, H - lh / 2, -lt / 2, holes=[(D["lug_r"], D["z_lug"], lhole)])
        deg = 180 - s * D["stay_plan_deg"]
        lugs.append((s, deg))
        _add(out, f"Stay lug 8 mm plate, {'left' if s > 0 else 'right'}, 15 hole", Rot(0, 0, deg) * lug, STEEL,
             "made", b, k)
    cx, cy, ct, cz = P["cleat_bar"]
    holes = [(0 - (cx / 2 - 40), 0, P["post"][0] + 0.6)]
    for y in (P["cleat_y"] - 30, P["cleat_y"] + 30, -P["cleat_y"] - 30, -P["cleat_y"] + 30):
        holes.append((40 - (cx / 2 - 40), y, 9.0))
    holes.append((50 - (cx / 2 - 40), 110, 15.0))
    bar = Pos(cx / 2 - 40, 0, cz - ct) * cp.sheet(cx, cy, ct, holes=holes, r_corner=6)
    _add(out, "Cleat bar 130 x 500 x 8 flat", bar, STEEL, "made", b, k)
    w = "mild_steel"
    _add(out, "Weld, post tube to foot plate", ring_weld(ro, 5, (0, 0, ft)), w, "weld", b, k)
    _add(out, "Weld, spike to foot plate", ring_weld(sd / 2, 5, (0, 0, 0), (0, 0, -1)), w, "weld", b, k)
    _add(out, "Weld, cap disc to tube", ring_weld(ro, 4, (0, 0, H), (0, 0, -1)), w, "weld", b, k)
    _add(out, "Weld, cleat bar to tube, top", ring_weld(ro + 0.3, 4, (0, 0, cz)), w, "weld", b, k)
    _add(out, "Weld, cleat bar to tube, underside", ring_weld(ro + 0.3, 4, (0, 0, cz - ct), (0, 0, -1)), w, "weld", b, k)
    for sy in (1, -1):
        _add(out, f"Weld, pad eye to tube {'+Y' if sy > 0 else '-Y'}",
             line_weld((ro, sy * pt / 2, H - ph), (0, 0, 1), ph - 6, 5, (1, 0, 0), (0, sy, 0)), w, "weld", b, k)
        for s, deg in lugs:
            bead = line_weld((ro, sy * lt / 2, H - lh), (0, 0, 1), lh - 6, 5, (1, 0, 0), (0, sy, 0))
            _add(out, f"Weld, stay lug {'left' if s > 0 else 'right'} to tube {'+Y' if sy > 0 else '-Y'}",
                 Rot(0, 0, deg) * bead, w, "weld", b, k)


def _bank_fittings(out, P, D):
    # 10 jam cleats on the cleat bar, 15 four M8 bolt sets
    cx, cy, ct, cz = P["cleat_bar"]
    for s in (1, -1):
        y = s * P["cleat_y"]
        _add(out, f"Jam cleat, {'left' if s > 0 else 'right'} leg, cast aluminium",
             Pos(40, y, cz) * bk.jam_cleat(), "cast_aluminium", "bought", 10, "cleats")
        for dy in (-30, 30):
            _bolt_set(out, 8, 10 + ct, Pos(40, y + dy, cz + 10), 15, "cleats", label=", stainless")
    # 8 near block and 13 its shackle
    blk, _ = bk.swivel_block(D["x_near"], P["z_block"], +1)
    for nm, shp, kind in blk:
        _add(out, f"Near block {nm}", shp, GALV if kind != "bought" or "sheave" not in nm else "hdpe_black", kind, 8,
             "near_block")
    _shackle(out, (P["eye_r"], 0, P["z_block"]), (0, 0, 1), (1, 0, 0), "Near block", 13, "near_shackle")
    # 5 stays, 12 turnbuckles, 13 shackles, 11 screw anchors
    ax, ay = P["anchor_xy"]
    for s in (1, -1):
        th = math.radians(180 - s * D["stay_plan_deg"])
        L = (D["lug_r"] * math.cos(th), D["lug_r"] * math.sin(th), D["z_lug"])
        n = (-s * math.sin(th), s * math.cos(th), 0.0)      # pin tips point toward each other, heads outboard
        A = (ax, s * ay, 60.0)
        side = "left" if s > 0 else "right"
        aloc = stay_chain(out, L, n, A, P["stay_d"], ROPE, f"Back-stay {side},", (13, 5, 5, 12),
                          ("stay_shackles", "stays", "turnbuckles"))
        _add(out, f"Screw ground anchor {side}, 250 helix, 20 rod 1.6 m, galvanised", aloc * bk.screw_anchor(),
             GALV, "bought", 11, "anchors")


def _table(out, P):
    """Clearing table (BOM 4): legs run up to the top boards and the rails are screwed to them (D-S4)."""
    L, W, H = P["table"]
    tx, ty = P["table_xy"]
    T = Pos(tx, ty, 0)
    screws = []           # (point, direction, length, d)
    xl = L / 2 - 75
    for k, b in enumerate(range(5)):
        y0 = -W / 2 + k * 125
        for sx in (-1, 1):
            for dy in (35, 70):
                screws.append(((sx * (xl - 50), y0 + dy, H), (0, 0, -1), 50, 5))
    for sx in (-1, 1):
        for sy in (-1, 1):
            for z in (765, 810):
                screws.append(((sx * xl, sy * W / 2, z), (0, -sy, 0), 50, 5))
            screws.append(((sx * (xl + 25), sy * (W / 2 - 50), 787.5), (-sx, 0, 0), 80, 5))
    for sy in (-1, 1):
        for x in (-450, -150, 150, 450):
            screws.append(((x, sy * (W / 2 - 12.5), H + 75), (0, 0, -1), 100, 6))
    holes = Compound([seg(p, tuple(p[i] + dvec[i] * ln for i in range(3)), d / 2) for p, dvec, ln, d in screws])
    timber = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            timber.append((f"Table leg 50 x 50 x 825, {'+' if sx > 0 else '-'}X {'+' if sy > 0 else '-'}Y",
                           bx(sx * xl - 25, sx * xl + 25, sy * (W / 2 - 50) - 25, sy * (W / 2 - 50) + 25, 0, H - 25)))
    for sy in (-1, 1):
        timber.append((f"Table long rail 75 x 25 x 1,150, {'+' if sy > 0 else '-'}Y",
                       bx(-L / 2 + 25, L / 2 - 25, sy * (W / 2 - 12.5) - 12.5, sy * (W / 2 - 12.5) + 12.5, H - 100, H - 25)))
    for sx in (-1, 1):
        timber.append((f"Table end rail 50 x 75 x 550, {'+' if sx > 0 else '-'}X",
                       bx(sx * (xl - 50) - 25, sx * (xl - 50) + 25, -W / 2 + 25, W / 2 - 25, H - 100, H - 25)))
    for k in range(5):
        y0 = -W / 2 + k * 125
        timber.append((f"Table top board {k + 1}, 100 x 25 x 1,200", bx(-L / 2, L / 2, y0, y0 + 100, H - 25, H)))
    for sy in (-1, 1):
        timber.append((f"Table lip board 25 x 75 x 1,200, {'+' if sy > 0 else '-'}Y",
                       bx(-L / 2, L / 2, sy * (W / 2 - 12.5) - 12.5, sy * (W / 2 - 12.5) + 12.5, H, H + 75)))
    for nm, shp in timber:
        shp = break_edges(shp, 2.0) - holes
        _add(out, nm, T * shp, TIMBER, "made", 4, "table", "table", (0, 0, 300))
    for i, (p, dvec, ln, d) in enumerate(screws):
        s = cp.coach_screw(int(d), ln)
        _add(out, f"Table screw {i + 1}, {d:.0f} x {ln:.0f} galvanised", T * frame(p, tuple(-c for c in dvec)) * s,
             "zinc_plated", "fastener", 4, "table", "table", (0, 0, 300))


def _far_end(out, P, D, S):
    so_, sw = P["stake"]
    ro = so_ / 2
    zb = D["z_bed"]
    z0 = zb - P["embed"]
    z1 = P["z_water"] + P["stake_top"]
    pt = P["point"]
    holes = Compound([Pos(S, 0, zh) * Rot(90, 0, 0) * Cylinder(P["pin_d"] / 2 + 0.25, so_ + 4) for zh in D["pin_holes"]])
    tube = Pos(S, 0, z0 + pt) * cp.round_tube(so_, sw, z1 - z0 - pt) - holes
    _add(out, f"Far stake tube 76.1 x 3.6 S355, {z1 - z0 - pt:,.0f} long, five 12.5 cross holes", tube, STEEL, "made",
         2, "stake", "far")
    outer = loft([Plane.XY.offset(z0 + pt) * Rectangle(so_, so_), Plane.XY.offset(z0 + 0.5) * Rectangle(1, 1)])
    inner = loft([Plane.XY.offset(z0 + pt + 0.01) * Rectangle(so_ - 8.6, so_ - 8.6),
                  Plane.XY.offset(z0 + 16) * Rectangle(0.5, 0.5)])
    _add(out, "Stake point, four 4 mm plates", Pos(S, 0, 0) * (outer - inner), STEEL, "made", 2, "stake", "far")
    cap = break_edges(Pos(S, 0, z1 + 3) * Cylinder(ro, 6), 0.8)
    _add(out, "Stake cap disc 76 x 6", cap, STEEL, "made", 2, "stake", "far")
    _add(out, "Weld, stake cap disc", ring_weld(ro, 4, (S, 0, z1), (0, 0, -1)), "mild_steel", "weld", 2, "stake", "far")
    _add(out, "Weld, stake point", ring_weld(ro, 4, (S, 0, z0 + pt)), "mild_steel", "weld", 2, "stake", "far")
    # 14 stop pin: M12 x 100 bolt, two washers and a nyloc nut through the stake
    _bolt_set(out, 12, so_, frame((S, ro, D["z_pin"]), (0, 1, 0)), 14, "pin", label=", stainless stop pin", group="far")
    # 3 swivel collar with its lug
    co, cw, cl = P["collar"]
    zc0 = D["z_collar0"]
    zf = D["z_far_m"]
    _add(out, "Swivel collar tube 88.9 x 3.2 x 200", Pos(S, 0, zc0) * cp.round_tube(co, cw, cl), STEEL, "made", 3,
         "collar", "far")
    lug = _plate_xz(60, 80, 8, S - co / 2 - 30, zf, -4, holes=[(S - P["far_eye_r"], zf, 18)])
    _add(out, "Collar lug 8 mm plate 60 x 80, 18 hole", lug, STEEL, "made", 3, "collar", "far")
    for sy in (1, -1):
        _add(out, f"Weld, collar lug {'+Y' if sy > 0 else '-Y'}",
             line_weld((S - co / 2, sy * 4, zf - 40), (0, 0, 1), 74, 5, (-1, 0, 0), (0, sy, 0)), "mild_steel", "weld", 3,
             "collar", "far")
    # 13 far shackle and 8 far block
    _shackle(out, (S - P["far_eye_r"], 0, zf), (0, 0, 1), (-1, 0, 0), "Far block", 13, "far_shackle", "far")
    blk, _ = bk.swivel_block(S - P["far_eye_r"] - 152.0, zf, -1)
    for nm, shp, kind in blk:
        _add(out, f"Far block {nm}", shp, "hdpe_black" if "sheave" in nm else GALV, kind, 8, "far_block", "far")


def leg_points(P=PARAMS, short=False, y=0.0):
    """Centre line of one loop leg: near sheave tangent, bank edge, water, far sheave tangent."""
    L = site(P, short)
    D = derived(P)
    zw = P["z_water"]
    r = P["rope_d"] / 2
    x_far_sheave = L["span"] - P["far_eye_r"] - 152.0
    c = P["cheek_r"] + 40.0
    zf = D["z_far_m"]
    return [(D["x_near"], y, P["z_block"]), (D["x_near"] + c, y, P["z_block"]), (L["x_water"], y, r),
            (L["x_water"] + 400.0, y, zw), (x_far_sheave - 1500.0, y, zw), (x_far_sheave - c, y, zf),
            (x_far_sheave, y, zf)]


def _z_on(pts, x):
    for (x0, _, z0), (x1, _, z1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return z0 + (z1 - z0) * (x - x0) / (x1 - x0)
    return pts[-1][2]


def _cut_leg(pts, x_from, x_to):
    """Part of a leg polyline between x_from and x_to (x increasing along the leg)."""
    out = [(x_from, pts[0][1], _z_on(pts, x_from))]
    out += [p for p in pts if x_from < p[0] < x_to]
    out.append((x_to, pts[0][1], _z_on(pts, x_to)))
    return out


def _loop(out, P, D, S, short):
    """Rope loop (6): two halves joined by the two swivel rings (9); net bridle (7) on ring 1."""
    rd = P["rope_d"]
    rp = D["r_pitch"]
    xn, zn = D["x_near"], P["z_block"]
    xf, zf = S - P["far_eye_r"] - 152.0, D["z_far_m"]
    lo = leg_points(P, short, -rp)
    hi = leg_points(P, short, rp)
    x1, x2 = xn + P["ring_gap"], xf - P["ring_gap"]
    z1, z2 = _z_on(lo, x1), _z_on(hi, x2)
    sl, so = P["swivel"]
    rings = []
    for nm, x, y, z, flip in (("1 (setting leg)", x1, -rp, z1, False), ("2", x2, rp, z2, True)):
        body = Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(9.0, sl - 32)
        eA = Pos(x - 37, y, z) * Rot(90, 0, 0) * (Cylinder(so / 2, 6) - Cylinder(so / 2 - 6, 8))     # hole along Y
        eB = Pos(x + 37, y, z) * (Cylinder(so / 2, 6) - Cylinder(so / 2 - 6, 8))                     # hole along Z
        sw = body.fuse(eA, eB)
        if flip:
            sw = Pos(x, y, z) * Rot(0, 0, 180) * Pos(-x, -y, -z) * sw
        rings.append(sw)
        _add(out, f"Swivel ring {nm}, eye to eye, galvanised", break_edges(sw, 0.5), GALV, "bought", 9, "rings", "loop")
    # ring 1: rope from the near block joins eye A (from -X, hole along Y); rope to the far end joins eye B (+X, Z)
    t1a, p1a = _ring_eye_loop(x1 - 37, -rp, z1, -1, rd, "y")
    t1b, p1b = _ring_eye_loop(x1 + 37, -rp, z1, +1, rd, "z")
    # ring 2 is turned round: rope from the far block joins its eye A on +X; rope to the near block eye B on -X
    t2a, p2a = _ring_eye_loop(x2 + 37, rp, z2, +1, rd, "y")
    t2b, p2b = _ring_eye_loop(x2 - 37, rp, z2, -1, rd, "z")
    # half 1: ring 1 -> far block (leg -56) -> far wrap -> leg +56 back to ring 2
    wrap_f = (Pos(xf, 0, zf) * Torus(rp, rd / 2)) & bx(xf, xf + rp + 20, -rp - 20, rp + 20, zf - 20, zf + 20)
    wrap_n = (Pos(xn, 0, zn) * Torus(rp, rd / 2)) & bx(xn - rp - 20, xn, -rp - 20, rp + 20, zn - 20, zn + 20)
    lo_out = [p1b] + _cut_leg(lo, p1b[0] + 1, xf)[1:]
    hi_back = [p2a] + _cut_leg(hi, p2a[0] + 1, xf)[1:]
    h1 = Compound([t1b, rope_path(lo_out, rd), wrap_f, rope_path(hi_back, rd), t2a])
    lo_in = _cut_leg(lo, xn, p1a[0] - 1)[:-1] + [p1a]
    hi_in = _cut_leg(hi, xn, p2b[0] - 1)[:-1] + [p2b]
    h2 = Compound([t2b, rope_path(hi_in, rd), wrap_n, rope_path(lo_in, rd), t1a])
    _add(out, "Rope loop half 1, 12 mm floating polysteel, spliced eye on ring 1", h1, ROPE, "made", 6, "loop", "loop")
    _add(out, "Rope loop half 2, 12 mm floating polysteel, spliced eye on ring 2", h2, ROPE, "made", 6, "loop", "loop")
    # 7 net bridle on ring 1: snap hook round the swivel body, weak link, bridle cord to the net on the table
    hook = Pos(x1, -rp, z1) * Rot(0, 90, 0) * Torus(14.0, 3.0)
    hook = hook.fuse(seg((x1, -rp, z1 - 17), (x1, -rp - 10, z1 - 75), 3.5))
    _add(out, "Net bridle snap hook 60 mm, stainless", hook, SS, "bought", 7, "bridle", "loop")
    wl = Pos(x1, -rp - 10, z1 - 105) * Rot(90, 0, 0) * Torus(26.0, 1.5)
    _add(out, "Net bridle weak link, braided cord loop, 500 to 700 N", wl, ROPE, "made", 7, "bridle", "loop")
    tx, ty = P["table_xy"]
    tl, tw, th = P["table"]
    over = (tx + tl / 2 - 150, ty - tw / 2 - 30, th + 100)
    end = (tx + tl / 2 - 150, ty - tw / 2 + 150, th + 80)
    cord = rope_path([(x1, -rp - 10, z1 - 136), (x1 - 150, -rp - 120, z1 - 260), over, end], 6.0)
    _add(out, "Net bridle cord 6 mm polyester", cord, ROPE, "made", 7, "bridle", "loop")


def option_a(P=PARAMS, short=True):
    L = site(P, short)
    D = derived(P)
    out = []
    _bank_weldment(out, P, D)
    _bank_fittings(out, P, D)
    _table(out, P)
    _far_end(out, P, D, L["span"])
    _loop(out, P, D, L["span"], short)
    _edge_board(out, P, L)
    return out


def _edge_board(out, P, L):
    """Bank-edge board (BOM 18; O-2, decided by Amish 2026-10-25): a smooth hardwood board set flush into the bank
    lip under both loop legs, its nose rounded, so the catch and weed slide over the edge instead of dragging."""
    xw = L["x_water"]
    bl, bw, bt = P["edge_board"]
    board = bx(xw - bl, xw, -bw / 2, bw / 2, -bt, 0.0)
    _add(out, f"Bank-edge board, smooth hardwood {bl:.0f} x {bw:.0f} x {bt:.0f}, set flush at the bank lip",
         break_edges(board, 10.0), TIMBER, "made", 18, "edge_board", "bank")


# ----------------------------------------------------------------------------- option B
def _mast(out, x, od, wall, z_foot, z_top, name, group, point_len=0.0, foot=None, key="mast"):
    """A vertical tube mast with cap disc and either a foot plate with spike (bank) or a driven point (bed)."""
    ro = od / 2
    w = "mild_steel"
    if foot:
        fs, ft = foot
        _add(out, f"{name} foot plate {fs:.0f} x {fs:.0f} x {ft:.0f}", Pos(x, 0, z_foot) * cp.sheet(fs, fs, ft, r_corner=6),
             STEEL, "made", None, key, group)
        _add(out, f"{name} ground spike 24 round bar", Pos(x, 0, z_foot - 450) * cp.round_bar(24, 450), STEEL, "made", None,
             key, group)
        _add(out, f"Weld, {name.lower()} to foot plate", ring_weld(ro, 6, (x, 0, z_foot + ft)), w, "weld", None, key, group)
        _add(out, f"Weld, {name.lower()} spike", ring_weld(12, 5, (x, 0, z_foot), (0, 0, -1)), w, "weld", None, key, group)
        z0 = z_foot + ft
    else:
        z0 = z_foot
        outer = loft([Plane.XY.offset(z0) * Rectangle(od, od), Plane.XY.offset(z0 - point_len + 0.5) * Rectangle(1, 1)])
        inner = loft([Plane.XY.offset(z0 + 0.01) * Rectangle(od - 10, od - 10),
                      Plane.XY.offset(z0 - point_len + 20) * Rectangle(0.5, 0.5)])
        _add(out, f"{name} point, four 5 mm plates", Pos(x, 0, 0) * (outer - inner), STEEL, "made", None, key, group)
        _add(out, f"Weld, {name.lower()} point", ring_weld(ro, 5, (x, 0, z0)), w, "weld", None, key, group)
    _add(out, f"{name} tube {od} x {wall}, {z_top - z0:,.0f} long", Pos(x, 0, z0) * cp.round_tube(od, wall, z_top - z0),
         STEEL, "made", None, key, group)
    _add(out, f"{name} cap disc", break_edges(Pos(x, 0, z_top + 4) * Cylinder(ro + 4, 8), 1.0), STEEL, "made", None,
         key, group)
    _add(out, f"Weld, mast cap {name.lower()}", ring_weld(ro, 4, (x, 0, z_top), (0, 0, -1)), w, "weld", None, key, group)


def _lug_on_mast(out, x, ro, z, deg, length, height, hole_r, hole_d, name, group, key="mast", zoff=0.0, r=3.0):
    """8 mm lug plate welded to a mast, pointing at plan angle deg, hole hole_r from the mast axis at height z;
    the plate is centred zoff above the hole (raised clear of a steep stay's eye) with corner radius r."""
    lug = _plate_xz(length, height, 8, ro + length / 2, z + zoff, -4, holes=[(hole_r, z, hole_d)], r=r)
    _add(out, name, Pos(x, 0, 0) * Rot(0, 0, deg) * lug, STEEL, "made", None, key, group)
    for sy in (1, -1):
        bead = line_weld((ro, sy * 4, z + zoff - height / 2), (0, 0, 1), height - 6, 5, (1, 0, 0), (0, sy, 0))
        _add(out, f"Weld, {name.split(',')[0].lower()} {'+Y' if sy > 0 else '-Y'}", Pos(x, 0, 0) * Rot(0, 0, deg) * bead,
             "mild_steel", "weld", None, key, group)


def option_b(P=PARAMS, short=True):
    Ls = site(P, short)
    D = derived(P)
    B = P["B"]
    S, zw = Ls["span"], P["z_water"]
    out = []
    mo, mw = B["mast"]
    ro = mo / 2
    H = B["mast_h"]
    # bank mast with foot plate and spike
    _mast(out, 0.0, mo, mw, 0.0, H, "Bank mast", "bank", foot=(400.0, 10.0))
    z_cab = H - 100.0
    _lug_on_mast(out, 0.0, ro, z_cab, 0.0, 70, 90, ro + 45, 15, "Cable lug, 8 mm plate, 15 hole", "bank")
    z_st = H - 160.0
    ax, ay = B["anchor_xy"]
    pdeg = math.degrees(math.atan2(ay, -ax))
    for s in (1, -1):
        _lug_on_mast(out, 0.0, ro, z_st, 180 - s * pdeg, 60, 80, ro + 40, 15,
                     f"Stay lug {'left' if s > 0 else 'right'}, 8 mm plate, 15 hole", "bank", zoff=18.0, r=16.0)
    z_hb = 950.0
    _lug_on_mast(out, 0.0, ro, z_hb, 0.0, 64, 100, ro + 40, 18, "Pad eye, haul block, 8 mm plate", "bank")
    # bank stays to screw anchors
    for s in (1, -1):
        th = math.radians(180 - s * pdeg)
        Lh = (ro + 40) * math.cos(th), (ro + 40) * math.sin(th), z_st
        n = (-math.sin(th), math.cos(th), 0.0)
        A = (ax, s * ay, 60.0)
        side = "left" if s > 0 else "right"
        aloc = stay_chain(out, Lh, n, A, 10.0, ROPE, f"Mast stay {side},", (None,) * 4, ("stay", "stay", "stay"))
        _add(out, f"Screw ground anchor {side}, mast stay", aloc * bk.screw_anchor(), GALV, "bought", None, "anchor")
    # far mast: driven tube with a point, top 3.0 m above the water
    fo, fw = B["far_mast"]
    fro = fo / 2
    xf = S
    zb = D["z_bed"]
    zt = zw + 3000.0
    _mast(out, xf, fo, fw, zb - 3500.0, zt, "Far mast", "far", point_len=180.0, key="far mast")
    _lug_on_mast(out, xf, fro, zt - 100.0, 180.0, 70, 90, fro + 45, 15, "Far cable lug, 8 mm plate, 15 hole", "far",
                 key="far mast")
    _lug_on_mast(out, xf, fro, zt - 160.0, 0.0, 60, 90, fro + 38, 15, "Guy lug, 8 mm plate, 15 hole", "far",
                 key="far mast", zoff=24.0, r=18.0)
    _lug_on_mast(out, xf, fro, zt - 260.0, 180.0, 64, 100, fro + 40, 18, "Pad eye, far haul block, 8 mm plate", "far",
                 key="far mast")
    # far guy: wire rope with turnbuckle to a screw anchor in the bed beyond the mast
    Lg = (xf + fro + 38, 0.0, zt - 160.0)
    Ag = (xf + B["guy_dx"], 0.0, zb + 60.0)
    aloc = stay_chain(out, Lg, (0, 1, 0), Ag, B["cable_d"], GALV, "Far guy,", (None,) * 4, ("guy", "guy", "guy"),
                      group="far", wire=True)
    _add(out, "Screw ground anchor, far guy, set in the bed", aloc * bk.screw_anchor(), GALV, "bought", None, "anchor",
         "far")
    # track cable: bank cable lug -> turnbuckle-free chain (shackle, thimble, wire, thimble, shackle) -> far lug
    Lc = (ro + 45, 0.0, z_cab)
    Fc = (xf - fro - 45, 0.0, zt - 100.0)
    cd = B["cable_d"]
    for nm, p0, dx in (("bank", Lc, 1), ("far", Fc, -1)):
        _shackle(out, p0, (0, 0, 1), (dx, 0, 0), f"Track cable {nm}", None, "cable")
    th = bk.thimble(cd)
    t1 = (Lc[0] + 52.5, 0, z_cab)
    t2 = (Fc[0] - 52.5, 0, Fc[2])
    _add(out, "Track cable thimble, bank, galvanised", Pos(*t1) * th, GALV, "bought", None, "cable")
    _add(out, "Track cable thimble, far, galvanised", Pos(*t2) * Rot(0, 0, 180) * th, GALV, "bought", None, "cable", "far")
    re_ = 6.5 + 2.0 + cd / 2
    a, b = (t1[0] + re_, 0, z_cab), (t2[0] - re_, 0, t2[2])
    mid = ((a[0] + b[0]) / 2, 0.0, (a[2] + b[2]) / 2 - B["sag"])
    a2, b2 = (a[0] + 320, 0.0, a[2]), (b[0] - 320, 0.0, b[2])      # straight past the grips, then the sag
    pts = [a, a2]
    for i in range(1, 12):
        u = i / 12
        x = a2[0] + (b2[0] - a2[0]) * u
        pts.append((x, 0.0, a2[2] + (b2[2] - a2[2]) * u - 4 * B["sag"] * u * (1 - u)))
    pts += [b2, b]
    rr = cd / 2 + 0.5
    cable = Compound([Pos(*t1) * bk.rope_eye(cd), Pos(*t2) * bk.rope_eye(cd), rope_path(pts, cd),
                      seg((a[0], 2 * rr, a[2]), (a[0] + 230, 2 * rr, a[2]), cd / 2),
                      seg((b[0] - 230, 2 * rr, b[2]), (b[0], 2 * rr, b[2]), cd / 2)])
    _add(out, "Track cable 8 mm galvanised wire rope", cable, GALV, "made", None, "cable")
    for xe, z, s, g in ((a[0], a[2], 1, "bank"), (b[0], b[2], -1, "far")):
        for k in (80, 170):
            for nm, shp, kind in bk.wire_grip(cd):
                _add(out, f"Track cable {g} {nm}", Pos(xe + s * k, rr, z) * shp, GALV, kind, None, "cable", g)
    # carriage on the cable at mid-span
    xm, zm = mid[0], mid[2]
    zc = zm + cd / 2 - cd / 2          # cable centre at mid-span
    for sy in (1, -1):
        pl = _plate_xz(150, 110, 6, xm, zc + 8, 11 if sy > 0 else -17,
                       holes=[(xm - 40, zc + 30.5, 12.5), (xm + 40, zc + 30.5, 12.5), (xm, zc - 20, 12.5),
                              (xm - 60, zc - 25, 10), (xm + 60, zc - 25, 10)], r=10)
        _add(out, f"Carriage side plate {'+Y' if sy > 0 else '-Y'}, 6 mm", pl, GALV, "made", None, "carriage", "carriage")
    for nm, xw in (("rear", xm - 40), ("front", xm + 40)):
        wheel = Pos(xw, 0, zc + 30.5) * Rot(90, 0, 0) * cp.pulley(60, 20, 12)
        _add(out, f"Carriage wheel {nm}, 60 mm grooved, nylon", wheel, "hdpe_black", "bought", None, "carriage", "carriage")
        _bolt_set(out, 12, 34, frame((xw, 17, zc + 30.5), (0, 1, 0)), None, "carriage", mat=GALV, label=f", {nm} axle",
                  group="carriage")
    _bolt_set(out, 12, 34, frame((xm, 17, zc - 20), (0, 1, 0)), None, "carriage", mat=GALV, label=", keeper under the cable",
              group="carriage")
    # drop line with weak link and snap hook for the net's far end
    drop = Compound([Pos(xm, 0, zc - 20) * Rot(90, 0, 0) * Torus(10.5, 4.0),
                     rope_path([(xm, 0, zc - 30.5), (xm, 0, zc - 1400)], 8.0)])
    _add(out, "Drop line 8 mm polyester", drop, ROPE, "made", None, "carriage", "carriage")
    _add(out, "Drop line weak link, 500 to 700 N", Pos(xm, 0, zc - 1432) * Rot(90, 0, 0) * Torus(26.0, 1.5), ROPE, "made",
         None, "carriage", "carriage")
    hook = Pos(xm, 0, zc - 1462) * Rot(0, 90, 0) * Torus(12.0, 3.0)
    _add(out, "Drop line snap hook 60 mm, stainless", hook.fuse(seg((xm, 0, zc - 1474), (xm, 0, zc - 1535), 3.5)), SS,
         "bought", None, "carriage", "carriage")
    # haul blocks and the endless haul line
    hd = B["haul_d"]
    xhb = ro + 40 + 152.0
    blk, _ = bk.swivel_block(xhb, z_hb, +1, dict(bk.BLOCK, rope_d=hd))
    for nm, shp, kind in blk:
        _add(out, f"Bank haul block {nm}", shp, "hdpe_black" if "sheave" in nm else GALV, kind, None, "haul")
    _shackle(out, (ro + 40, 0, z_hb), (0, 0, 1), (1, 0, 0), "Bank haul block", None, "haul")
    zfb = zt - 260.0
    xfb = xf - fro - 40 - 152.0
    blk, _ = bk.swivel_block(xfb, zfb, -1, dict(bk.BLOCK, rope_d=hd))
    for nm, shp, kind in blk:
        _add(out, f"Far haul block {nm}", shp, "hdpe_black" if "sheave" in nm else GALV, kind, None, "haul", "far")
    _shackle(out, (xf - fro - 40, 0, zfb), (0, 0, 1), (-1, 0, 0), "Far haul block", None, "haul", "far")
    rp = 50.0 + hd / 2
    # out-haul from the bank block's -Y side to the carriage's rear hole; return from the carriage front hole round
    # the far block and back to the bank block's +Y side
    ta, pa = _ring_eye_loop(xm - 60, -14.0, zc - 25, -1, hd, "y")
    tb, pb = _ring_eye_loop(xm + 60, -14.0, zc - 25, +1, hd, "y")
    wrap_n = (Pos(xhb, 0, z_hb) * Torus(rp, hd / 2)) & bx(xhb - rp - 20, xhb, -rp - 20, rp + 20, z_hb - 20, z_hb + 20)
    wrap_f = (Pos(xfb, 0, zfb) * Torus(rp, hd / 2)) & bx(xfb, xfb + rp + 20, -rp - 20, rp + 20, zfb - 20, zfb + 20)
    line = Compound([ta, tb, wrap_n, wrap_f,
                     rope_path([(xhb, -rp, z_hb), (xhb + 110, -rp, z_hb), pa], hd),
                     rope_path([pb, (xfb - 110, -rp, zfb), (xfb, -rp, zfb)], hd),
                     rope_path([(xfb, rp, zfb), (xfb - 110, rp, zfb), (xhb + 110, rp, z_hb), (xhb, rp, z_hb)], hd)])
    _add(out, "Endless haul line 8 mm polyester", line, ROPE, "made", None, "haul")
    # jam cleats for the haul line on a cleat bar round the mast
    cz = 850.0
    holes = [(-(65 - 40), 0, mo + 0.6)] + [(40 - 25, y, 9.0) for y in (170, 230, -170, -230)]
    _add(out, "Haul cleat bar 130 x 500 x 8 flat", Pos(25, 0, cz - 8) * cp.sheet(130, 500, 8, holes=holes, r_corner=6),
         STEEL, "made", None, "mast")
    _add(out, "Weld, haul cleat bar top", ring_weld(ro + 0.3, 4, (0, 0, cz)), "mild_steel", "weld", None, "mast")
    for s in (1, -1):
        _add(out, f"Haul jam cleat {'left' if s > 0 else 'right'}", Pos(40, s * 200, cz) * bk.jam_cleat(), "cast_aluminium",
             "bought", None, "haul")
        for dy in (-30, 30):
            _bolt_set(out, 8, 18, Pos(40, s * 200 + dy, cz + 10), None, "haul", label=", haul cleat")
    return out


# ----------------------------------------------------------------------------- option C
def option_c(P=PARAMS, short=True):
    Ls = site(P, short)
    C = P["C"]
    out = []
    zp = C["pivot_z"]
    fy = C["frame_y"]
    xp = Ls["x_water"] - 3000.0           # pivot 3 m back from the water's edge
    w = "mild_steel"
    G = "frame"
    # skids, cross members and ground stakes
    for sy in (1, -1):
        sk = frame((xp - 1200, sy * fy, 25), (1, 0, 0), (0, 1, 0)) * cp.rhs(100, 50, 4, 2400)
        sk = sk - Compound([Pos(xp + x, sy * fy, 25) * Cylinder(11, 60) for x in (-1100, 1100)])
        _add(out, f"Skid RHS 100 x 50 x 4, 2,400 long, {'+Y' if sy > 0 else '-Y'}", sk, STEEL, "made", None, "frame", G)
        for x in (-1100, 1100):
            st = Pos(xp + x, sy * fy, -550) * cp.round_bar(20, 600)
            st = st.fuse(Pos(xp + x, sy * fy, 50 + 5) * Cylinder(20, 10))
            _add(out, f"Ground stake 20 round bar with head, {x:+.0f} {'+Y' if sy > 0 else '-Y'}", st, GALV, "bought", None,
                 "frame", G)
    for x in (-900, 900):
        cm = frame((xp + x, -fy - 50, 75), (0, 1, 0), (1, 0, 0)) * cp.shs(50, 3, 2 * fy + 100)
        _add(out, f"Cross member SHS 50 x 3 at {x:+.0f}", cm, STEEL, "made", None, "frame", G)
        for sy in (1, -1):
            for sx in (1, -1):
                _add(out, f"Weld, cross member {x:+.0f} to skid {'+Y' if sy > 0 else '-Y'} {'+' if sx > 0 else '-'}X",
                     line_weld((xp + x + sx * 25, sy * fy - 50, 50), (0, 1, 0), 100, 4, (sx, 0, 0), (0, 0, 1)), w, "weld",
                     None, "frame", G)
    # A-frame legs (SHS 60 x 4, mitred to the skid and the head plate) and head plates
    for sy in (1, -1):
        for sx in (1, -1):
            a = Vector(xp + sx * 1000, sy * fy, 50)
            b = Vector(xp + sx * 60, sy * fy, zp - 100)
            dv = (b - a)
            ext = 120.0
            leg = frame(a - dv.normalized() * ext, dv, (0, 1, 0)) * cp.shs(60, 4, dv.length + 2 * ext)
            leg = leg & bx(xp - 1300, xp + 1300, sy * fy - 40, sy * fy + 40, 50, zp - 100)
            _add(out, f"A-frame leg SHS 60 x 4, {'+' if sx > 0 else '-'}X {'+Y' if sy > 0 else '-Y'}", leg, STEEL, "made",
                 None, "frame", G)
            foot = 60 / math.cos(math.atan2(940, zp - 150))
            x0 = a.X - foot / 2
            for side in (1, -1):
                _add(out, f"Weld, leg {'+' if sx > 0 else '-'}X {'+Y' if sy > 0 else '-Y'} to skid {side:+d}",
                     line_weld((x0, sy * fy + side * 30, 50), (1, 0, 0), foot, 5, (0, side, 0), (0, 0, 1)), w, "weld", None,
                     "frame", G)
        plate = _plate_xz(300, 250, 10, xp, zp + 25, sy * fy - 5, holes=[(xp, zp, 41)])
        _add(out, f"Pivot head plate 10 mm, {'+Y' if sy > 0 else '-Y'}", plate, STEEL, "made", None, "frame", G)
    # boom (RHS 60 x 100 x 4) with its pivot holes, bushes, spacers, pivot pin and split pin
    bw, bh, bt = C["boom"]
    x0, x1 = xp - C["arm_short"], xp + C["arm_long"]
    boom = frame((x0, 0, zp), (1, 0, 0), (0, 1, 0)) * cp.rhs(bw, bh, bt, x1 - x0)
    boom = boom - Pos(xp, 0, zp) * Rot(90, 0, 0) * Cylinder(25, bw + 10)
    boom = boom - Compound([Pos(x0 + 450, 0, zp + dz) * Rot(90, 0, 0) * Cylinder(6.5, bw + 10) for dz in (-25, 25)])
    _add(out, f"Boom RHS 100 x 60 x 4, {x1 - x0:,.0f} long", boom, STEEL, "made", None, "boom", "boom")
    for sy in (1, -1):
        _add(out, f"Pivot bush {'+Y' if sy > 0 else '-Y'}, 50 x 40, UHMW-PE",
             frame((xp, sy * (bw / 2 - 30) if sy > 0 else -bw / 2, zp), (0, 1, 0)) * cp.bush(50, 40, 30), "hdpe_natural",
             "bought", None, "boom", "boom")
        sp = frame((xp, sy * bw / 2, zp), (0, sy, 0)) * cp.round_tube(60, 8, fy - 5 - bw / 2)
        _add(out, f"Pivot spacer tube 60 x 8, {'+Y' if sy > 0 else '-Y'}", sp, STEEL, "made", None, "boom", "boom")
    sd = C["shaft_d"]
    grip = 2 * fy + 10
    pin = frame((xp, fy + 8.0, zp), (0, 1, 0)) * cp.clevis_pin(int(sd), grip)
    _add(out, f"Pivot pin 40 mm, {grip:.0f} grip", pin, STEEL, "bought", None, "boom", "boom")
    _add(out, "Pivot split pin", Pos(xp, fy + 8.0 - grip - sd, zp) * cp.split_pin(sd), STEEL, "fastener", None, "boom",
         "boom")
    # king post and its two wire stays
    ztop = zp + bh / 2
    kp_h = C["kingpost_h"]
    _add(out, "King post tube 60.3 x 3.6", Pos(xp + 200, 0, ztop) * cp.round_tube(60.3, 3.6, kp_h), STEEL, "made", None,
         "boom", "boom")
    _add(out, "Weld, king post to boom", ring_weld(30.15, 5, (xp + 200, 0, ztop)), w, "weld", None, "boom", "boom")
    _add(out, "King post cap disc", break_edges(Pos(xp + 200, 0, ztop + kp_h + 4) * Cylinder(34, 8), 1.0), STEEL, "made",
         None, "boom", "boom")
    _add(out, "Weld, mast cap king post", ring_weld(30.15, 4, (xp + 200, 0, ztop + kp_h), (0, 0, -1)), w, "weld", None,
         "boom", "boom")
    zl = ztop + kp_h - 60
    for nm, sx, xa in (("tip", 1, x1 - 300), ("tail", -1, x0 + 300)):
        lug = _plate_xz(60, 70, 8, xp + 200 + sx * (30.15 + 30), zl, -4, holes=[(xp + 200 + sx * (30.15 + 40), zl, 15)])
        _add(out, f"King post lug, {nm} stay", lug, STEEL, "made", None, "boom", "boom")
        blug = _plate_xz(50, 70, 8, xa + sx * 5, ztop + 35, -4, holes=[(xa, ztop + 45, 15)])
        _add(out, f"Boom lug, {nm} stay", blug, STEEL, "made", None, "boom", "boom")
        for sy in (1, -1):
            _add(out, f"Weld, boom lug {nm} {'+Y' if sy > 0 else '-Y'}",
                 line_weld((xa + sx * 5 - 25, sy * 4, ztop), (1, 0, 0), 50, 5, (0, sy, 0), (0, 0, 1)), w, "weld", None, "boom",
                 "boom")
            _add(out, f"Weld, king post lug {nm} {'+Y' if sy > 0 else '-Y'}",
                 Pos(xp + 200, 0, 0) * Rot(0, 0, 0 if sx > 0 else 180) *
                 line_weld((30.15, sy * 4, zl - 35), (0, 0, 1), 64, 5, (1, 0, 0), (0, sy, 0)), w, "weld", None, "boom", "boom")
        Lk = (xp + 200 + sx * (30.15 + 40), 0.0, zl)
        Ab = (xa, 0.0, ztop + 45)
        _wire_tie(out, Lk, Ab, 8.0, f"King post {nm} stay", "boom")
    # counterweight basket under the tail, hung on two straps bolted through the boom
    xc = x0 + 450
    zb0 = zp - bh / 2 - 900
    base = Pos(xc, 0, zb0) * cp.sheet(520, 470, 5, r_corner=8)
    _add(out, "Counterweight basket base 5 mm plate", base, STEEL, "made", None, "counterweight", "boom")
    for sx in (1, -1):
        for sy in (1, -1):
            an = Pos(xc + sx * 260, sy * 235, zb0 + 5) * Rot(0, 0, 180 if (sx > 0 and sy > 0) else -90 if sx < 0 and sy > 0
                                                             else 90 if sx > 0 and sy < 0 else 0) * cp.angle(40, 40, 4, 395)
            _add(out, f"Basket corner angle 40 x 40 x 4, {'+' if sx > 0 else '-'}X {'+' if sy > 0 else '-'}Y", an, STEEL,
                 "made", None, "counterweight", "boom")
    ztop_b = zb0 + 400
    for sy in (1, -1):
        rail = Pos(0, -sy * 4, 0) * frame((xc - 260, sy * 235, ztop_b + 20), (1, 0, 0), (0, 1, 0)) * cp.flat_bar(8, 40, 520)
        _add(out, f"Basket top rail 40 x 8, {'+Y' if sy > 0 else '-Y'}", rail, STEEL, "made", None, "counterweight", "boom")
    hb = frame((xc, -239, ztop_b + 44), (0, 1, 0), (1, 0, 0)) * cp.flat_bar(50, 8, 478)
    _add(out, "Basket hanger bar 50 x 8", hb, STEEL, "made", None, "counterweight", "boom")
    zs0 = ztop_b + 48
    for sy in (1, -1):
        strap = Pos(xc, sy * (bw / 2 + 4), zs0) * cp.flat_bar(50, 8, zp + bh / 2 - 10 - zs0)
        strap = strap - Compound([Pos(xc, sy * (bw / 2 + 4), zp + dz) * Rot(90, 0, 0) * Cylinder(6.5, 20) for dz in (-25, 25)])
        _add(out, f"Basket strap 50 x 8, {'+Y' if sy > 0 else '-Y'}", strap, STEEL, "made", None, "counterweight", "boom")
        for sx in (1, -1):
            _add(out, f"Weld, strap {'+Y' if sy > 0 else '-Y'} to hanger bar {'+' if sx > 0 else '-'}X",
                 line_weld((xc + sx * 25, sy * (bw / 2), zs0), (0, sy, 0), 8, 5, (sx, 0, 0), (0, 0, 1)), w, "weld", None,
                 "counterweight", "boom")
    for dz in (-25, 25):
        _bolt_set(out, 12, bw + 16, frame((xc, bw / 2 + 8, zp + dz), (0, 1, 0)), None, "counterweight", mat=GALV,
                  label=", basket strap", group="boom")
    n = C["blocks"]
    for i in range(n):
        lay, side = divmod(i, 2)
        blk = Pos(xc, (side - 0.5) * 210, zb0 + 5 + 50 + lay * 101) * Box(400, 200, 100)
        _add(out, f"Counterweight block {i + 1}, 400 x 200 x 100 concrete", break_edges(blk, 4.0), "concrete", "made", None,
             "counterweight", "boom")
    # hand line from a pad eye under the tail to the fisher's hand
    pe = _plate_xz(70, 60, 8, x0 + 80, zp - bh / 2 - 30, -4, holes=[(x0 + 80, zp - bh / 2 - 38, 15)])
    _add(out, "Hand line pad eye 8 mm plate", pe, STEEL, "made", None, "boom", "boom")
    for sy in (1, -1):
        _add(out, f"Weld, hand line pad eye {'+Y' if sy > 0 else '-Y'}",
             line_weld((x0 + 45, sy * 4, zp - bh / 2), (1, 0, 0), 70, 4, (0, sy, 0), (0, 0, -1)), w, "weld", None, "boom",
             "boom")
    zh = zp - bh / 2 - 38
    t = Pos(x0 + 80, 0, zh - 20) * Rot(0, 90, 0) * Torus(20.0, 6.0)
    hl = Compound([t, rope_path([(x0 + 80, 0, zh - 40), (x0 + 80, 0, 900)], 12.0)])
    _add(out, "Hand line 12 mm polyester", hl, ROPE, "made", None, "boom", "boom")
    # net spreaders and bridles from a tip pad eye
    xt = x1 - 80
    zpe = zp - bh / 2 - 38
    pe = _plate_xz(70, 60, 8, xt, zp - bh / 2 - 30, -4, holes=[(xt, zpe, 15)])
    _add(out, "Net pad eye 8 mm plate, boom tip", pe, STEEL, "made", None, "net", "boom")
    for sy in (1, -1):
        _add(out, f"Weld, net pad eye {'+Y' if sy > 0 else '-Y'}",
             line_weld((xt - 35, sy * 4, zp - bh / 2), (1, 0, 0), 70, 4, (0, sy, 0), (0, 0, -1)), w, "weld", None, "net",
             "boom")
    _shackle(out, (xt, 0, zpe), (1, 0, 0), (0, 0, -1), "Net bridle", None, "net", "boom")
    hn = C["net"] / 2
    zs = 200.0
    a = hn * math.sqrt(2)
    for k, (dx, dy) in enumerate(((1, 1), (1, -1))):
        z = zs + k * 52
        pole = frame((xt - dx * a / math.sqrt(2), -dy * a / math.sqrt(2), z), (dx, dy, 0)) * cp.round_tube(50, 5, 2 * a)
        pole = pole - Pos(xt, 0, z) * Cylinder(6.5, 60)
        _add(out, f"Net spreader pole {k + 1}, 50 bamboo, {2 * a:,.0f} long", pole, "bamboo", "made", None, "net", "boom")
    _bolt_set(out, 12, 102, Pos(xt, 0, zs + 52 + 25), None, "net", mat=GALV, label=", spreader cross", group="boom")
    apex = (xt, 0.0, zpe - 51 - 11)
    br = []
    for dx, dy in ((1, 1), (-1, -1), (1, -1), (-1, 1)):
        k = 0 if dx * dy > 0 else 1
        z = zs + k * 52 + 25
        endp = (xt + dx * (a - 40) / math.sqrt(2), dy * (a - 40) / math.sqrt(2), z + 4)
        br.append(rope_path([apex, endp], 8.0))
    _add(out, "Net bridles, four 8 mm polyester", Compound(br), ROPE, "made", None, "net", "boom")
    return out


def _wire_tie(out, L, A, d, name, group):
    """Wire stay between two lug holes (pins along Y): shackle, thimble, wire with two grips, thimble, shackle."""
    u = (Vector(*A) - Vector(*L)).normalized()
    dist = (Vector(*A) - Vector(*L)).length
    loc = frame(L, u.cross(Vector(0, 1, 0)), u)
    bow, pin = bk.shackle()
    th = bk.thimble(d)
    re_ = 6.5 + 2.0 + d / 2
    x1, x2 = 52.5, dist - 52.5
    for nm, x, flip in (("upper", 0.0, False), ("lower", dist, True)):
        L2 = loc * Pos(x, 0, 0) * (Rot(0, 0, 180) if flip else Rot(0, 0, 0))
        _add(out, f"{name} {nm} shackle bow, 10 mm", L2 * bow, GALV, "bought", None, "stay", group)
        _add(out, f"{name} {nm} shackle pin", L2 * pin, GALV, "fastener", None, "stay", group)
    _add(out, f"{name} thimble, upper", loc * Pos(x1, 0, 0) * th, GALV, "bought", None, "stay", group)
    _add(out, f"{name} thimble, lower", loc * Pos(x2, 0, 0) * th, GALV, "bought", None, "stay", group)
    rr = d / 2 + 0.5
    wire = Compound([loc * Pos(x1, 0, 0) * bk.rope_eye(d), loc * Pos(x2, 0, 0) * bk.rope_eye(d),
                     loc * seg((x1 + re_, 0, 0), (x2 - re_, 0, 0), d / 2),
                     loc * seg((x1 + re_, 2 * rr, 0), (x1 + re_ + 140, 2 * rr, 0), d / 2),
                     loc * seg((x2 - re_ - 140, 2 * rr, 0), (x2 - re_, 2 * rr, 0), d / 2)])
    _add(out, f"{name} 8 mm wire rope", wire, GALV, "made", None, "stay", group)
    for xe, s in ((x1 + re_, 1), (x2 - re_, -1)):
        for nm, shp, kind in bk.wire_grip(d):
            _add(out, f"{name} {nm}", loc * Pos(xe + s * 80, rr, 0) * shp, GALV, kind, None, "stay", group)


# ----------------------------------------------------------------------------- kit 1.9 interface
@lru_cache(maxsize=8)
def _build(option, short):
    return tuple({"A": option_a, "B": option_b, "C": option_c}[option](PARAMS, short))


def components(option, short=True):
    """Parts of one option as cad_parts.part() dicts (picture layout by default; short=False for the design case)."""
    return [dict(p) for p in _build(option, short)]


# ----------------------------------------------------------------------------- legacy interface (option A)
@dataclass
class Comp:
    name: str
    shape: object
    bom: int
    group: str          # bank, far, table, loop, net
    material: str


BOM = {  # key: (BOM line, plain name)
    "post": (1, "Bank post weldment"), "stake": (2, "Far stake"), "collar": (3, "Swivel collar"),
    "table": (4, "Clearing table"), "stays": (5, "Back-stays (2)"), "loop": (6, "Rope loop (two halves)"),
    "bridle": (7, "Net bridle with weak link and snap hook"), "near_block": (8, "Swivel blocks (2)"),
    "far_block": (8, "Swivel blocks (2)"), "rings": (9, "Swivel rings (2)"), "cleats": (10, "Jam cleats (2)"),
    "anchors": (11, "Screw ground anchors (2)"), "turnbuckles": (12, "Turnbuckles (2)"),
    "near_shackle": (13, "Shackles (6)"), "far_shackle": (13, "Shackles (6)"), "stay_shackles": (13, "Shackles (6)"),
    "pin": (14, "Stop pin"),
}
MATERIAL = {"post": "steel", "stake": "steel", "collar": "steel", "table": "timber", "stays": "polyester",
            "loop": "polysteel", "bridle": "polyester", "near_block": "bought", "far_block": "bought",
            "rings": "steel", "cleats": "bought", "anchors": "steel", "turnbuckles": "steel",
            "near_shackle": "steel", "far_shackle": "steel", "stay_shackles": "steel", "pin": "steel"}
GROUP = {"post": "bank", "cleats": "bank", "anchors": "bank", "stays": "bank", "turnbuckles": "bank",
         "near_block": "bank", "near_shackle": "bank", "stay_shackles": "bank",
         "stake": "far", "pin": "far", "collar": "far", "far_block": "far", "far_shackle": "far",
         "table": "table", "loop": "loop", "rings": "loop", "bridle": "net"}


def build_components(P=PARAMS, short=False):
    """Option A grouped into the legacy components, each a Compound of its detailed parts. Returns {key: Comp}."""
    parts = components("A", short)
    comps = {}
    for k in BOM:
        shapes = [p["shape"] for p in parts if p["key"] == k]
        comps[k] = Comp(BOM[k][1], Compound(shapes), BOM[k][0], GROUP[k], MATERIAL[k])
    return comps


def far_parts(P=PARAMS):
    """Far-end components in the stake's local frame (stake axis at the origin), and the stop pin heights."""
    C = build_components(P, short=False)
    S = P["span"]
    out = {k: Pos(-S, 0, 0) * C[k].shape for k in ("stake", "pin", "collar", "far_shackle", "far_block")}
    return out, derived(P)["pin_holes"]


def table_parts(P=PARAMS):
    """Clearing table centred at the origin."""
    tx, ty = P["table_xy"]
    return Pos(-tx, -ty, 0) * build_components(P, short=True)["table"].shape


def context_shapes(P=PARAMS, short=False):
    """Site context for pictures: bank, water surface, bed, and a net stacked on the table."""
    L = site(P, short)
    D = derived(P)
    xw, S = L["x_water"], L["span"]
    bank = bx(-2600, xw, -1800, 1800, -700, 0)
    water = bx(xw, S + 1200, -1800, 1800, P["z_water"] - 10, P["z_water"])
    bed = bx(xw, S + 1200, -1800, 1800, D["z_bed"] - 80, D["z_bed"])
    tx, ty = P["table_xy"]
    tl, tw, th = P["table"]
    net = bx(tx - tl / 2 + 60, tx + tl / 2 - 60, ty - tw / 2 + 40, ty + tw / 2 - 40, th, th + 70)
    return {"bank": bank, "water": water, "bed": bed, "net": net}


def assembly(P=PARAMS, short=False, keys=None):
    C = build_components(P, short)
    keys = keys or list(C)
    return Compound([C[k].shape for k in keys])


# ----------------------------------------------------------------------------- checks, masses, export
def checks(option=CHOSEN, verbose=True):
    """Constructability: no two parts overlap by more than 5 mm3 (same rule as .kit/cad_check.py)."""
    sys.path.insert(0, str(HERE.parents[1] / ".kit"))
    import cad_check
    parts = [p for p in components(option) if p["kind"] != "context"]
    hits = cad_check.interference(parts, ALLOWED_CONTACTS)
    if verbose:
        print(f"option {option}: {len(parts)} parts; overlaps (should be none):", hits or "none")
    return hits


def masses(P=PARAMS, short=False):
    """Mass in kg of each legacy component of option A from model volumes and kit densities (design case)."""
    out = {}
    for p in components("A", short):
        out[p["key"]] = out.get(p["key"], 0.0) + cp.mass_kg(p)
    return out


def export(P=PARAMS):
    """Legacy STEP and STL of the design case (30 m span); STL at 0.15 mm chord error."""
    root = HERE.parents[1]
    (root / "cad" / "step").mkdir(parents=True, exist_ok=True)
    (root / "cad" / "stl").mkdir(parents=True, exist_ok=True)
    groups = {"bank-station": ["post", "cleats", "anchors", "stays", "turnbuckles", "near_block", "near_shackle",
                               "stay_shackles"],
              "far-end": ["stake", "pin", "collar", "far_block", "far_shackle"],
              "table": ["table"]}
    C = build_components(P, short=False)
    for g, keys in groups.items():
        cmp = Compound([C[k].shape for k in keys])
        export_step(cmp, str(root / "cad" / "step" / f"bankhaul-{g}.step"))
        if g == "far-end":
            cmp = Compound([Pos(-P["span"], 0, 0) * C[k].shape for k in keys])
        export_stl(cmp, str(root / "cad" / "stl" / f"bankhaul-{g}.stl"), tolerance=0.15, angular_tolerance=0.3)
    export_step(Compound([c.shape for c in C.values()]), str(root / "cad" / "step" / "bankhaul-assembly.step"))
    print("exported legacy STEP and STL to cad/step and cad/stl")


if __name__ == "__main__":
    D = derived()
    print({k: (round(v, 1) if isinstance(v, float) else v) for k, v in D.items() if not isinstance(v, list)})
    for opt in OPTIONS:
        ps = [p for p in components(opt) if p["kind"] != "context"]
        design = [p for p in components(opt, short=False) if p["kind"] != "context"]
        print(f"option {opt}: {len(ps)} parts, {sum(cp.mass_kg(p) for p in ps):.1f} kg in the picture layout, "
              f"{sum(cp.mass_kg(p) for p in design):.1f} kg in the design case")
        checks(opt)
    for k, v in sorted(masses().items()):
        print(f"{k:14s} {v:7.2f} kg")
    if "--check" not in sys.argv:
        export()
