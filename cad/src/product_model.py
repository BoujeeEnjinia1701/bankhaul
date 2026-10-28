"""BankHaul product appearance model for photoreal renders (STANDARDS sections 12 and 24), TRL 3.

Every product part is components(CHOSEN) from cad/src/model.py as it is, in the 7 m picture layout: the post
weldment with its welds, jam cleats and every bolt, the near and far blocks, every shackle, thimble, stay,
turnbuckle and screw anchor, the clearing table with every screw, the far stake with its point, stop pin and
collar, the two loop halves, the swivel rings and the net bridle. Only the site is added, as context parts: the
earth bank the station stands on, sloping into the water ("Bank (site)"), a net stacked on the table and a
1.75 m mannequin standing on the bank beside the post ("(scale)").

Site scenes need the water to show, and .kit/photoreal.py floods its ground plane with still water when
--water is positive. So the whole model is lifted by LIFT mm: the scene's ground (z = 0) is the lake bed just
offshore, the still water stands 60 mm above it (--water=60) at the model's water level, and the bank is a
site part whose top is the model's ground (z = LIFT). This deviation from "ground level at z = 0" is proposed,
awaiting Amish (BKH-DEC-001 O-4). Studio views put the studio floor at the bank top (--ground-z=LIFT), so the
spike, anchor rods and helixes below ground are hidden. APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "bank" (bank station and table), "far" (far stake above the bed, collar, pin and far block), "loop" (the
whole loop, rings and bridle, for the site view), "bankrope" and "farrope" (the ends of the loop and rings cut
for the studio and detail views), "context".

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Plane, Polygon, Pos, Rot, extrude  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part  # noqa: E402

TITLE = "BankHaul: bank station that sets and hauls a net on a rope loop"
P = M.PARAMS
S = P["short"]["span"]
XW = P["short"]["x_water"]
ZW = P["z_water"]
LIFT = 60.0 - ZW            # water level (model z = -500) lands 60 mm above the scene's ground

_SITE = ["--scene=outdoor", "--ground=mud", "--ground-z=0", "--water=60", "--sun=38,-75", "--lens=35"]
_STUDIO = [f"--ground-z={LIFT:.0f}"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["bank", "loop", "far", "context"], "explode": False, "el": 20, "az": -40, "args": _SITE,
     "note": "Site render from the front right and above (about 20 deg elevation): bank post with its two back-stays and "
             "screw anchors, near block and jam cleats on the earth bank, the loop's two legs running down the bank and "
             "out across the water to the far stake and block, the clearing table with a net, and a 1.75 m person "
             "standing on the bank beside the post; picture layout, 7 m between the blocks"},
    {"name": "studio", "groups": ["bank", "bankrope"], "explode": False, "el": 24, "az": -50, "args": _STUDIO,
     "note": "Studio render of the bank station from the front right and above (about 24 deg elevation): post weldment "
             "with pad eye, stay lugs and cleat bar, near block on its shackle, two jam cleats, back-stays with thimbles, "
             "shackles and turnbuckles to the screw anchors, the clearing table and the bank ends of the loop"},
    {"name": "exploded", "groups": ["bank", "bankrope"], "explode": True, "el": 26, "az": -50, "args": _STUDIO,
     "note": "Exploded bank station from the front right and above (about 26 deg elevation): post weldment, jam cleats "
             "and bolts, near block and shackle, stay shackles, thimbles, back-stays, turnbuckles, screw anchors and table"},
    {"name": "detail", "groups": ["far", "farrope"], "explode": False, "el": 18, "az": -35,
     "note": "Detail of the far end from the front right and above (about 18 deg elevation): stake shown cut 300 mm "
             "below the water line, stop pin bolt, swivel collar resting on it, shackle and far block, with the loop and "
             "ring 2 arriving from the bank"},
]

EXPLODE = {"post": (0, 0, 0), "cleats": (0, 0, 350), "near_block": (550, 0, 350), "near_shackle": (300, 0, 350),
           "stay_shackles": (-250, 0, 300), "stays": (-450, 0, 200), "turnbuckles": (-650, 0, 100),
           "anchors": (-850, 0, 0), "table": (0, 700, 0), "loop": (0, -500, 0), "rings": (0, -700, 250),
           "bridle": (0, -700, -150)}
FAR = ("stake", "pin", "collar", "far_shackle", "far_block")


def _bank_site():
    """Earth bank: flat to the water's edge, then sloping into the water; reaches below the scene's ground."""
    top = LIFT
    pts = [(-3200, top), (XW, top), (XW + 450, -80), (-3200, -80)]
    prof = Plane.XZ * Polygon(*[(x, z) for x, z in pts], align=None)
    slab = extrude(prof, 2600, both=True)
    return slab


def product_parts(P=P):
    L = Pos(0, 0, LIFT)
    out = []

    def add(p, group, explode=(0, 0, 0), shape=None, name=None):
        q = dict(p)
        q["shape"] = L * (shape if shape is not None else p["shape"])
        q["group"] = group
        q["explode"] = tuple(float(v) for v in explode)
        if name:
            q["name"] = name
        out.append(q)

    for p in M.components(M.CHOSEN):
        k = p["key"]
        if k in FAR:
            shp = p["shape"]
            if k == "stake":
                shp = shp & M.bx(S - 300, S + 300, -300, 300, ZW - 300, 200)
                if shp is None or not shp.solids() or shp.volume < 1:
                    continue
            add(p, "far", shape=shp)
        elif k in ("loop", "rings"):
            bank = p["shape"] & M.bx(-600, 2600, -400, 400, -100, 1200)
            if bank is not None and bank.volume > 1:
                add(p, "bankrope", EXPLODE[k], shape=bank, name=p["name"] + " (bank end)")
            far = p["shape"] & M.bx(S - 1600, S + 400, -400, 400, ZW - 300, 200)
            if far is not None and far.volume > 1:
                add(p, "farrope", shape=far, name=p["name"] + " (far end)")
            add(p, "loop")
        elif k == "bridle":
            add(p, "loop", EXPLODE[k])
        else:
            add(p, "bank", EXPLODE.get(k, (0, 0, 0)))
    X = M.context_shapes(P, short=True)
    out.append(part("Net stacked on the table (site)", L * X["net"], "coir_net", kind="context", group="context"))
    out.append(part("Bank (site)", _bank_site(), "soil", kind="context", group="context"))
    from context_parts import mannequin
    person = Pos(-750.0, -950.0, LIFT) * Rot(0, 0, 90) * mannequin(1750, "stand")
    out.append(part("Person, 1.75 m (scale)", person, "skin", kind="context", group="context"))
    for q in out:
        q.setdefault("explode", (0.0, 0.0, 0.0))
    return out


if __name__ == "__main__":
    ps = product_parts()
    for p in ps:
        print(f"{p['name'][:60]:60s} {p['group']:8s} {p['material']:12s}")
    print(len(ps), "parts")
