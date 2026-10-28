"""BankHaul repo-specific CAD helpers (kit 1.9 parts library extensions, STANDARDS section 24).

These sit beside .kit/cad_parts.py and build the rigging hardware a rope station is made of, at catalogue
envelope with their holes, pins and eyes, so every option in cad/src/model.py reaches detail level D3:

    frame()          a Location from an origin, a z direction and an optional x direction
    seg()            a round bar or rope piece between two points
    rope_path()      a rope through points, as straight pieces with round joints
    ring_weld()      a round fillet weld bead (tube to plate)
    line_weld()      a straight fillet weld bead with its legs on two faces
    shackle()        a bow shackle: bow with ears, and its screw pin
    thimble()        a grooved rope thimble
    turnbuckle()     a jaw-and-jaw turnbuckle: body, two jaws with threaded rods, two clevis pins, two split pins
    swivel_block()   a single-sheave swivel block: two cheeks, sheave, axle bolt and nut, swivel head with eye
    jam_cleat()      a V-jam cleat with two fixing holes
    screw_anchor()   a helical ground anchor: forged eye, rod and helix plate
    wire_grip()      a wire rope grip: U-bolt, saddle and two nuts

Nothing here is in .kit/; candidates for a future kit release are listed in docs/REVIEW.md. All sizes in mm.
Catalogue envelopes follow common galvanised rigging (10 mm bow shackle, M12 jaw-and-jaw turnbuckle,
100 mm sheave block); the parts bought are checked against them when ordered (BKH-DEC-001, to confirm).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import (Axis, Box, Compound, Cylinder, Location, Plane, Polygon, Pos, Rot, Solid, Sphere,  # noqa: E402
                       Torus, Vector, extrude, revolve)
from cad_parts import break_edges, clevis_pin, split_pin, hex_nut, washer, ISO  # noqa: E402


# ----------------------------------------------------------------------------------------------- placement
def frame(origin, z, x=None):
    """Location whose local Z points along z and local X along x (made perpendicular to z)."""
    zv = Vector(*z).normalized()
    if x is None:
        ref = Vector(1, 0, 0) if abs(zv.X) < 0.9 else Vector(0, 1, 0)
        xv = ref - zv * ref.dot(zv)
    else:
        xv = Vector(*x) - zv * Vector(*x).dot(zv)
    return Location(Plane(origin=tuple(origin), x_dir=tuple(xv.normalized()), z_dir=tuple(zv)))


def seg(a, b, r):
    """Round bar of radius r from point a to point b."""
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def rope_path(points, d, joints=True):
    """Rope of diameter d through points: straight pieces with spheres at the bends (a Compound)."""
    pieces = []
    for a, b in zip(points, points[1:]):
        if math.dist(a, b) > 1e-6:
            pieces.append(seg(a, b, d / 2))
    if joints:
        pieces += [Pos(*p) * Sphere(d / 2) for p in points[1:-1]]
    return Compound(pieces)


# ----------------------------------------------------------------------------------------------- welds
def ring_weld(r, leg, origin=(0, 0, 0), n=(0, 0, 1)):
    """Round fillet weld at radius r: one leg outward along the face it sits on, one along n (up the tube)."""
    prof = Plane.XZ * Polygon((r, 0), (r + leg, 0), (r, leg), align=None)
    ring = revolve(prof, Axis.Z, 360)
    return frame(origin, n) * ring


def line_weld(start, axis, length, leg, d1, d2):
    """Straight fillet weld from start along axis for length, legs along the unit vectors d1 and d2."""
    tri = extrude(Polygon((0, 0), (leg, 0), (0, leg), align=None), length)     # legs +X, +Y; length +Z
    ax, v1, v2 = Vector(*axis).normalized(), Vector(*d1).normalized(), Vector(*d2).normalized()
    if (ax.cross(v1) - v2).length < 1e-6:
        return frame(start, ax, v1) * tri
    if (ax.cross(v2) - v1).length < 1e-6:
        return frame(start, ax, v2) * tri
    raise ValueError("line_weld: axis, d1 and d2 must be mutually perpendicular unit vectors")


# ----------------------------------------------------------------------------------------------- rigging
SHACKLE = dict(d=10.0, pin=12.0, jaw=18.0, apex=51.0)


def shackle(s=SHACKLE):
    """Bow shackle in its local frame: pin axis along Y through the origin, bow toward +X, wire centre at the
    bow's apex at x = apex. Returns (bow, pin)."""
    d, pd, jaw, apex = s["d"], s["pin"], s["jaw"], s["apex"]
    R = jaw / 2 + d / 2
    L1 = apex - R
    legs = [Pos(L1 / 2, y, 0) * Rot(0, 90, 0) * Cylinder(d / 2, L1) for y in (-R, R)]
    bow = Pos(L1, 0, 0) * Torus(R, d / 2) & Pos(L1 + R, 0, 0) * Box(2 * R, 2 * R + d + 2, d + 2)
    ears = [Pos(0, y, 0) * Rot(90, 0, 0) * Cylinder(d * 0.95, d) for y in (-R, R)]
    body = legs[0].fuse(legs[1], bow, *ears)
    body = body - Rot(90, 0, 0) * Cylinder(pd / 2 + 0.3, 2 * R + 2 * d)
    pin = Rot(90, 0, 0) * Cylinder(pd / 2, 2 * R + d + 2)
    head = Pos(0, -(R + d / 2 + 1 + 2.5), 0) * Rot(90, 0, 0) * Cylinder(pd * 0.9, 5)
    eye = Pos(0, -(R + d / 2 + 1 + 5 + 4), 0) * Rot(0, 90, 0) * (Cylinder(5.5, 3) - Cylinder(2.5, 4))
    return body, pin.fuse(head, eye)


def thimble(rope_d, hole=6.5, wall=2.0):
    """Grooved thimble in the local XZ plane (hole axis along Y), centred on the origin: a bore of radius
    hole for the shackle pin, the rope's eye lying in its groove at radius hole + wall + rope_d / 2."""
    re_ = hole + wall + rope_d / 2
    ann = Rot(90, 0, 0) * (Cylinder(re_, rope_d + 3) - Cylinder(hole, rope_d + 5))
    return ann - rope_eye(rope_d, hole, wall)


def rope_eye(rope_d, hole=6.5, wall=2.0):
    """The rope's spliced eye round a thimble: a torus in the XZ plane lying in the thimble's groove."""
    return Rot(90, 0, 0) * Torus(hole + wall + rope_d / 2, rope_d / 2)


TB = dict(d=12.0, length=200.0, gap=14.0, tine=5.0)


def turnbuckle(tb=TB):
    """Jaw-and-jaw turnbuckle in its local frame: pin axes along Z at x = 0 (upper jaw) and x = length (lower
    jaw), body along X. Returns a list of (name, shape, kind)."""
    d, L, gap, tt = tb["d"], tb["length"], tb["gap"], tb["tine"]
    out = []
    for nm, x0, sgn in (("upper", 0.0, 1), ("lower", L, -1)):
        tines = []
        for z in (gap / 2 + tt / 2, -(gap / 2 + tt / 2)):
            tine = Pos(x0 + sgn * 6, 0, z) * Box(36, 26, tt)
            tine = tine - Pos(x0, 0, z) * Cylinder(d / 2 + 0.4, tt + 2)
            tines.append(tine)
        block = Pos(x0 + sgn * 28, 0, 0) * Box(8, 26, gap + 2 * tt)
        rod = Pos(x0 + sgn * (32 + 30), 0, 0) * Rot(0, 90, 0) * Cylinder(d / 2, 60)
        jaw = tines[0].fuse(tines[1], block, rod)
        out.append((f"Turnbuckle jaw, {nm}", break_edges(jaw, 0.6), "bought"))
        pin = Pos(x0, 0, gap / 2 + tt) * clevis_pin(int(d), gap + 2 * tt)
        out.append((f"Turnbuckle clevis pin, {nm}", pin, "bought"))
        sp = Pos(x0, 0, gap / 2 + tt - (gap + 2 * tt) - d) * split_pin(d)
        out.append((f"Turnbuckle split pin, {nm}", sp, "fastener"))
    # body: open frame, two end bosses threaded over the rods
    b0, b1 = 70.0, L - 70.0
    boss = [Pos(x, 0, 0) * Rot(0, 90, 0) * (Cylinder(10, 12) - Cylinder(d / 2, 14)) for x in (b0, b1)]
    bars = [Pos((b0 + b1) / 2, y, 0) * Box(b1 - b0, 5, 12) for y in (-11.5, 11.5)]
    body = boss[0].fuse(boss[1], *bars)
    out.append(("Turnbuckle body", break_edges(body, 0.5), "bought"))
    return out


BLOCK = dict(sheave=100.0, st=16.0, cheek_r=65.0, rope_d=12.0)


def swivel_block(xc, zc, facing, b=BLOCK):
    """Single-sheave swivel block with its sheave horizontal at height zc, sheave centre at x = xc, y = 0.
    facing=+1: eye toward -X (rope runs out to +X); -1: eye toward +X. Returns (name, shape, kind) and the
    x of the swivel eye's centre."""
    so, st, cr, rd = b["sheave"], b["st"], b["cheek_r"], b["rope_d"]
    f = facing
    out = []
    sheave = Pos(xc, 0, zc) * (Cylinder(so / 2, st) - Cylinder(6.5, st + 2))
    sheave = sheave - Pos(xc, 0, zc) * Torus(so / 2 + rd / 2, rd / 2 + 0.3)
    hub = Pos(xc, 0, zc) * (Cylinder(14, st + 4) - Cylinder(6.5, st + 6))
    out.append(("sheave, nylon, bushed", sheave.fuse(hub), "bought"))
    neck_x = xc - f * cr
    sp_x = neck_x - f * 14
    for nm, z0 in (("lower", zc - st / 2 - 5), ("upper", zc + st / 2 + 2)):
        disc = Pos(xc, 0, z0 + 1.5) * Cylinder(cr, 3)
        strap = Pos((sp_x + xc) / 2, 0, z0 + 1.5) * Box(abs(xc - sp_x), 40, 3)
        cheek = disc.fuse(strap) - Pos(xc, 0, z0 + 1.5) * Cylinder(6.2, 5)
        cheek = cheek - Pos(sp_x + f * 5, 0, z0 + 1.5) * Cylinder(4.3, 5)
        out.append((f"cheek, {nm}, galvanised", cheek, "bought"))
    # axle: M12 bolt through both cheeks and the sheave bore
    grip = st + 10.0
    s, k, m, d2, h, p = ISO[12]
    ztop = zc + st / 2 + 5
    bolt = Pos(xc, 0, ztop) * (Pos(0, 0, k / 2) * Cylinder(s / 2 + 1, k) + Pos(0, 0, -(grip + 14) / 2) * Cylinder(6, grip + 14))
    out.append(("axle bolt M12", bolt, "fastener"))
    out.append(("axle nut M12", Pos(xc, 0, ztop - grip - m) * hex_nut(12), "fastener"))
    # swivel head: spacer between the cheeks, neck and eye
    spacer = Pos(sp_x + f * 5, 0, zc) * Box(10, 24, st + 4)
    spacer = spacer - Pos(sp_x + f * 5, 0, zc) * Cylinder(4.3, st + 8)
    neck = Pos(sp_x - f * 5, 0, zc) * Rot(0, 90, 0) * Cylinder(7, 10)
    eye_x = sp_x - f * 22
    eye = Pos(eye_x, 0, zc) * Rot(90, 0, 0) * (Cylinder(14, 6) - Cylinder(8, 8))
    head = spacer.fuse(neck, eye)
    out.append(("swivel head with eye", break_edges(head, 0.5), "bought"))
    pin = Pos(sp_x + f * 5, 0, zc) * Cylinder(4, st + 10 + 2)
    out.append(("spacer rivet", pin, "fastener"))
    return out, eye_x


def jam_cleat(length=100.0, width=80.0, base=10.0, height=40.0, hole_y=30.0):
    """V-jam cleat with its V groove along X, base on z = 0, centred on the origin; two fixing holes on
    y = +/- hole_y."""
    plate = Pos(0, 0, base / 2) * Box(length, width, base)
    plate = break_edges(plate, 2.0)
    ridges = []
    for s in (1, -1):
        prof = Polygon((s * 2, base), (s * 20, base), (s * 20, height - 2), (s * 12, height), align=None)
        r = Plane.YZ * prof
        ridge = extrude(r, length - 10)
        ridge = Pos(-(length - 10) / 2, 0, 0) * ridge
        ridges.append(ridge)
    body = plate.fuse(*ridges)
    for y in (hole_y, -hole_y):
        body = body - Pos(0, y, base / 2) * Cylinder(4.25, base + 2)
    return body


def screw_anchor(rod_d=20.0, rod_l=1600.0, helix_d=250.0, helix_t=8.0, helix_at=1400.0, eye_R=26.0, eye_r=6.0):
    """Helical ground anchor in its local frame: forged eye centred on the origin in the XY plane (hole axis
    along Z), rod from the eye along +X, helix plate across the rod at helix_at from the rod's top."""
    eye = Torus(eye_R, eye_r)
    top = eye_R + eye_r - 2.0
    rod = Pos(top + rod_l / 2, 0, 0) * Rot(0, 90, 0) * Cylinder(rod_d / 2, rod_l)
    tip = Pos(top + rod_l, 0, 0) * Rot(0, 90, 0) * Solid.make_cone(rod_d / 2, 2, 40)
    helix = Pos(top + helix_at, 0, 0) * Rot(0, 90, 0) * (Cylinder(helix_d / 2, helix_t)
                                                          - Pos(helix_d / 4 + 5, 0, 0) * Box(helix_d / 2, 6, helix_t + 2))
    return eye.fuse(rod, tip, helix)


def wire_grip(wire_d=8.0):
    """Wire rope grip (DIN 741 pattern) in its local frame: two wires along X side by side at y = +/- rr
    (rr = wire_d / 2 + 0.5) on z = 0, the U-bolt round them from below, the saddle and two nuts on top.
    Returns a list of (name, shape, kind)."""
    rr = wire_d / 2 + 0.5
    R = 2 * rr + 4.0
    ub = (Rot(0, 90, 0) * Torus(R, 3.0)) & Pos(0, 0, -R) * Box(20, 4 * R, 2 * R)
    legs = [Pos(0, y, (rr + 22) / 2) * Cylinder(3.0, rr + 22) for y in (-R, R)]
    ubolt = ub.fuse(*legs)
    saddle = Pos(0, 0, rr + 4) * Box(16, 2 * R + 16, 8)
    saddle = saddle - Compound([Pos(0, y, rr + 4) * Cylinder(3.8, 10) for y in (-R, R)])
    nuts = [Pos(0, y, rr + 8) * hex_nut(6) for y in (-R, R)]
    return [("wire rope grip U-bolt", ubolt, "fastener"), ("wire rope grip saddle", saddle, "fastener")] + \
        [("wire rope grip nut", n, "fastener") for n in nuts]
