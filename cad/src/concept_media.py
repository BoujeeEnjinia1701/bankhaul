"""BankHaul concept media (TRL 3, constructable design BKH-DDR-002), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes every component from cad/src/model.py in the shortened picture layout (7 m between the
blocks instead of 30 m) and renders the media set with .kit/concept.py: hero, exploded view with
BOM callouts, concept blueprint (BKH-DWG-010), work flow per haul, and the web model (model.glb
with viewer.html). Coloured parts carry the BOM line numbers of bom/bom.csv; grey parts (bank,
water, bed, the net on the table, person) are context only. Figures on the sheet and in the flow
diagram come from docs/04-calcs/sizing.py (BKH-CAL-001). CONCEPT, NOT FOR FABRICATION.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Compound, Color, Pos, export_gltf  # noqa: E402
import matplotlib.colors as mc  # noqa: E402
from concept import Part, render_all, human_figure, _render  # noqa: E402
from model import PARAMS as P, build_components, context_shapes, bx  # noqa: E402

C = build_components(P, short=True)
X = context_shapes(P, short=True)

STYLE = {  # key: (colour, exploded offset in mm)
    "post": ("#0F766E", (0, 0, 0)),
    "cleats": ("#1D4ED8", (0, 0, 500)),
    "near_block": ("#D4A017", (500, 0, 600)),
    "near_shackle": ("#6B7280", (250, 0, 600)),
    "stay_shackles": ("#6B7280", (-300, 0, 400)),
    "stays": ("#F97316", (-500, 0, 300)),
    "turnbuckles": ("#374151", (-500, 0, 350)),
    "anchors": ("#111827", (-900, 0, -300)),
    "stake": ("#475569", (0, 0, 0)),
    "pin": ("#DC2626", (0, -400, 0)),
    "collar": ("#0E7490", (0, 0, 500)),
    "far_shackle": ("#6B7280", (-250, 0, 650)),
    "far_block": ("#D4A017", (-550, 0, 650)),
    "table": ("#A16207", (1300, 1800, -600)),
    "loop": ("#E11D48", (0, -600, 0)),
    "rings": ("#111827", (0, -900, 300)),
    "bridle": ("#15803D", (0, -900, -200)),
}
S = P["short"]["span"]
FAR = ("stake", "pin", "collar", "far_shackle", "far_block")
parts, compact = [], []
for key, comp in C.items():
    color, off = STYLE[key]
    shape = comp.shape
    if key == "anchors":                      # show only the parts above ground in the pictures
        shape = shape & bx(-3000, 1000, -2000, 2000, 0, 500)
    if key == "stake":                        # and the stake above the bed
        shape = shape & bx(S - 500, S + 500, -500, 500, -1500, 600)
    parts.append(Part(comp.name, shape, color, comp.bom))
    # exploded view: far end drawn beside the bank station, loop cut short
    if key in FAR:
        shape = Pos(-S + 1900, -1000, 900) * shape
    if key in ("loop", "rings"):
        shape = shape & bx(-500, 1800, -500, 500, 0, 1200)
    compact.append(Part(comp.name, shape, color, comp.bom, off))

person = human_figure(1750.0, x=-450.0, y=-1000.0, z=0.0)
context = [Part("Bank (site)", X["bank"] & bx(-1800, 4000, -1500, 1600, -120, 0), "#D6D3D1"),
           Part("Water surface (site)", X["water"] & bx(0, S + 700, -800, 800, -600, 0), "#93C5FD", alpha=0.45),
           Part("Net stacked on the table (site)", X["net"], "#A8A29E"), person]

flow = {"title": "work per haul of a 30 m gillnet with a 10 kg catch, kJ (BKH-CAL-001 estimates)", "unit": "kJ",
        "stages": [("Fisher's hands at the loop and net", 2.8), ("Net leaves the water", 1.6),
                   ("Net up the bank edge", 0.7), ("Catch on the clearing table", "10 kg")],
        "losses": [(0, "Loop round two blocks", 0.55), (0, "Water drag and bed friction", 0.65),
                   (1, "Friction up the bank edge", 0.9)]}

if "--exploded-only" in sys.argv:
    _render(compact, ROOT / "media" / "exploded.png", offsets=True, labels=True, title="BankHaul: exploded view",
            note="Seen from the front right and above, 24 deg elevation; far end drawn beside the bank station and "
                 "the loop cut short; numbers match bom/bom.csv")
    sys.exit(0)

outs = render_all(
    parts, project="BankHaul", title="Bank-hauled net loop concept", dwg_no="BKH-DWG-010",
    key_figures=["Span 30 m between blocks (50 m stretch); 12 mm floating loop",
                 "Peak hand pull about 200 N to haul a 30 m net with 10 kg catch",
                 "Weak link releases at 500 to 700 N; far stake load 1.4 kN at most",
                 "Bank station holds 3 kN: two 250 mm screw anchors, factor 2.1",
                 "Fisher works 5 m or more from the water; nobody wades",
                 "Station parts about USD 382; heaviest lift 26.8 kg (far stake)",
                 "Layout shortened to 7 m in these views"],
    scale_figure=False, context=context, cut=False, web_model=False, flow=flow)

_render(compact, ROOT / "media" / "exploded.png", offsets=True, labels=True, title="BankHaul: exploded view",
        note="Seen from the front right and above, 24 deg elevation; far end drawn beside the bank station and the "
             "loop cut short; numbers match bom/bom.csv")

# Web model at a coarse tessellation (a few MB), with the kit's viewer page
md = ROOT / "media"
kids = []
for p in parts:
    sh = p.shape
    sh.color = Color(*mc.to_rgb(p.color))
    sh.label = p.name
    kids.append(sh)
export_gltf(Compound(kids), str(md / "model.glb"), binary=True, linear_deflection=1.0, angular_deflection=0.35)
(md / "viewer.html").write_text("""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>BankHaul: bank-hauled net loop concept</title>
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3/dist/model-viewer.min.js"></script>
<style>body{margin:0;font-family:system-ui,sans-serif;background:#F9FAFB}model-viewer{width:100vw;height:100vh}
.tag{position:fixed;left:12px;top:10px;font-size:12px;color:#B45309;letter-spacing:.06em}</style></head>
<body><div class="tag">CONCEPT, NOT FOR FABRICATION</div>
<model-viewer src="model.glb" poster="hero.png" alt="BankHaul: bank-hauled net loop concept" camera-controls auto-rotate shadow-intensity="0.6"
  exposure="1.0" camera-orbit="-35deg 70deg auto" interaction-prompt="auto"></model-viewer></body></html>
""")
print({k: str(v) for k, v in outs.items()}, "model.glb", round((md / "model.glb").stat().st_size / 1e6, 2), "MB")
