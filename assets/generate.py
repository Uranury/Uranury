"""Draws the profile README's header and social banners as animated SVGs.

GitHub strips CSS and fonts from READMEs, so everything lives inside the SVGs.
The lettering is a hand-drawn 5x7 pixel font to match the pixel-art koi.

Run:  python3 assets/generate.py
"""

from pathlib import Path

OUT = Path(__file__).parent

NAME = "ALIBI ULANULY"
TAGLINE = "Software Engineer · Go Developer · Student at KBTU"

# (label, handle, icon, icon colour)
SOCIALS = {
    "email": ("EMAIL", "alarmy126@gmail.com", "mail", "#f2994a"),
    "twitter": ("TWITTER", "@touna333", "x", "#e6edf3"),
    "linkedin": ("LINKEDIN", "in/alibi-ulanuly", "in", "#4da3ff"),
    "discord": ("DISCORD", "afferenian", "discord", "#8c95ff"),
}

GLYPHS = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "I": ["###", ".#.", ".#.", ".#.", ".#.", ".#.", "###"],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    " ": ["...", "...", "...", "...", "...", "...", "..."],
}

# The name in the header: 10x14 cells at 4px, so its pixels sit closer to the koi's.
TITLE_GLYPHS = {
    "A": ["...####...", "..######..", ".###..###.", ".##....##.", "##......##", "##......##", "##......##",
          "##########", "##########", "##......##", "##......##", "##......##", "##......##", "##......##"],
    "B": ["########..", "#########.", "##.....###", "##......##", "##......##", "##.....###", "########..",
          "#########.", "##.....###", "##......##", "##......##", "##.....###", "#########.", "########.."],
    "I": ["######", "######"] + ["..##.."] * 10 + ["######", "######"],
    "L": ["##........"] * 12 + ["##########", "##########"],
    "N": ["##......##", "###.....##", "####....##", "##.##...##", "##.##...##", "##..##..##", "##..##..##",
          "##...##.##", "##...##.##", "##....####", "##....####", "##.....###", "##......##", "##......##"],
    "U": ["##......##"] * 11 + ["###....###", ".########.", "..######.."],
    "Y": ["##......##", "##......##", "##......##", ".##....##.", ".###..###.", "..######..", "...####..."]
         + ["....##...."] * 7,
    " ": ["....."] * 14,
}

# 12-cell icons drawn on the same 2px grid as the koi.
ICONS = {
    "mail": [
        "############",
        "##........##",
        "#.#......#.#",
        "#..#....#..#",
        "#...#..#...#",
        "#....##....#",
        "#..........#",
        "#..........#",
        "############",
    ],
    "x": [
        "####.....##.",
        "#..#....##..",
        ".#..#..##...",
        "..#..###....",
        "...#..#.....",
        "....#..#....",
        "....##..#...",
        "...##.#..#..",
        "..##...#..#.",
        ".##.....#..#",
        "##......####",
    ],
    "in": [
        ".##########.",
        "############",
        "##..########",
        "############",
        "##..#....###",
        "##..#..#..##",
        "##..#..##.##",
        "##..#..##.##",
        "##..#..##.##",
        "##..#..##.##",
        "############",
        ".##########.",
    ],
    "discord": [
        ".##......##.",
        ".##########.",
        "############",
        "############",
        "###..##..###",
        "###..##..###",
        "############",
        "############",
        ".###....###.",
        "..#......#..",
    ],
}

THEMES = {
    "light": dict(ink="#0b3d91", glint="#4da3ff", shadow="#f2994a", ripple="#4da3ff", sub="#57606a"),
    "dark": dict(ink="#e6edf3", glint="#58a6ff", shadow="#1f6feb", ripple="#58a6ff", sub="#8b949e"),
}

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


def text_pixels(text, font=GLYPHS, gap=1):
    """Return (column, row) for every lit pixel, plus the total width in columns."""
    pixels, x = [], 0
    for ch in text:
        glyph = font[ch]
        for row, line in enumerate(glyph):
            for col, c in enumerate(line):
                if c == "#":
                    pixels.append((x + col, row))
        x += len(glyph[0]) + gap
    return pixels, x - gap


def header(theme):
    t = THEMES[theme]
    w, h, px = 800, 180, 4
    pixels, cols = text_pixels(NAME, TITLE_GLYPHS, gap=2)
    x0, y0 = (w - cols * px) // 2, 36

    columns = {}
    for c, r in pixels:
        columns.setdefault(c, []).append(r)

    groups = []
    for c in sorted(columns):
        x = x0 + c * px
        shadow = "".join(f'<rect x="{x + 4}" y="{y0 + r * px + 4}" width="{px}" height="{px}"/>' for r in columns[c])
        ink = "".join(f'<rect x="{x}" y="{y0 + r * px}" width="{px}" height="{px}"/>' for r in columns[c])
        groups.append(
            f'<g class="col" style="animation-delay:{c * 0.0125:.4f}s">'
            f'<g fill="{t["shadow"]}">{shadow}</g><g fill="url(#shine)">{ink}</g></g>'
        )

    name_w = cols * px
    ripples = []
    for i, (cx, cy, delay) in enumerate([(x0 - 50, 70, 0), (x0 + name_w + 50, 80, 1.7), (x0 - 70, 92, 3.1)]):
        ripples.append(
            f'<ellipse cx="{cx}" cy="{cy}" rx="0" ry="0" fill="none" stroke="{t["ripple"]}" stroke-width="1.5" opacity="0">'
            f'<animate attributeName="rx" values="0;34" dur="4.5s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animate attributeName="ry" values="0;9" dur="4.5s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.8;0" dur="4.5s" begin="{delay}s" repeatCount="indefinite"/>'
            f"</ellipse>"
        )

    # Typewriter tagline: a clip rect widens one character at a time.
    sub_w, sub_y, n = 520, 146, len(TAGLINE)
    sub_x = (w - sub_w) // 2
    steps = ";".join(f"{sub_w * i / n:.1f}" for i in range(n + 1))
    cursor = ";".join(f"{sub_x + sub_w * i / n + 2:.1f}" for i in range(n + 1))

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Alibi Ulanuly — {TAGLINE}">
<style>
  .col {{ animation: drop .6s cubic-bezier(.3,1.6,.5,1) both; }}
  @keyframes drop {{ from {{ transform: translateY(-36px); opacity: 0; }} to {{ transform: none; opacity: 1; }} }}
  @media (prefers-reduced-motion: reduce) {{ .col {{ animation: none; }} }}
</style>
<defs>
  <linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="{x0}" y1="0" x2="{x0 + name_w}" y2="0" gradientTransform="translate(-{name_w} 0)">
    <stop offset="0" stop-color="{t['ink']}"/>
    <stop offset="0.42" stop-color="{t['ink']}"/>
    <stop offset="0.5" stop-color="{t['glint']}"/>
    <stop offset="0.58" stop-color="{t['ink']}"/>
    <stop offset="1" stop-color="{t['ink']}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-{name_w};-{name_w};{name_w}" keyTimes="0;0.55;1" dur="7s" begin="1.2s" repeatCount="indefinite"/>
  </linearGradient>
  <clipPath id="type"><rect x="{sub_x}" y="{sub_y - 16}" width="0" height="24">
    <animate attributeName="width" values="{steps}" calcMode="discrete" dur="2.4s" begin="1.1s" fill="freeze"/>
  </rect></clipPath>
</defs>
{''.join(ripples)}
{''.join(groups)}
<text x="{sub_x}" y="{sub_y}" textLength="{sub_w}" lengthAdjust="spacing" font-family="{MONO}" font-size="15" fill="{t['sub']}" clip-path="url(#type)">{TAGLINE}</text>
<rect x="{sub_x + 2}" y="{sub_y - 13}" width="8" height="16" fill="{t['shadow']}">
  <animate attributeName="x" values="{cursor}" calcMode="discrete" dur="2.4s" begin="1.1s" fill="freeze"/>
  <animate attributeName="opacity" values="1;0" calcMode="discrete" dur="1s" repeatCount="indefinite"/>
</rect>
</svg>
"""


def pixel_text(text, x, y, s):
    pixels, _ = text_pixels(text)
    return "".join(f'<rect x="{x + c * s}" y="{y + r * s}" width="{s}" height="{s}"/>' for c, r in pixels)


# Underwater palette for the social cards: stepped water bands (top to bottom),
# the waves rolling along the seabed, and the rim.
WATER = ["#0f3d5e", "#0d3354", "#0b2a4a", "#0a2240"]
WAVE_BACK, WAVE_FRONT, FOAM = "#0f4a6b", "#13607f", "#5fc4d9"
RIM = "#1f6f8b"


def wave(w, base, s, heights, fill, crest):
    """A pixel wave: one column per entry in `heights`, repeated across 2 extra periods so it can scroll."""
    period = len(heights) * s
    body, foam = [], []
    for x in range(-period, w + period, s):
        hgt = heights[(x // s) % len(heights)]
        top = base - hgt * s
        body.append(f'<rect x="{x}" y="{top + s}" width="{s}" height="{base - top}"/>')
        foam.append(f'<rect x="{x}" y="{top}" width="{s}" height="{s}"/>')
    return f'<g fill="{fill}">{"".join(body)}</g><g fill="{crest}">{"".join(foam)}</g>', period


def banner(key, index):
    label, handle, icon, colour = SOCIALS[key]
    w, h = 190, 56
    # Card with notched pixel corners.
    n = 4
    card = f"M{n},0H{w - n}V{n}H{w}V{h - n}H{w - n}V{h}H{n}V{h - n}H0V{n}H{n}Z"
    s = 2
    grid = ICONS[icon]
    iy = (h - len(grid) * s) // 2
    icon_px = "".join(
        f'<rect x="{14 + c * s}" y="{iy + r * s}" width="{s}" height="{s}"/>'
        for r, line in enumerate(grid)
        for c, ch in enumerate(line)
        if ch == "#"
    )
    delay = index * 1.1

    band = h / len(WATER)
    water = "".join(
        f'<rect x="0" y="{i * band:.0f}" width="{w}" height="{band + 1:.0f}" fill="{c}"/>' for i, c in enumerate(WATER)
    )
    back, back_p = wave(w, h - 2, 2, [1, 2, 2, 3, 4, 4, 3, 2, 1, 1, 1, 1], WAVE_BACK, WAVE_FRONT)
    front, front_p = wave(w, h - 2, 2, [0, 1, 1, 2, 3, 2, 1, 0, 0, 0], WAVE_FRONT, FOAM)

    # Bubbles drift up from the icon, staggered so one is always in flight.
    bubbles = "".join(
        f'<rect class="bubble" x="{bx}" y="16" width="{bs}" height="{bs}" style="animation-delay:{delay + bd:.1f}s"/>'
        for bx, bs, bd in [(42, 2, 0), (45, 3, 1.3), (41, 2, 2.4)]
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label.title()}: {handle}">
<style>
  .bob {{ animation: bob 2.4s steps(2, jump-none) {delay:.1f}s infinite; }}
  @keyframes bob {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-2px); }} }}
  .ray {{ animation: ray 7s ease-in-out {delay:.1f}s infinite; }}
  @keyframes ray {{ 0%, 60% {{ transform: translateX(-60px) skewX(-25deg); }} 100% {{ transform: translateX({w + 40}px) skewX(-25deg); }} }}
  .back {{ animation: back 3.2s steps({back_p // 2}) infinite; }}
  @keyframes back {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-{back_p}px); }} }}
  .front {{ animation: front 2s steps({front_p // 2}) infinite; }}
  @keyframes front {{ from {{ transform: translateX(0); }} to {{ transform: translateX({front_p}px); }} }}
  .bubble {{ opacity: 0; animation: rise 3.6s steps(8) infinite; }}
  @keyframes rise {{ 0% {{ transform: translateY(0); opacity: 0; }} 15% {{ opacity: .9; }} 100% {{ transform: translateY(-16px); opacity: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{ .bob, .ray, .back, .front, .bubble {{ animation: none; }} }}
</style>
<defs><clipPath id="card"><path d="{card}"/></clipPath></defs>
<g clip-path="url(#card)">
  {water}
  <rect class="ray" x="0" y="-10" width="18" height="{h + 20}" fill="#7fd4ff" opacity="0.07" transform="translate(-60 0)" style="transform-origin:0 0"/>
  <g class="back" opacity="0.85">{back}</g>
  <g class="front" opacity="0.8">{front}</g>
  <rect x="0" y="0" width="4" height="{h}" fill="{colour}"/>
</g>
<path d="{card}" fill="none" stroke="{RIM}" stroke-width="4" clip-path="url(#card)"/>
<g fill="#bfeaf5">{bubbles}</g>
<g class="bob" fill="{colour}">{icon_px}</g>
<g fill="#e6edf3">{pixel_text(label, 52, 12, 2)}</g>
<text x="52" y="43" font-family="{MONO}" font-size="11" fill="#9edcf0">{handle}</text>
</svg>
"""


def main():
    for theme in THEMES:
        (OUT / f"header-{theme}.svg").write_text(header(theme), encoding="utf-8")
    for i, key in enumerate(SOCIALS):
        (OUT / f"{key}.svg").write_text(banner(key, i), encoding="utf-8")


if __name__ == "__main__":
    main()
