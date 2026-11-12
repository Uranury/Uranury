"""Adds pixel ripples that trail behind the koi in koi.gif.

git-koi draws the koi on a transparent background. For each frame this finds
the koi's centre, drops a ripple there every few frames, and lets each ripple
spread and break up as it fades. Ripples sit underneath the koi and wrap
around the loop, so the GIF still loops seamlessly.

Run:  python3 koi/ripples.py [in.gif] [out.gif]   (defaults to koi/koi.gif in place)
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageSequence

PX = 2  # git-koi draws in 2x2 pixels; ripples use the same grid.
EVERY = 8  # frames between ripples
LIFE = 34  # frames a ripple lives
GROWTH = 0.55  # radius gained per frame, in koi pixels
# Readable on both GitHub's light and dark backgrounds.
COLOURS = ["#9fd3ff", "#4da3ff", "#3b82c4"]


def centre(frame):
    """Centroid of the koi's opaque pixels, in koi-pixel units."""
    alpha = frame.getchannel("A").reduce(PX)
    w, _ = alpha.size
    xs = ys = n = 0
    for i, a in enumerate(alpha.tobytes()):
        if a:
            xs += i % w
            ys += i // w
            n += 1
    return (xs / n, ys / n) if n else None


def ring(draw, cx, cy, r, colour, broken):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=1)
    if broken:
        # Knock out every other pixel along the ring so it reads as fading.
        for y in range(int(cy - r) - 1, int(cy + r) + 2):
            for x in range(int(cx - r) - 1, int(cx + r) + 2):
                if (x + y) % 2:
                    draw.point((x, y), fill=(0, 0, 0, 0))


def add_ripples(src, dst):
    with Image.open(src) as gif:
        duration = gif.info.get("duration", 70)
        frames = [f.convert("RGBA") for f in ImageSequence.Iterator(gif)]
    count = len(frames)
    w, h = frames[0].size
    centres = [centre(f) for f in frames]

    out = []
    for t, koi in enumerate(frames):
        water = Image.new("RGBA", (w // PX, h // PX), (0, 0, 0, 0))
        draw = ImageDraw.Draw(water)
        # Oldest ripples first, so newer ones draw over them.
        for age in range(LIFE - 1, -1, -1):
            spawn = (t - age) % count
            if spawn % EVERY or centres[spawn] is None:
                continue
            cx, cy = centres[spawn]
            r = 3 + age * GROWTH
            stage = min(len(COLOURS) - 1, age * len(COLOURS) // LIFE)
            ring(draw, round(cx), round(cy), round(r), COLOURS[stage], broken=age > LIFE * 0.6)
            if r * 0.55 >= 7 and age < LIFE * 0.6:
                ring(draw, round(cx), round(cy), round(r * 0.55), COLOURS[stage], broken=True)
        frame = water.resize((w, h), Image.NEAREST)
        frame.alpha_composite(koi)
        out.append(frame)

    out[0].save(
        dst,
        save_all=True,
        append_images=out[1:],
        duration=duration,
        loop=0,
        disposal=2,
        optimize=False,
    )


if __name__ == "__main__":
    here = Path(__file__).parent
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else here / "koi.gif"
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src
    add_ripples(src, dst)
