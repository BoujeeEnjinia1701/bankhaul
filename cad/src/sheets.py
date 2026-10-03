"""BankHaul drawing sheets, Rev P2 (TRL 3, constructable design BKH-DDR-002).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/BKH-DWG-001 (bank station, general arrangement), BKH-DWG-002 (far end, general
arrangement) and BKH-DWG-003 (station layout, shortened) as SVG, PDF and PNG from cad/src/model.py
with .kit/drawing.py. Overall sizes are dimensioned by the kit; main dimensions and interfaces are
listed in the notes, taken from PARAMS and derived(). The concept blueprint in media/ is BKH-DWG-010;
the making sketches for the build plan are BKH-DWG-101 onward (cad/src/build_plan_media.py).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Compound, Pos  # noqa: E402
from drawing import Sheet  # noqa: E402
from model import PARAMS as P, build_components, derived  # noqa: E402

DATE = "2026-10-03"
REVS = [("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
        ("P2", "BKH-DDR-002: design for construction", DATE, "AC")]


def safe_project_views(part, workdir, line_weight=0.35):
    """Front, top, right and iso views, edge by edge, so a degenerate edge is skipped."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center()
    d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out = {}
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    pass
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    return out


def bank_sheet(C, D):
    keys = ["post", "cleats", "near_block", "near_shackle", "stay_shackles", "stays", "turnbuckles", "anchors"]
    work = ROOT / "cad" / "drawings" / "_views1"
    views = safe_project_views(Compound([C[k].shape for k in keys]), work)
    s = Sheet(project="BankHaul", title="Bank station: general arrangement", dwg_no="BKH-DWG-001", rev="P2",
              author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="Steel weldment, bought blocks, anchors and rigging per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=REVS)
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 32, 140, 92, label="Isometric view", sublabel="Not to scale; ground at z = 0")
    s.add_notes("Main dimensions and interfaces (mm)", [
        "Post 48.3 x 3.2 tube, head 1,000 above the ground; weldment 17.2 kg (1)",
        "Foot plate 350 x 350 x 8; ground spike 20 round, 400 below the plate",
        f"Pad eye 18 hole {P['eye_r']:.0f} from the post axis, {P['z_block']:.0f} up; near block on a shackle (8, 13)",
        f"Near sheave centre {D['x_near']:.0f} in front of the post; legs {2 * D['r_pitch']:.0f} apart",
        f"Two stay lugs, 15 holes, {D['z_lug']:.0f} up, splayed {D['stay_plan_deg']:.1f} deg either side of the line",
        "Back-stays 10 rope with M12 turnbuckles to the anchor eyes (5, 12)",
        f"Anchor eyes 1,100 behind and 450 either side; rods in line with the stays (11)",
        "Cleat bar 130 x 500 x 8 slipped over the post, top 850 up; jam cleats 200 either side (10)",
        "Tie-off hole 15 dia in the cleat bar for the net's near end",
        "Third-angle; front view from -Y; the loop runs out to +X; (n) = BOM line",
    ], x=276, y=135, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "BKH-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print("wrote", out)


def far_sheet(C, D):
    keys = ["stake", "pin", "collar", "far_shackle", "far_block"]
    work = ROOT / "cad" / "drawings" / "_views2"
    shape = Compound([Pos(-P["span"], 0, 0) * C[k].shape for k in keys])
    views = safe_project_views(shape, work)
    s = Sheet(project="BankHaul", title="Far end: stake, swivel collar and far block, general arrangement",
              dwg_no="BKH-DWG-002", rev="P2", author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="Steel tube S355 per bom/bom.csv; bought block and shackle. PRELIMINARY, NOT FOR FABRICATION",
              revisions=REVS)
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 32, 140, 92, label="Isometric view", sublabel="Not to scale")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Stake 76.1 x 3.6 S355 tube, {D['stake_len']:,.0f} long overall with a 150 point; 26.8 kg (2)",
        f"Driven {P['embed']:,.0f} into the bed; design water depth {P['water_depth']:,.0f}; top 500 above the water",
        "Cap disc 6 thick takes the driving cap; never drive on the open tube",
        f"Five 12.5 holes at {P['pin_pitch']:.0f} pitch for the M12 stop pin (14)",
        "Collar 88.9 x 3.2 x 200 turns on the stake and rests on the pin (3)",
        f"Collar lug 8 thick, 18 hole {P['far_eye_r']:.0f} from the stake axis",
        f"Far sheave {P['z_far_above_water']:.0f} above the water at the design level (8, 13)",
        "Move the pin up or down a hole to follow the season's water level",
        "Lateral capacity: BKH-CAL-001, section E",
        "Third-angle; front view from -Y; the loop arrives from -X; (n) = BOM line",
    ], x=276, y=135, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "BKH-DWG-002")
    shutil.rmtree(work, ignore_errors=True)
    print("wrote", out)


def layout_sheet(C, D):
    work = ROOT / "cad" / "drawings" / "_views3"
    views = safe_project_views(Compound([C[k].shape for k in C if k not in ("anchors",)]), work, line_weight=0.25)
    s = Sheet(project="BankHaul", title="Net-hauling station: layout (span shortened)", dwg_no="BKH-DWG-003", rev="P2",
              author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="Layout only; parts per BKH-DWG-001, 002 and 101 to 107. PRELIMINARY, NOT FOR FABRICATION",
              revisions=REVS)
    s.add_ortho(views, names=("front", "top"))
    s.add_svg(views["iso"], 276, 32, 140, 92, label="Isometric view", sublabel="Not to scale; span shortened to 7 m")
    s.add_notes("Layout rules (mm)", [
        f"Design span {P['span']:,.0f} between sheave centres; stretch {P['span_max']:,.0f} (R2)",
        f"Post at least {P['x_water']:,.0f} back from the water's edge (R11)",
        "The fisher works within 1,000 of the post, never nearer the water",
        "Loop legs 112 apart, floating; the net is set along the -Y leg",
        "Net no longer than the span less 2,000, so no ring reaches a block",
        "Loop direction within the stays' splay (22 deg either side)",
        "Clearing table landward on the +Y side, clear of the stays",
        "Far stake set from a boat or at low water, never by wading",
        "Nobody in the bight of the loop or in line with a loaded stay",
        "Third-angle; front view from -Y; X along the loop",
    ], x=276, y=135, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "BKH-DWG-003")
    shutil.rmtree(work, ignore_errors=True)
    print("wrote", out)


if __name__ == "__main__":
    D = derived(P)
    C = build_components(P, short=False)
    bank_sheet(C, D)
    far_sheet(C, D)
    layout_sheet(build_components(P, short=True), D)
