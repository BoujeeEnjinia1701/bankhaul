"""BankHaul product appearance model (build123d), TRL 3, constructable design (BKH-DDR-002).

For photoreal renders only (.kit/export_views.py, then .kit/photoreal.py on Amish's Mac). Every
part is the model.py solid itself, placed in the shortened picture layout of model.py (7 m between
the blocks); colours and material classes are added for the look. Appearance additions not in
model.py, recorded in docs/REVIEW.md: the loop cut short a little before the water in the hero and
exploded views, the far stake shown above the bed only, the screw anchors shown with their rods,
a net stacked on the table, and a posed 1.75 m mannequin standing beside the post (never between
the camera and the station). CONCEPT, NOT FOR FABRICATION.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Pos, Rot  # noqa: E402
from model import PARAMS as P, build_components, context_shapes, bx  # noqa: E402

TITLE = "BankHaul: bank station that sets and hauls a net on a rope loop"
S = P["short"]["span"]

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "context"], "explode": False, "el": 22, "az": -40,
     "note": "Product render from the front right and above (about 22 deg elevation): bank post with its two "
             "back-stays and screw anchors, near block and jam cleats, the loop's two legs running toward the "
             "water, the clearing table with a net, and a 1.75 m person beside the post"},
    {"name": "exploded", "groups": ["shell"], "explode": True, "el": 26, "az": -50,
     "note": "Exploded bank station from the front right and above (about 26 deg elevation): post weldment, "
             "jam cleats, near block and shackle, stay shackles, back-stays, turnbuckles, screw anchors and table"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 18, "az": -35,
     "note": "Detail of the far end from the front right and above (about 18 deg elevation): stake above the bed, "
             "stop pin, swivel collar, shackle and far block, with the loop and ring 2 arriving from the bank"},
]

LOOK = {  # key: (colour, material class, group, exploded offset)
    "post": ("#0F766E", "painted", "shell", (0, 0, 0)),
    "cleats": ("#1D4ED8", "plastic", "shell", (0, 0, 350)),
    "near_block": ("#D4A017", "metal", "shell", (550, 0, 350)),
    "near_shackle": ("#9CA3AF", "metal", "shell", (300, 0, 350)),
    "stay_shackles": ("#9CA3AF", "metal", "shell", (-250, 0, 300)),
    "stays": ("#F97316", "fabric", "shell", (-450, 0, 200)),
    "turnbuckles": ("#6B7280", "metal", "shell", (-650, 0, 100)),
    "anchors": ("#374151", "metal", "shell", (-850, 0, 0)),
    "table": ("#A16207", "wood", "shell", (0, 700, 0)),
    "loop": ("#E11D48", "fabric", "shell", (0, -500, 0)),
    "rings": ("#9CA3AF", "metal", "shell", (0, -700, 250)),
    "bridle": ("#15803D", "fabric", "shell", (0, -700, -150)),
    "stake": ("#475569", "painted", "internal", (0, 0, 0)),
    "pin": ("#9CA3AF", "metal", "internal", (0, 0, 0)),
    "collar": ("#0E7490", "painted", "internal", (0, 0, 0)),
    "far_shackle": ("#9CA3AF", "metal", "internal", (0, 0, 0)),
    "far_block": ("#D4A017", "metal", "internal", (0, 0, 0)),
}


def product_parts(P=P):
    C = build_components(P, short=True)
    X = context_shapes(P, short=True)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    for k, c in C.items():
        color, mat, grp, ex = LOOK[k]
        shape = c.shape
        if k in ("loop", "rings"):
            add(c.name + " (bank end)", shape & bx(-600, 2600, -400, 400, -100, 1200), color, mat, c.bom, "shell", ex)
            add(c.name + " (far end)", shape & bx(S - 1600, S + 400, -400, 400, -700, 200), color, mat, c.bom,
                "internal", (0, 0, 0))
            continue
        if k == "stake":
            shape = shape & bx(S - 300, S + 300, -300, 300, -1500, 200)
        add(c.name, shape, color, mat, c.bom, grp, ex)
    add("Net stacked on the table (site)", X["net"], "#57534E", "fabric", None, "context", (0, 0, 0))
    from context_parts import mannequin
    person = Pos(-750.0, -950.0, 0) * Rot(0, 0, 90) * mannequin(1750, "stand")
    add("Person, 1.75 m (scale)", person, "#D1D5DB", "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:44s} {p['group']:9s} {p['material']:9s} vol={s.volume / 1000:9.1f} cm3")
