"""BankHaul prototype build plan pictures (BKH-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py, so the
pictures and the model never disagree:
    docs/05-build-plan/overview.png       every component pulled apart, numbered in build order
    cad/drawings/BKH-DWG-101 to 107       making sketches for the made components
    docs/05-build-plan/joint-NN.png       close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png        one picture per assembly step
Uses .kit/build_views.py. The station is drawn in the shortened layout (7 m between the blocks).
BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from build123d import Pos, Rot, Torus  # noqa: E402
from model import (PARAMS as P, derived, build_components, context_shapes, bx, xcyl, rod, ring_xz,  # noqa: E402
                   fuse, far_parts, table_parts)

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-03"
D = derived(P)
S = P["short"]["span"]
C = {k: c.shape for k, c in build_components(P, short=True).items()}
X = context_shapes(P, short=True)

COL = {"post": "#0F766E", "cleats": "#1D4ED8", "near_block": "#D4A017", "far_block": "#D4A017",
       "near_shackle": "#6B7280", "far_shackle": "#6B7280", "stay_shackles": "#6B7280", "stays": "#F97316",
       "turnbuckles": "#374151", "anchors": "#111827", "stake": "#475569", "pin": "#DC2626", "collar": "#0E7490",
       "table": "#A16207", "loop": "#E11D48", "rings": "#111827", "bridle": "#15803D"}
NAMES = {"post": "Bank post weldment", "cleats": "Jam cleats (2)", "near_block": "Near block",
         "far_block": "Far block", "near_shackle": "Shackle", "far_shackle": "Shackle",
         "stay_shackles": "Stay shackles (2)", "stays": "Back-stays (2)", "turnbuckles": "Turnbuckles (2)",
         "anchors": "Screw ground anchors (2)", "stake": "Far stake", "pin": "Stop pin", "collar": "Swivel collar",
         "table": "Clearing table", "loop": "Rope loop", "rings": "Swivel rings (2)", "bridle": "Net bridle"}


def part(key, shape=None, explode=(0, 0, 0), name=None):
    return Part(name or NAMES[key], C[key] if shape is None else shape, COL[key], None, tuple(explode))


def crop(shape, x0, x1, y0, y1, z0, z1):
    return shape & bx(x0, x1, y0, y1, z0, z1)


def ghost(name, shape):
    return Part(name, shape, "#D1D5DB")


# local shapes for the rope parts' sketches
def stay_piece():
    L = 1440.0
    r = P["stay_d"] / 2
    body = xcyl(0, 0, r, 40, L - 40)
    eyes = [Pos(x, 0, 0) * Torus(28.0, r) for x in (28.0, L - 28.0)]
    tails = [xcyl(0, 0, r * 0.9, x0, x0 + 160) for x0 in (56.0, L - 216.0)]
    return fuse([body] + eyes) + fuse(tails)


def loop_end_piece():
    r = P["rope_d"] / 2
    so = P["swivel"][1]
    ring = fuse([xcyl(0, 0, 9.0, -29, 29), ring_xz(-37, 0, 0, so / 2, so / 2 - 6, 6),
                 Pos(37, 0, 0) * Rot(90, 0, 0) * ring_xz(0, 0, 0, so / 2, so / 2 - 6, 6)])
    eye = (Pos(-37 - 6, 0, 0) * Rot(90, 0, 0) * Torus(40.0, r)) & bx(-200, -43, -60, 60, -60, 60)
    legs = [rod((-43 - 40 * math.cos(a), 0, 40 * math.sin(a) * s), (-190, 0, 8 * s), r)
            for a, s in ((0.0, 1), (0.0, -1))]
    rope = xcyl(0, 0, r, -700, -190) + fuse(legs)
    bury = xcyl(0, 0, r * 1.35, -460, -190)       # the tail buried in the standing part
    return ring, fuse([eye, rope, bury])


def bridle_piece():
    hook = fuse([rod((0, 0, 0), (0, 0, -60), 4.0), Pos(0, 0, 10) * Rot(90, 0, 0) * Torus(12.0, 3.0)])
    weak = Pos(0, 0, -100) * Rot(90, 0, 0) * Torus(40.0, 1.5)
    cord = rod((0, 0, -140), (0, 0, -1500), 3.0)
    return hook, weak, cord


# ----------------------------------------------------------------- overview
def overview():
    far_dx = -S + 3600                                    # bring the far end beside the bank station
    F = {k: Pos(far_dx, 0, 900) * C[k] for k in ("stake", "pin", "collar", "far_shackle", "far_block")}
    F["stake"] = crop(F["stake"], -1e5, 1e5, -1e3, 1e3, -1200, 2000)
    ring, rope = loop_end_piece()
    hook, weak, cord = bridle_piece()
    items = [
        ("Bank post weldment", C["post"], "post", (0, 0, 0)),
        ("Far stake (point cut short)", F["stake"], "stake", (0, 0, 0)),
        ("Swivel collar", F["collar"], "collar", (0, 0, 500)),
        ("Clearing table", C["table"], "table", (1400, 1600, -700)),
        ("Back-stays (2)", C["stays"], "stays", (-300, 0, 300)),
        ("Rope loop halves (2), ends shown", Pos(900, -1300, 300) * rope, "loop", (0, 0, 0)),
        ("Net bridles with weak links (2)", Pos(1700, -1300, 1100) * (hook + weak + cord), "bridle", (0, 0, 0)),
        ("Swivel blocks (2), bought", C["near_block"] + F["far_block"], "near_block", (500, 0, 900)),
        ("Swivel rings (2), bought", Pos(900, -1300, 300) * ring, "rings", (600, 0, 700)),
        ("Jam cleats (2), bought", C["cleats"], "cleats", (0, -500, 550)),
        ("Screw ground anchors (2), bought", C["anchors"], "anchors", (-300, 0, -100)),
        ("Turnbuckles (2), bought", C["turnbuckles"], "turnbuckles", (-500, 0, 150)),
        ("Shackles (6), bought", C["near_shackle"] + C["stay_shackles"] + F["far_shackle"], "near_shackle", (-200, 0, 700)),
        ("Stop pin, bought", F["pin"], "pin", (0, -350, 0)),
    ]
    parts = [Part(n, s, COL[k], None, tuple(e)) for n, s, k, e in items]
    bv.overview(parts, OUT / "overview.png", "BankHaul prototype: every component in build order",
                subtitle="Made parts first (1 to 7), then bought parts; far end drawn beside the bank station",
                key=True, size=(11, 7.5))


# ----------------------------------------------------------------- making sketches
def sheets():
    bank_n = [ghost(k, C[k]) for k in ("cleats", "near_block", "near_shackle", "stay_shackles")]
    stays_n = [ghost("stays", crop(C["stays"], -700, 200, -800, 800, 400, 1100))]
    far_local, _ = far_parts(P)
    stake_c = crop(far_local["stake"], -200, 200, -200, 200, -1300, 600)
    ring, rope = loop_end_piece()
    hook, weak, cord = bridle_piece()
    sheets_ = [
        ("BKH-DWG-101", "Bank post weldment: making sketch", part("post"), bank_n + stays_n, None,
         "48.3 x 3.2 tube; 8 mm plate; 20 mm round bar; zinc-rich paint",
         ["Tube 992 long, ends square; foot plate 350 x 350 x 8 welded under it",
          "Spike 20 round, 400 below the plate centre, ground to a point",
          "Cap disc 60 dia x 8 welded on the top of the tube",
          f"Pad eye 8 plate: 18 hole {P['eye_r']:.0f} from the post axis, {P['z_block']:.0f} up, facing the water",
          f"Two stay lugs 8 plate: 15 holes 960 up, {D['stay_plan_deg']:.0f} deg either side of straight back",
          "Cleat bar 130 x 500 x 8: 48.9 hole, slip on, top 850 up, weld all round",
          "Cleat bar holes: four 9 at 170 and 230 either side; one 15 tie-off hole",
          "Square the tube to the foot plate within 1 deg; weld all round",
          "Check: pad eye hole and lug holes take a 10 mm shackle pin freely"]),
        ("BKH-DWG-102", "Far stake: making sketch", Part("Far stake", far_local["stake"], COL["stake"]),
         [ghost("collar", far_local["collar"]), ghost("pin", far_local["pin"])], None,
         "76.1 x 3.6 tube, S355; 4 mm plate; 6 mm plate; zinc-rich paint",
         [f"Tube {D['stake_len'] - P['point']:,.0f} long; overall {D['stake_len']:,.0f} with the point; 33 kg, two to lift",
          "Point: four 4 mm plate triangles welded to a cone, 150 long",
          "Cap disc 76 dia x 6 welded on the top; it takes every blow",
          f"Five 12.5 cross holes at {P['pin_pitch']:.0f} pitch, the top one 712 below the cap",
          "Drill the holes square through both walls on one line",
          f"Mark a paint ring {P['embed']:,.0f} above the point: drive to this ring at the bed",
          "Paint after drilling; leave the bore open to drain",
          "Check: straight within 10 over the length; the pin slides through every hole"]),
        ("BKH-DWG-103", "Swivel collar: making sketch", Part("Swivel collar", far_local["collar"], COL["collar"]),
         [ghost("stake", stake_c), ghost("pin", far_local["pin"]), ghost("far_shackle", far_local["far_shackle"]),
          ghost("far_block", far_local["far_block"])], None,
         "88.9 x 3.2 tube; 8 mm plate",
         ["Tube 200 long, ends square and deburred inside",
          "Lug 8 plate 60 x 80, 18 hole 75 from the collar axis",
          "Weld the lug on the tube's outside, square to the axis, on the centre line",
          "Bore 82.5 over a 76.1 stake: 3 mm clearance all round, so it turns freely",
          "Check: the collar spins on a stake offcut and drops under its own weight"]),
        ("BKH-DWG-104", "Clearing table: making sketch", Part("Clearing table", table_parts(P), COL["table"]),
         [ghost("net", Pos(-P['table_xy'][0], -P['table_xy'][1], 0) * X["net"])], None,
         "Hardwood or treated softwood; 50 mm galvanised screws",
         ["Top 1,200 x 600, 850 high; five boards 100 x 25 with 25 gaps",
          "Legs 50 x 50 x 750 inset 50 from the ends and the sides",
          "Long rails 75 x 25 outside the legs; end rails 50 x 75 between them",
          "Two lip boards 25 x 75 along the long edges stop the net sliding off",
          "Two screws at every crossing; drill pilot holes in hardwood",
          "Check: stands level on firm ground without rocking"]),
        ("BKH-DWG-105", "Back-stay: making sketch", Part("Back-stay", stay_piece(), COL["stays"]),
         [], None,
         "10 mm three-strand polyester; two thimbles",
         ["Cut 1,800 of rope; tape and melt the ends",
          "Eye splice round a thimble at each end, five full tucks",
          "Length 1,440 between the eye centres after splicing",
          "Shackle one eye to a post lug, the other to the turnbuckle jaw",
          "Make two; check both are the same length within 20"]),
        ("BKH-DWG-106", "Rope loop half and swivel ring: making sketch", Part("Loop half end", rope, COL["loop"]),
         [ghost("ring", ring)], None,
         "12 mm floating polysteel rope; eye-to-eye swivel",
         ["Cut two halves of 55 m from the 120 m coil; tape and melt the ends",
          "Splice a soft eye 80 long round one swivel eye in each half; five tucks",
          "Lead each plain end round the other ring: round turn and two half hitches",
          "Set the length so the rings lie at the blocks when the loop is snug",
          "Seize the knot's tail and coil any surplus at the ring, never between rings",
          "Check: each ring turns freely on its swivel under a hand pull"]),
        ("BKH-DWG-107", "Net bridle with weak link: making sketch", Part("Net bridle", hook + weak + cord, COL["bridle"]),
         [], None,
         "6 mm polyester cord; braided weak link cord; 60 mm stainless snap hook",
         ["Bridle 1,500 of 6 mm cord; bowline to the net's head and foot ropes",
          "Weak link: one loop of the chosen cord, 80 long, joining hook and bridle",
          "Choose the cord by pulling three samples: each must release at 500 to 700 N",
          "Snap hook clips to a swivel ring (far end) or the tie-off hole (near end)",
          "Make two; mark the weak link cord with paint so it is never swapped",
          "Check: the hook opens with one hand and snaps shut by itself"]),
    ]
    revs = {"BKH-DWG-102": [("P1", "Making sketch for the prototype build plan", DATE, "AC"),
                            ("P2", "BKH-DDR-003: stake 5.0 m long, driven 3.5 m (decision 14A)", DATE, "AC")]}
    only = [a for a in sys.argv[2:] if a.startswith("BKH-DWG-")]
    for no, title, p, neigh, vs, mat, notes in sheets_:
        if only and no not in only:
            continue
        r = revs.get(no)
        bv.component_sheet(p, neigh, "BankHaul", no, title, mat, notes, DATE, view_shape=vs,
                           rev=r[-1][0] if r else "P1", revisions=r)
        print("sheet", no)


# ----------------------------------------------------------------- joints
def joint8():
    ring, rope = loop_end_piece()
    hook, weak, cord = bridle_piece()
    other = Rot(0, 0, 180) * rope
    drop = Pos(0, 0, -16)
    return [Part("Swivel ring", ring, COL["rings"]), Part("Loop half, spliced eye", rope & bx(-500, 0, -99, 99, -99, 99), COL["loop"]),
            Part("Other loop half, hitched on", other & bx(0, 500, -99, 99, -99, 99), "#9F1239"),
            Part("Snap hook", drop * hook, "#6B7280"), Part("Weak link", drop * weak, "#FACC15"),
            Part("Net bridle", drop * (cord & bx(-50, 50, -50, 50, -500, -130)), COL["bridle"])]


def joints():
    ro = P["post"][0] / 2
    head = (-150, 450, -200, 200, 850, 1020)
    J = [
        ("joint-01.png", "Near block on the pad eye",
         "Shackle pin through the 18 mm pad eye hole; the shackle bow through the block's swivel eye",
         [part("post", crop(C["post"], *head)), part("near_shackle"), part("near_block"),
          part("loop", crop(C["loop"], -200, 500, -200, 200, 900, 1000))], None),
        ("joint-02.png", "Back-stays on the post lugs",
         "Each stay's thimble eye on a 10 mm shackle through a 15 mm lug hole, 960 mm up",
         [part("post", crop(C["post"], -200, 100, -200, 200, 850, 1020)),
          part("stay_shackles"), part("stays", crop(C["stays"], -400, 0, -300, 300, 700, 1000))], None),
        ("joint-03.png", "Jam cleats on the cleat bar",
         "Each cleat on two M8 bolts through the bar; a loop leg drops into the V to hold",
         [part("post", crop(C["post"], -60, 100, -300, 300, 780, 900)), part("cleats")], None),
        ("joint-04.png", "Foot plate and ground spike, cut open",
         "Spike welded under the plate centre; the tube welded on top; plate bears on the soil",
         [part("post", crop(C["post"], -200, 200, -200, 200, -420, 150))], "+Y"),
        ("joint-05.png", "Screw anchor, turnbuckle and stay",
         "Turnbuckle jaw on the anchor eye; the stay's eye on the other jaw by a shackle; rod in line with the stay",
         [part("anchors", crop(C["anchors"], -1500, -800, 200, 800, -500, 200)),
          part("turnbuckles", crop(C["turnbuckles"], -1500, -800, 200, 800, -100, 400)),
          part("stays", crop(C["stays"], -1300, -800, 200, 800, -100, 400))], None),
        ("joint-06.png", "Swivel collar on the stake, cut open",
         "The collar turns on the stake with 3 mm clearance and rests on the M12 stop pin",
         [part("stake", crop(C["stake"], S - 200, S + 200, -200, 200, -700, -100)), part("pin"), part("collar")], "+Y"),
        ("joint-07.png", "Far block on the collar lug",
         "Shackle pin through the 18 mm lug hole; the bow through the block's swivel eye; the loop round the sheave",
         [part("collar"), part("far_shackle"), part("far_block"),
          part("stake", crop(C["stake"], S - 200, S + 200, -200, 200, -450, -150)),
          part("loop", crop(C["loop"], S - 700, S, -200, 200, -350, -250))], None),
        ("joint-08.png", "Swivel ring, loop eyes and net bridle",
         "One loop half spliced, the other hitched, on the two ring eyes; the bridle's snap hook clips on the ring through the weak link",
         joint8(), None),
    ]
    for fn, title, sub, parts, cut in J:
        bv.joint(parts, OUT / fn, title, sub, cut=cut)
        print("joint", fn)


# ----------------------------------------------------------------- steps
def steps():
    def done(keys):
        return [ghost(NAMES[k], C[k]) for k in keys]
    bank = ["anchors", "post", "stay_shackles", "stays", "turnbuckles", "cleats", "near_shackle", "near_block"]
    far = ["stake", "pin", "collar", "far_shackle", "far_block"]
    stake_vis = crop(C["stake"], S - 300, S + 300, -300, 300, -5100, 100)
    bed = Part("Lake bed (site)", crop(X["bed"], S - 800, S + 800, -800, 800, -1700, -1400), "#E5E7EB")
    water = Part("Water surface (site)", crop(X["water"], S - 800, S + 800, -800, 800, -600, -400), "#E5E7EB")
    T = [
        ("Screw in the two ground anchors", "1,100 mm behind the post spot and 450 mm either side, in line with the stays",
         [], [part("anchors", explode=(0, 0, 500))], []),
        ("Stand the post on its spike", "Push the spike into the ground until the foot plate sits flat; pad eye toward the water",
         done(["anchors"]), [part("post", explode=(0, 0, 600))], []),
        ("Fit the back-stays", "Shackle each stay to a lug; turnbuckle to the anchor eye; take up until the post leans 1 deg landward",
         done(["anchors", "post"]), [part("stay_shackles", explode=(-200, 0, 150)), part("stays", explode=(-250, 0, 200)),
                                     part("turnbuckles", explode=(-300, 0, 100))], []),
        ("Bolt on the jam cleats", "Two M8 bolts each, V toward the water",
         done(["anchors", "post", "stay_shackles", "stays", "turnbuckles"]), [part("cleats", explode=(0, 0, 250))], []),
        ("Hang the near block", "Shackle through the pad eye and the block's swivel eye; mouse the pin",
         done(bank[:6]), [part("near_shackle", explode=(250, 0, 150)), part("near_block", explode=(450, 0, 250))], []),
        ("Drive the far stake from a boat", "5.0 m stake, two to lift; driving cap on the cap disc; drive until the 3.5 m paint ring reaches the bed",
         [], [part("stake", stake_vis, explode=(0, 0, 1200))], [bed, water]),
        ("Fit the stop pin and the collar", "Pin through the hole for the season's level; slide the collar down onto it",
         [ghost("Far stake", stake_vis)], [part("pin", explode=(0, -300, 0)), part("collar", explode=(0, 0, 900))], [water]),
        ("Hang the far block", "Shackle through the collar lug and the block's swivel eye; mouse the pin",
         [ghost("Far stake", stake_vis), ghost("Stop pin", C["pin"]), ghost("Swivel collar", C["collar"])],
         [part("far_shackle", explode=(-250, 0, 150)), part("far_block", explode=(-450, 0, 250))], [water]),
        ("Reeve the loop and join the halves", "From the boat: round the far block, back to the bank, round the near block; rings at the blocks",
         [ghost(NAMES[k], C[k]) for k in bank + far if k not in ("anchors",)],
         [part("loop", explode=(0, 0, 400)), part("rings", explode=(0, 0, 400))], []),
        ("Set up the clearing table", "Landward of the post on the +Y side, clear of the stays; level it",
         done(bank), [part("table", explode=(0, 0, 600))], []),
        ("Clip the net to ring 1", "Far bridle to ring 1 through its weak link; near bridle to the tie-off hole",
         done(bank + ["table"]) + [ghost("Rope loop", crop(C["loop"], -100, 1600, -300, 300, 0, 1100)),
                                   ghost("Swivel rings", crop(C["rings"], -100, 1600, -300, 300, 0, 1100))],
         [part("bridle", explode=(0, -300, 250))], [Part("Net on the table (site)", X["net"], "#E5E7EB")]),
    ]
    only = [int(a[5:]) for a in sys.argv[2:] if a.startswith("step-")]
    for i, (title, sub, dn, new, ctx) in enumerate(T, 1):
        if only and i not in only:
            continue
        bv.step(dn, new, OUT / f"step-{i:02d}.png", f"Step {i}: {title}", sub, context=ctx, label_done=len(dn) <= 6)
        print("step", i)


if __name__ == "__main__":
    which = [a for a in sys.argv[1:] if not a.startswith(("BKH-", "step-"))] or ["overview", "sheets", "joints", "steps"]
    for w in which:
        globals()[w]()
