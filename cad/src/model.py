"""BankHaul parametric model (build123d), TRL 3, constructable design (BKH-DDR-002).

Run from the repo root:  python cad/src/model.py          (checks, masses and exports)
                         python cad/src/model.py --check  (constructability checks only)
Exports STEP and STL into cad/step and cad/stl:
    bankhaul-bank-station.step / .stl   bank post weldment with stays, ground anchors, near block,
                                        jam cleats and shackles
    bankhaul-far-end.step / .stl        far stake with stop pin, swivel collar, far block and shackle
    bankhaul-table.step / .stl          clearing table
    bankhaul-assembly.step              the whole station at the design case (30 m between pulleys)

Axes (site): X runs from the bank post (x = 0) out toward the far stake (+X), Y is across the line,
Z is up with the bank ground at z = 0 and the water surface at z = -500 mm. The loop's two legs run
side by side 112 mm apart (y = +56 and y = -56); the clearing table stands landward on the +Y side.

Constructable design, 2026-10-03 (BKH-DDR-002, decided under Amish's pre-approval of 2026-10-03):
    the bank post is a 48.3 mm steel tube welded to a 350 mm foot plate with a ground spike, held
    back by two splayed rope back-stays with turnbuckles to two 250 mm helix screw ground anchors
    set in line with the stays; a pad eye at the head carries the near block on a shackle; a cleat
    bar slipped over the post carries two jam cleats and the net tie-off hole;
    the far end is a 76.1 mm steel stake driven 2.5 m into the bed with a welded point and cap,
    a swivel collar that turns on the stake and rests on a through-bolt stop pin (holes every
    200 mm for the season's water level) and carries the far block on a shackle;
    the loop is two halves of 12 mm floating rope joined by two eye-to-eye swivels that are the
    clip rings and the end stops; each net bridle reaches its ring through a weak link.
Main dimensions and interfaces only; tolerances are TRL 4 work. The same PARAMS feed
docs/04-calcs/sizing.py (BKH-CAL-001), the drawings (cad/src/sheets.py), the concept media
(cad/src/concept_media.py), the product model and the build plan pictures.
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

from build123d import (Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, Solid, Torus, Vector, extrude,
                       export_step, export_stl)

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # site layout, design case (R2): span between pulley centres, waterline, water and bed levels
    "span": 30000.0, "x_water": 6000.0, "z_water": -500.0, "water_depth": 1000.0,
    "short": {"span": 7000.0, "x_water": 3000.0},       # shortened layout for pictures
    "span_max": 50000.0,                                  # stretch goal (R2)
    # 6 loop rope: 12 mm floating polypropylene and polyethylene blend ("polysteel"), MBS in N
    "rope_d": 12.0, "rope_mbs": 20000.0, "rope_kg_m": 0.068, "splice_eff": 0.85,
    # 8 blocks: sheave OD, sheave thickness, cheek radius, pitch radius of the rope round the sheave
    "sheave": (100.0, 16.0), "cheek_r": 65.0, "block_wll": 5000.0,
    # 1 bank post weldment: tube OD x wall, head height; foot plate; spike; cleat bar; lugs
    "post": (48.3, 3.2), "post_h": 1000.0, "foot": (350.0, 8.0), "spike": (20.0, 400.0),
    "cleat_bar": (130.0, 500.0, 8.0, 850.0),     # X depth, Y length, thickness, top height
    "cleat_y": 200.0,                            # jam cleat centres from the post centre line
    "pad_eye": (60.0, 100.0, 8.0, 18.0),         # radial length, height, thickness, hole
    "lug": (60.0, 80.0, 8.0, 15.0),
    "eye_r": 64.0,                                # pad eye hole centre from the post axis (+X)
    "z_block": 950.0,                             # near block sheave plane height
    # 11 screw ground anchors and 5 back-stays: anchor eye plan position, rod, helix
    "anchor_xy": (-1100.0, 450.0), "anchor_rod": (20.0, 1600.0), "helix": (250.0, 8.0, 1400.0),
    "stay_d": 10.0, "stay_mbs": 22000.0, "turnbuckle": (12.0, 200.0),
    # 2 far stake: tube OD x wall, embedment below the bed, top above the water, point length
    "stake": (76.1, 3.6), "embed": 2500.0, "stake_top": 500.0, "point": 150.0, "pin_d": 12.0,
    "pin_pitch": 200.0,
    # 3 swivel collar: tube OD x wall x length, lug; far block sheave height above the water
    "collar": (88.9, 3.2, 200.0), "z_far_above_water": 200.0, "far_eye_r": 75.0,
    # 4 clearing table: top L x W, height, centre (x, y)
    "table": (1200.0, 600.0, 850.0), "table_xy": (-600.0, 1000.0),
    # 9 swivel rings: body length, eye OD; distance of ring 1 from the near sheave when ready to set
    "swivel": (90.0, 30.0), "ring_gap": 450.0,
    # materials (kg per m^3)
    "rho_steel": 7850.0, "rho_timber": 750.0,
}


# ----------------------------------------------------------------------------- helpers
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
    """Round bar from point a to point b."""
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _ccw(points):
    a = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(points, points[1:] + points[:1]))
    return list(points) if a > 0 else list(points)[::-1]


def prism_xy(points, z0, z1):
    f = Plane.XY.offset(z0) * Polygon(*_ccw(points), align=None)
    return extrude(f, amount=z1 - z0)


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
    lug_r = P["post"][0] / 2 + P["lug"][0] - 20.0
    D["lug_r"] = lug_r
    D["z_lug"] = P["post_h"] - 40.0
    D["stake_len"] = P["water_depth"] + P["embed"] + P["stake_top"]
    D["z_bed"] = P["z_water"] - P["water_depth"]
    D["z_far"] = P["z_water"] + P["z_far_above_water"]
    D["loop_len"] = 2 * P["span"] + 2 * math.pi * D["r_pitch"]
    D["half_len"] = D["loop_len"] / 2
    return D


# ----------------------------------------------------------------------------- components
def post_parts(P=PARAMS):
    """Bank post weldment (BOM 1), jam cleats (10), screw anchors (11), stays with turnbuckles (5, 12),
    near block (8) and the post shackles (13). Local frame: post axis at the origin, ground z = 0."""
    D = derived(P)
    ro = P["post"][0] / 2
    ri = ro - P["post"][1]
    H = P["post_h"]
    fs, ft = P["foot"]
    out = {}
    # 1 weldment: foot plate, spike, tube, cap, pad eye, two stay lugs, cleat bar
    foot = bx(-fs / 2, fs / 2, -fs / 2, fs / 2, 0, ft)
    sd, sl = P["spike"]
    spike = zcyl(0, 0, sd / 2, -sl + 40, 0) + Solid.make_cone(1.0, sd / 2, 40, Plane.XY.offset(-sl))
    tube = ztube(0, 0, ro, ri, ft, H)
    cap = zcyl(0, 0, ro + 6, H, H + 8)
    pl, ph, pt, phole = P["pad_eye"]
    pad = bx(ro - 1, ro + pl, -pt / 2, pt / 2, P["z_block"] - ph / 2, H) - ycyl(P["eye_r"], P["z_block"], phole / 2, -pt, pt)
    lugs = []
    ll, lh, lt, lhole = P["lug"]
    for s in (1, -1):
        lug = bx(ro - 1, ro + ll, -lt / 2, lt / 2, H - lh, H) - ycyl(D["lug_r"], D["z_lug"], lhole / 2, -lt, lt)
        lugs.append(rot_z(lug, 180 - s * D["stay_plan_deg"]))
    cx, cy, ct, cz = P["cleat_bar"]
    bar = bx(-40, cx - 40, -cy / 2, cy / 2, cz - ct, cz) - zcyl(0, 0, ro + 0.3, cz - ct - 1, cz + 1)
    for y in (P["cleat_y"] - 30, P["cleat_y"] + 30, -P["cleat_y"] - 30, -P["cleat_y"] + 30):
        bar = bar - zcyl(40, y, 4.5, cz - ct - 1, cz + 1)
    bar = bar - zcyl(50, 110, 7.5, cz - ct - 1, cz + 1)          # net tie-off hole
    out["post"] = fuse([foot, spike, tube, cap, pad, bar] + lugs)
    # 10 jam cleats: V blocks 100 long on the bar, groove along X
    cleats = []
    for y in (P["cleat_y"], -P["cleat_y"]):
        body = bx(-10, 90, y - 20, y + 20, cz, cz + 30)
        v = bx(-12, 92, y - 6, y + 6, cz + 10, cz + 31)          # V groove, simplified as a slot
        cleats.append(body - v)
    out["cleats"] = fuse(cleats)
    # 8 near block, sheave plane horizontal at z_block, sheave centre at x_near
    out["near_block"] = block(P, D["x_near"], P["z_block"], facing=+1)
    # 13 shackle: pin through the pad eye, bow round the block's swivel eye
    out["near_shackle"] = shackle(P["eye_r"], P["z_block"], P["eye_r"] + 51.0, facing=+1)
    # 11 screw anchors and 5 stays, 12 turnbuckles, stay shackles
    anchors, stays, tbs, shk = [], [], [], []
    ax, ay = P["anchor_xy"]
    for s in (1, -1):
        th = math.radians(180 - s * D["stay_plan_deg"])
        L = Vector(D["lug_r"] * math.cos(th), D["lug_r"] * math.sin(th), D["z_lug"])
        A = Vector(ax, s * ay, 60.0)
        d = (A - L).normalized()
        rd, rl = P["anchor_rod"]
        top = A + d * 30.0
        anchors.append(rod(top, top + d * rl, rd / 2))
        hd, ht, hz = P["helix"]
        hc = top + d * hz
        anchors.append(Solid.make_cylinder(hd / 2, ht, Plane(origin=hc, z_dir=d)))
        anchors.append(Solid.make_torus(26.0, 6.0, Plane(origin=A, z_dir=Vector(-d.Y, d.X, 0).normalized())))
        # turnbuckle body from the anchor eye back toward the post, then the stay rope to the lug shackle
        tb0 = A - d * 30.0
        tb1 = tb0 - d * P["turnbuckle"][1]
        tbs.append(rod(tb0, tb1, P["turnbuckle"][0] / 2 + 3))
        s0 = L + d * 48.0
        stays.append(rod(s0, tb1 - d * 2.0, P["stay_d"] / 2))
        shk.append(rod(L - d * 4.0, L + d * 44.0, 6.0))
    out["anchors"] = fuse(anchors)
    out["stays"] = fuse(stays)
    out["turnbuckles"] = fuse(tbs)
    out["stay_shackles"] = fuse(shk)
    return out


def block(P, xc, zc, facing=+1):
    """Single-sheave swivel block lying with its sheave horizontal. facing=+1: eye toward -X (near
    block, rope runs out to +X); facing=-1: eye toward +X (far block)."""
    so, st = P["sheave"]
    cr = P["cheek_r"]
    f = facing
    sheave = zcyl(xc, 0, so / 2, zc - st / 2, zc + st / 2) - zcyl(xc, 0, 6.5, zc - st, zc + st)
    groove = Pos(xc, 0, zc) * Torus(so / 2 + P["rope_d"] / 2, P["rope_d"] / 2 + 0.3)
    sheave = sheave - groove
    pin = zcyl(xc, 0, 6.0, zc - st / 2 - 6, zc + st / 2 + 6)
    neck_x = xc - f * cr                       # where the cheeks end
    sp_x = neck_x - f * 14                     # spacer between the cheeks, outside the rope wrap
    cheeks = []
    for z0 in (zc - st / 2 - 6, zc + st / 2 + 3):
        disc = zcyl(xc, 0, cr, z0, z0 + 3)
        strap = bx(min(sp_x, xc), max(sp_x, xc), -20, 20, z0, z0 + 3)
        cheeks.append(disc + strap)
    spacer = bx(min(sp_x, neck_x), max(sp_x, neck_x), -12, 12, zc - st / 2 - 3, zc + st / 2 + 3)
    neck = xcyl(0, zc, 6.0, min(sp_x - f * 8, sp_x), max(sp_x - f * 8, sp_x))
    eye_x = sp_x - f * 22
    eye = ring_xz(eye_x, 0, zc, 14.0, 8.0, 6.0)
    return fuse(cheeks + [spacer, neck, eye, pin]) + sheave


def shackle(x_pin, z, x_bow, facing=+1):
    """Bow shackle: pin along Y through a pad eye at x_pin, legs along X, bow through the block eye."""
    f = facing
    pin = ycyl(x_pin, z, 5.0, -16, 16)
    legs = [xcyl(y, z, 5.0, min(x_pin, x_bow), max(x_pin, x_bow)) for y in (-12, 12)]
    bow = ycyl(x_bow, z, 4.0, -16, 16)
    return fuse([pin, bow] + legs)


def far_parts(P=PARAMS):
    """Far stake (BOM 2) with stop pin (14), swivel collar (3), far block (8) and shackle (13).
    Local frame: stake axis at the origin, water surface z_water."""
    D = derived(P)
    so_, sw = P["stake"]
    ro, ri = so_ / 2, so_ / 2 - sw
    zb = D["z_bed"]
    z0 = zb - P["embed"]
    z1 = P["z_water"] + P["stake_top"]
    pt = P["point"]
    tube = ztube(0, 0, ro, ri, z0 + pt, z1)
    point = Pos(0, 0, z0 + pt / 2) * Solid.make_cone(1.0, ro, pt, Plane.XY.offset(-pt / 2))
    cap = zcyl(0, 0, ro, z1, z1 + 6)
    stake = fuse([tube, point, cap])
    zf = D["z_far"]
    co, cw, cl = P["collar"]
    z_c0 = zf - cl / 2
    z_pin = z_c0 - P["pin_d"] / 2
    holes = [z_pin + k * P["pin_pitch"] for k in range(-3, 2)]
    for zh in holes:
        stake = stake - ycyl(0, zh, P["pin_d"] / 2 + 0.5, -ro - 1, ro + 1)
    out = {"stake": stake}
    out["pin"] = fuse([ycyl(0, z_pin, P["pin_d"] / 2, -ro - 8, ro + 8), ycyl(0, z_pin, 10.0, ro + 8, ro + 16),
                       ycyl(0, z_pin, 10.0, -ro - 18, -ro - 8)])
    collar = ztube(0, 0, co / 2, co / 2 - cw, z_c0, z_c0 + cl)
    lug = bx(-co / 2 - 60, -co / 2 + 1, -4, 4, zf - 40, zf + 40) - ycyl(-P["far_eye_r"] - 0, zf, 9.0, -8, 8)
    lug = lug - zcyl(0, 0, co / 2 - cw + 0.1, zf - 50, zf + 50)
    out["collar"] = fuse([collar, lug])
    x_eye = -P["far_eye_r"]
    out["far_shackle"] = shackle(x_eye, zf, x_eye - 51.0, facing=-1)
    out["far_block"] = block(P, x_eye - 152.0, zf, facing=-1)
    return out, holes


def table_parts(P=PARAMS):
    """Clearing table (BOM 4), centred at the origin, timber."""
    L, W, H = P["table"]
    parts = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            x = sx * (L / 2 - 75)
            y = sy * (W / 2 - 50)
            parts.append(bx(x - 25, x + 25, y - 25, y + 25, 0, H - 25 - 75))
    for sy in (-1, 1):   # long rails (aprons) 75 x 25, outside the legs
        y = sy * (W / 2 - 50 + 25 + 12.5)
        parts.append(bx(-L / 2 + 25, L / 2 - 25, y - 12.5, y + 12.5, H - 25 - 75, H - 25))
    for sx in (-1, 1):   # end rails between the long rails
        x = sx * (L / 2 - 75)
        parts.append(bx(x - 25, x + 25, -W / 2 + 25 + 12.5 - 0.0, W / 2 - 25 - 12.5, H - 25 - 75, H - 25))
    nb = 5
    gap = (W - nb * 100) / (nb - 1)
    for k in range(nb):
        y0 = -W / 2 + k * (100 + gap)
        parts.append(bx(-L / 2, L / 2, y0, y0 + 100, H - 25, H))
    for sy in (-1, 1):   # lip boards along the long edges stop the net sliding off
        y = sy * (W / 2 - 12.5)
        parts.append(bx(-L / 2, L / 2, y - 12.5, y + 12.5, H, H + 75))
    return fuse(parts)


# ----------------------------------------------------------------------------- site assembly
@dataclass
class Comp:
    name: str
    shape: object
    bom: int
    group: str          # bank, far, table, loop, net
    material: str


BOM = {  # key: (BOM line, plain name)
    "post": (1, "Bank post weldment"),
    "stake": (2, "Far stake"),
    "collar": (3, "Swivel collar"),
    "table": (4, "Clearing table"),
    "stays": (5, "Back-stays (2)"),
    "loop": (6, "Rope loop (two halves)"),
    "bridle": (7, "Net bridle with weak link and snap hook"),
    "near_block": (8, "Swivel blocks (2)"),
    "far_block": (8, "Swivel blocks (2)"),
    "rings": (9, "Swivel rings (2)"),
    "cleats": (10, "Jam cleats (2)"),
    "anchors": (11, "Screw ground anchors (2)"),
    "turnbuckles": (12, "Turnbuckles (2)"),
    "near_shackle": (13, "Shackles (6)"),
    "far_shackle": (13, "Shackles (6)"),
    "stay_shackles": (13, "Shackles (6)"),
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


def site(P=PARAMS, short=False):
    L = dict(P)
    if short:
        L.update(P["short"])
    return L


def leg_points(P=PARAMS, short=False, y=0.0):
    """Centre line of one loop leg: near sheave tangent, bank edge, water, far sheave tangent."""
    L = site(P, short)
    D = derived(P)
    zw = P["z_water"]
    r = P["rope_d"] / 2
    x_far_sheave = L["span"] - P["far_eye_r"] - 152.0
    c = P["cheek_r"] + 40.0                      # straight, level lead out of each block
    return [(D["x_near"], y, P["z_block"]), (D["x_near"] + c, y, P["z_block"]), (L["x_water"], y, r),
            (L["x_water"] + 400.0, y, zw), (x_far_sheave - 1500.0, y, zw), (x_far_sheave - c, y, D["z_far"]),
            (x_far_sheave, y, D["z_far"])]


def _z_on(pts, x):
    for (x0, _, z0), (x1, _, z1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return z0 + (z1 - z0) * (x - x0) / (x1 - x0)
    return pts[-1][2]


def loop_parts(P=PARAMS, short=False):
    """Rope loop (6) with its wraps round both sheaves, and the two swivel rings (9)."""
    L = site(P, short)
    D = derived(P)
    r = P["rope_d"] / 2
    rp = D["r_pitch"]
    pieces = []
    for y in (rp, -rp):
        pts = leg_points(P, short, y)
        for a, b in zip(pts, pts[1:]):
            pieces.append(rod(a, b, r))
    xn = D["x_near"]
    wrap_n = (Pos(xn, 0, P["z_block"]) * Torus(rp, r)) & bx(xn - rp - 20, xn, -rp - 20, rp + 20, P["z_block"] - 20, P["z_block"] + 20)
    xf = L["span"] - P["far_eye_r"] - 152.0
    zf = D["z_far"]
    wrap_f = (Pos(xf, 0, zf) * Torus(rp, r)) & bx(xf, xf + rp + 20, -rp - 20, rp + 20, zf - 20, zf + 20)
    loop = fuse(pieces + [wrap_n, wrap_f])
    # rings: ring 1 on the setting leg (y = -56) near the bank, ring 2 on the other leg near the far block
    sl, so = P["swivel"]
    rings = []
    for y, x in ((-rp, xn + P["ring_gap"]), (rp, xf - P["ring_gap"])):
        pts = leg_points(P, short, y)
        z = _z_on(pts, x)
        body = xcyl(y, z, 9.0, x - sl / 2 + 16, x + sl / 2 - 16)
        e1 = ring_xz(x - sl / 2 + 8, y, z, so / 2, so / 2 - 6, 6)
        e2 = Pos(x + sl / 2 - 8, y, z) * Rot(90, 0, 0) * Pos(-(x + sl / 2 - 8), -y, -z) * ring_xz(x + sl / 2 - 8, y, z, so / 2, so / 2 - 6, 6)
        rings.append(fuse([body, e1, e2]))
    return loop, rings


def bridle_parts(P=PARAMS, short=False):
    """Net bridle (7): snap hook on ring 1, weak link, bridle legs down to the net's end on the table."""
    D = derived(P)
    rp = D["r_pitch"]
    x1 = D["x_near"] + P["ring_gap"]
    pts = leg_points(P, short, -rp)
    z1 = _z_on(pts, x1)
    hook = rod((x1, -rp, z1 - 12), (x1, -rp - 10, z1 - 70), 4.0)
    weak = rod((x1, -rp - 10, z1 - 70), (x1 - 150, -rp - 120, z1 - 220), 2.0)
    tx, ty = P["table_xy"]
    tl, tw, th = P["table"]
    over = (tx + tl / 2 - 150, ty - tw / 2 - 30, th + 100)          # over the table lip
    end = (tx + tl / 2 - 150, ty - tw / 2 + 150, th + 80)          # the net's end, on top of the stack
    leg = rod((x1 - 150, -rp - 120, z1 - 220), over, 3.0) + rod(over, end, 3.0)
    return fuse([hook, weak, leg])


def build_components(P=PARAMS, short=False):
    """Every component placed on site. Returns {key: Comp}."""
    L = site(P, short)
    bank = post_parts(P)
    far, _ = far_parts(P)
    comps = {}
    for k, s in bank.items():
        comps[k] = Comp(BOM[k][1], s, BOM[k][0], GROUP[k], MATERIAL[k])
    for k, s in far.items():
        comps[k] = Comp(BOM[k][1], Pos(L["span"], 0, 0) * s, BOM[k][0], GROUP[k], MATERIAL[k])
    tx, ty = P["table_xy"]
    comps["table"] = Comp(BOM["table"][1], Pos(tx, ty, 0) * table_parts(P), 4, "table", "timber")
    loop, rings = loop_parts(P, short)
    comps["loop"] = Comp(BOM["loop"][1], loop, 6, "loop", "polysteel")
    comps["rings"] = Comp(BOM["rings"][1], fuse(rings), 9, "loop", "steel")
    comps["bridle"] = Comp(BOM["bridle"][1], bridle_parts(P, short), 7, "net", "polyester")
    return comps


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


# ----------------------------------------------------------------------------- checks
def _dist(a, b):
    try:
        return a.distance_to(b)
    except Exception:
        return float("nan")


HOLDS = [("cleats", "post"), ("near_shackle", "post"), ("near_block", "near_shackle"), ("stay_shackles", "post"),
         ("stays", "stay_shackles"), ("turnbuckles", "stays"), ("anchors", "turnbuckles"), ("pin", "stake"),
         ("collar", "pin"), ("far_shackle", "collar"), ("far_block", "far_shackle"), ("loop", "near_block"),
         ("loop", "far_block"), ("rings", "loop"), ("bridle", "rings")]
ALLOWED = [{"loop", "rings"}, {"bridle", "rings"}, {"near_shackle", "near_block"}, {"far_shackle", "far_block"},
           {"stays", "stay_shackles"}, {"anchors", "turnbuckles"}, {"near_shackle", "post"},
           {"far_shackle", "collar"}, {"stay_shackles", "post"}, {"pin", "stake"}]


def checks(P=PARAMS, verbose=True):
    """Constructability checks: no two separate parts overlap (except a pin or rope eye passing
    through the hole or eye it is fitted to, listed in ALLOWED and checked for clearance by hand);
    every part touches or sits within 6 mm of what holds it (pin clearances)."""
    C = build_components(P, short=True)
    keys = list(C)
    res = {"overlaps": [], "floating": []}
    for a, b in HOLDS:
        d = _dist(C[a].shape, C[b].shape)
        if not d <= 6.0:
            res["floating"].append((a, b, round(d, 1)))
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if {a, b} in ALLOWED:
                continue
            ba, bb_ = C[a].shape.bounding_box(), C[b].shape.bounding_box()
            if (ba.min.X > bb_.max.X or bb_.min.X > ba.max.X or ba.min.Y > bb_.max.Y or bb_.min.Y > ba.max.Y
                    or ba.min.Z > bb_.max.Z or bb_.min.Z > ba.max.Z):
                continue
            try:
                inter = C[a].shape & C[b].shape
                v = 0.0 if inter is None else inter.volume
            except Exception:
                v = float("nan")
            if not v < 1.0:
                res["overlaps"].append((a, b, round(v, 1)))
    if verbose:
        print("overlaps (should be none):", res["overlaps"] or "none")
        print("parts not touching what holds them (should be none):", res["floating"] or "none")
    return res


def masses(P=PARAMS):
    """Mass in kg of each made steel or timber part from model volumes; ropes and bought parts from
    catalogue figures in docs/04-calcs/sizing.py."""
    C = build_components(P, short=False)
    rho = {"steel": P["rho_steel"], "timber": P["rho_timber"]}
    return {k: C[k].shape.volume * 1e-9 * rho[C[k].material] for k in ("post", "stake", "collar", "table", "anchors")}


def export(P=PARAMS):
    root = Path(__file__).resolve().parents[2]
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
        export_stl(cmp, str(root / "cad" / "stl" / f"bankhaul-{g}.stl"), tolerance=0.5, angular_tolerance=0.3)
    export_step(Compound([c.shape for c in C.values()]), str(root / "cad" / "step" / "bankhaul-assembly.step"))
    print("exported STEP and STL to cad/step and cad/stl")


if __name__ == "__main__":
    D = derived()
    print({k: (round(v, 1) if isinstance(v, float) else v) for k, v in D.items()})
    checks()
    for k, v in sorted(masses().items()):
        print(f"{k:12s} {v:6.2f} kg")
    if "--check" not in sys.argv:
        export()
