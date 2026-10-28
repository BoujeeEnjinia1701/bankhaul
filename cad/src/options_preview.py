"""Provisional shaded preview of the concept options picture, media/options.png (BKH-OPT-001).

Run from the repo root:  python cad/src/options_preview.py
Each panel is components(option) from cad/src/model.py (the detailed D3 models, picture layout), shaded with
.kit/concept.py beside the kit's 1.75 m scale figure. It stands in so the repo carries an options picture
until the coordinator renders the kit 1.9 picture in Blender Cycles with `python .kit/options.py`, which
overwrites this file. The picture says so in its header. Repo-specific helper; nothing here is in .kit/.
"""
import sys
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402
import concept  # noqa: E402
import model as M  # noqa: E402

INK, MUTED, ACCENT = "#111827", "#4B5563", "#0F766E"


def panel(key, path):
    parts = []
    for p in M.components(key):
        if p["kind"] == "context":
            continue
        shp = p["shape"]
        if shp.bounding_box().min.Z < -600:
            shp = shp & M.bx(-1e5, 1e5, -1e5, 1e5, -600, 1e5)
            if shp is None or not shp.solids():
                continue
        parts.append(concept.Part(p["name"], shp, p["color"], p.get("bom")))
    from build123d import Compound
    bb = Compound(children=[p.shape for p in parts]).bounding_box()
    parts.append(concept.human_figure(1750.0, x=bb.min.X - 600, y=-900.0, z=0.0))   # on the bank, ground z = 0
    v = M.OPTION_VIEWS.get(key, {})
    concept._render(parts, path, elev=v.get("el", 22), azim=v.get("az", -55), size=(5, 5), dpi=160)
    return Image.open(path).convert("RGB")


def main():
    keys = list(M.OPTIONS)
    n = len(keys)
    with tempfile.TemporaryDirectory() as tmp:
        imgs = [panel(k, Path(tmp) / f"opt-{k}.png") for k in keys]
    fig = plt.figure(figsize=(5.2 * n, 6.6), dpi=160)
    fig.text(0.015, 0.975, f"{M.TITLE}: concept options", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.015, 0.935, "CONCEPT OPTIONS, NOT FOR FABRICATION. PROVISIONAL SHADED PREVIEW of the D3 models; the "
             "Cycles render replaces it. Same 1.75 m figure on the bank in every panel; parts more than 0.6 m below the bank not shown.",
             fontsize=7.5, color="#B45309", va="top")
    fig.text(0.985, 0.975, "github.com/BoujeeEnjinia1701/bankhaul", fontsize=8, color=ACCENT, va="top", ha="right",
             family="monospace")
    for i, (k, im) in enumerate(zip(keys, imgs)):
        ax = fig.add_axes([i / n + 0.01, 0.2, 1 / n - 0.02, 0.68])
        ax.imshow(im)
        ax.axis("off")
        fig.text(i / n + 0.02, 0.17, f"Option {k}: {M.OPTIONS[k]}", fontsize=11, fontweight="bold", color=INK, va="top")
        fig.text(i / n + 0.02, 0.12, textwrap.fill(M.PRINCIPLES.get(k, ""), 52), fontsize=8.5, color=MUTED, va="top")
        if k == M.CHOSEN:
            fig.text((i + 1) / n - 0.02, 0.17, "CURRENT DESIGN", fontsize=8, fontweight="bold", color=ACCENT, va="top",
                     ha="right")
    out = ROOT / "media/options.png"
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
