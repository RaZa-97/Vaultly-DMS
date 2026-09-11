#!/usr/bin/env python3
"""Generate the Vaultly brand assets.

Every SVG in this folder is produced by this script so the icon geometry and
the wordmark stay in sync. Run it from the repository root:

    python branding/build-branding.py

The wordmark is emitted as outlined vector paths taken from Inter
(SIL Open Font License 1.1). Outlining removes the runtime font dependency:
the logo is loaded through an <img> tag, so live SVG <text> would otherwise
resolve fonts on the viewer's machine and render differently per visitor.

Requires: fonttools. The Inter variable font is downloaded to branding/.cache
on first run.
"""

from __future__ import annotations

import base64
import math
import urllib.request
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HERE = Path(__file__).resolve().parent
FONT_URL = (
    "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/"
    "Inter%5Bopsz%2Cwght%5D.ttf"
)
FONT_CACHE = HERE / ".cache" / "Inter.ttf"

# ---------------------------------------------------------------- palette ---
INDIGO = "#4338CA"          # brand indigo, also the UI primary
INDIGO_LIGHT = "#4F46E5"
INDIGO_DEEP = "#3730A3"
TEAL_LIGHT = "#2DD4BF"
TEAL_DEEP = "#0D9488"
LIGHT_INK = "#F8FAFC"       # single colour used on dark backgrounds
SLATE = "#64748B"           # byline on light backgrounds
SLATE_LIGHT = "#CBD5E1"     # byline and divider on dark backgrounds
RULE_LIGHT = "#CBD5E1"

# ------------------------------------------------------------- typography ---
WGHT = 650       # between Semibold and Bold: authoritative without shouting
OPSZ = 32        # display optical size: tighter spacing, finer joins
TRACKING = -0.012


# ==================================================================== font ===
def font() -> TTFont:
    if not FONT_CACHE.exists():
        FONT_CACHE.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(FONT_URL, FONT_CACHE)
    var = TTFont(FONT_CACHE)
    return instancer.instantiateVariableFont(
        var, {"wght": WGHT, "opsz": OPSZ}, inplace=False
    )


def _kerning(f: TTFont) -> dict:
    pairs = {}
    if "GPOS" not in f:
        return pairs
    for lookup in f["GPOS"].table.LookupList.Lookup:
        for sub in lookup.SubTable:
            sub = getattr(sub, "ExtSubTable", sub)
            if lookup.LookupType != 2 or getattr(sub, "Format", None) != 1:
                continue
            covered = sub.Coverage.glyphs
            for i, pairset in enumerate(sub.PairSet):
                for record in pairset.PairValueRecord:
                    value = getattr(record.Value1, "XAdvance", 0) or 0
                    if value:
                        pairs[(covered[i], record.SecondGlyph)] = value
    return pairs


class Typesetter:
    """Turns a string into an outlined SVG path at a given cap height."""

    def __init__(self) -> None:
        self.f = font()
        self.upm = self.f["head"].unitsPerEm
        self.cap = self.f["OS/2"].sCapHeight
        self.cmap = self.f.getBestCmap()
        self.glyphs = self.f.getGlyphSet()
        self.hmtx = self.f["hmtx"]
        self.kern = _kerning(self.f)

    def em_for_cap(self, cap_height: float) -> float:
        return cap_height * self.upm / self.cap

    def draw(self, text, cap_height, x, baseline, tracking=TRACKING):
        """Return (path_data, width). x and baseline are output coordinates."""
        em = self.em_for_cap(cap_height)
        scale = em / self.upm
        names = [self.cmap[ord(c)] for c in text]
        pen = SVGPathPen(self.glyphs, ntos=lambda v: format(v, ".2f"))
        cursor = float(x)
        for i, name in enumerate(names):
            if i:
                cursor += self.kern.get((names[i - 1], name), 0) * scale
            # Flip the y axis: fonts are y-up, SVG is y-down.
            self.glyphs[name].draw(
                TransformPen(pen, Transform(scale, 0, 0, -scale, cursor, baseline))
            )
            cursor += self.hmtx[name][0] * scale + tracking * em
        return pen.getCommands(), cursor - tracking * em - x


# ==================================================================== icon ===
# The mark is defined once in a 64-unit box and scaled everywhere else, so the
# favicon and the logo are the same drawing rather than two similar ones.
BOX = 64.0
C = 32.0                     # centre
RING_R, RING_W = 25.2, 5.8   # dial ring
RING_GAP = 4.0               # four index notches cut into the ring
V_TOP = 21.8                 # top terminals of the V
V_APEX = 44.6                # point of the V
V_OUTER_L = 18.0
V_TERMINAL = 6.9             # width of each top terminal


def _v_path(boost: float = 1.0) -> str:
    """The teal V: a filled outline with flat terminals and a pointed apex."""
    term = V_TERMINAL * boost
    outer_l = V_OUTER_L - (term - V_TERMINAL) / 2
    inner_l = outer_l + term
    outer_r, inner_r = BOX - outer_l, BOX - inner_l
    # The inner edge runs parallel to the outer edge, so each arm keeps a
    # constant width until the two converge on the apex.
    t = (C - inner_l) / (C - outer_l)
    notch_y = V_TOP + (V_APEX - V_TOP) * t
    return (
        "M{:.2f} {:.2f}L{:.2f} {:.2f}L{:.2f} {:.2f}"
        "L{:.2f} {:.2f}L{:.2f} {:.2f}L{:.2f} {:.2f}Z"
    ).format(
        outer_l, V_TOP, C, V_APEX, outer_r, V_TOP,
        inner_r, V_TOP, C, notch_y, inner_l, V_TOP,
    )


def _ring(paint: str, boost: float) -> str:
    """The dial ring, cut by four index notches at the cardinal points.

    The notches are a dash pattern rather than separate tick shapes, so they
    close up optically below ~24 px and the mark degrades to a clean solid
    ring instead of breaking into fragments.
    """
    quarter = 2 * math.pi * RING_R / 4
    return (
        '<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{p}"'
        ' stroke-width="{w:g}" stroke-dasharray="{d:.3f} {g:g}"'
        ' stroke-dashoffset="{o:.3f}"/>'
    ).format(
        c=C, r=RING_R, p=paint, w=RING_W * boost,
        d=quarter - RING_GAP, g=RING_GAP, o=(-RING_GAP / 2) % quarter,
    )


def icon(uid, x=0.0, y=0.0, size=BOX, mono=None, boost=1.0):
    """Return (defs, markup) for the mark. mono renders a single-colour mark."""
    if mono:
        defs = ""
        ring_paint = v_paint = mono
    else:
        defs = (
            '<linearGradient id="{u}-r" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="{il}"/>'
            '<stop offset="1" stop-color="{id_}"/></linearGradient>'
            '<linearGradient id="{u}-v" x1="0" y1="0" x2="0.35" y2="1">'
            '<stop offset="0" stop-color="{tl}"/>'
            '<stop offset="1" stop-color="{td}"/></linearGradient>'
        ).format(u=uid, il=INDIGO_LIGHT, id_=INDIGO_DEEP, tl=TEAL_LIGHT, td=TEAL_DEEP)
        ring_paint = "url(#{}-r)".format(uid)
        v_paint = "url(#{}-v)".format(uid)
    body = _ring(ring_paint, boost) + '<path d="{}" fill="{}"/>'.format(
        _v_path(boost), v_paint
    )
    transform = ""
    if (x, y) != (0.0, 0.0) or size != BOX:
        transform = ' transform="translate({:g} {:g}) scale({:.6g})"'.format(
            x, y, size / BOX
        )
    return defs, "<g{}>{}</g>".format(transform, body)


# ================================================================== assets ===
def svg(width, height, defs, body, title, desc=None) -> str:
    label = "title desc" if desc else "title"
    out = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}"'
        ' width="{w:g}" height="{h:g}" role="img" aria-labelledby="{l}">'
        '<title id="title">{t}</title>'
    ).format(w=width, h=height, l=label, t=title)
    if desc:
        out += '<desc id="desc">{}</desc>'.format(desc)
    if defs:
        out += "<defs>{}</defs>".format(defs)
    return out + body + "</svg>\n"


def b64_png(name: str) -> str:
    data = base64.b64encode((HERE / name).read_bytes()).decode("ascii")
    return "data:image/png;base64," + data


PAD = 8.0
ICON = 64.0
CAP = 34.0
GAP = 24.0          # optical gap between the mark and the wordmark
MARK_DESC = (
    "A teal V shaped like a vault-dial pointer inside an indigo dial ring "
    "cut by four index notches."
)


def build_logo(ts, dark):
    mono = LIGHT_INK if dark else None
    height = 80.0
    cy = height / 2
    defs, mark = icon("vl", PAD, cy - ICON / 2, ICON, mono=mono)
    text_x = PAD + ICON + GAP
    path, width = ts.draw("Vaultly", CAP, text_x, cy + CAP / 2)
    ink = LIGHT_INK if dark else INDIGO
    body = mark + '<path d="{}" fill="{}"/>'.format(path, ink)
    variant = " for dark backgrounds" if dark else ""
    return svg(
        round(text_x + width + PAD, 1), height, defs, body,
        "Vaultly" + variant,
        MARK_DESC + " Followed by the Vaultly wordmark.",
    )


def build_mark(dark):
    mono = LIGHT_INK if dark else None
    defs, mark = icon("vm", mono=mono)
    variant = " for dark backgrounds" if dark else ""
    return svg(BOX, BOX, defs, mark, "Vaultly mark" + variant, MARK_DESC)


def build_favicon(dark):
    # Optically compensated for small sizes: heavier ring, ticks and V.
    mono = LIGHT_INK if dark else None
    defs, mark = icon("vf", mono=mono, boost=1.10)
    variant = " for dark backgrounds" if dark else ""
    return svg(BOX, BOX, defs, mark, "Vaultly favicon" + variant)


BYLINE_CAP = 9.5
BYLINE_TRACK = 0.10
BYLINE_KERN = 5.5   # space between the wordmark and the raised byline
BADGE = 44.0        # well inside the 200 px source resolution


def build_lockup_full(ts, dark):
    mono = LIGHT_INK if dark else None
    height = 96.0
    cy = height / 2
    defs, mark = icon("vk", PAD, cy - ICON / 2, ICON, mono=mono)

    text_x = PAD + ICON + GAP
    # "Vaultly" sits centred on the mark; the byline is set as a superscript,
    # its cap aligned to the top of the wordmark's cap height.
    cap_top = cy - CAP / 2
    word, word_w = ts.draw("Vaultly", CAP, text_x, cap_top + CAP)
    byline_x = text_x + word_w + BYLINE_KERN
    byline, byline_w = ts.draw(
        "BY PBSS", BYLINE_CAP, byline_x, cap_top + BYLINE_CAP,
        tracking=BYLINE_TRACK,
    )
    ink = LIGHT_INK if dark else INDIGO
    sub = SLATE_LIGHT if dark else SLATE
    body = mark + '<path d="{}" fill="{}"/><path d="{}" fill="{}"/>'.format(
        word, ink, byline, sub
    )

    rule_x = byline_x + byline_w + 22.0
    rule = "rgba(248,250,252,0.30)" if dark else RULE_LIGHT
    body += (
        '<path d="M{x:.1f} {a:.1f}V{b:.1f}" stroke="{s}" stroke-width="1"'
        ' fill="none"/>'
    ).format(x=rule_x, a=cy - 26, b=cy + 26, s=rule)

    # The plain white badge vanishes on light surfaces, so the ringed variant
    # is used there. Neither is ever scaled past its 200 px source.
    badge = b64_png("pbss-badge-white.png" if dark else "pbss-badge-white-ring.png")
    badge_x = rule_x + 22.0
    body += (
        '<image href="{h}" x="{x:.1f}" y="{y:.1f}" width="{s:g}" height="{s:g}"/>'
    ).format(h=badge, x=badge_x, y=cy - BADGE / 2, s=BADGE)

    variant = " for dark backgrounds" if dark else ""
    return svg(
        round(badge_x + BADGE + PAD, 1), height, defs, body,
        "Vaultly by PBSS" + variant,
        MARK_DESC + " Followed by the Vaultly wordmark, a raised BY PBSS "
        "byline, and the PBSS company badge.",
    )


def main() -> None:
    ts = Typesetter()
    outputs = {
        "vaultly-logo.svg": build_logo(ts, False),
        "vaultly-logo-dark.svg": build_logo(ts, True),
        "vaultly-lockup-compact.svg": build_logo(ts, False),
        "vaultly-lockup-compact-dark.svg": build_logo(ts, True),
        "vaultly-lockup-full.svg": build_lockup_full(ts, False),
        "vaultly-lockup-full-dark.svg": build_lockup_full(ts, True),
        "vaultly-mark.svg": build_mark(False),
        "vaultly-mark-dark.svg": build_mark(True),
        "vaultly-favicon.svg": build_favicon(False),
        "vaultly-favicon-dark.svg": build_favicon(True),
    }
    for name, content in outputs.items():
        (HERE / name).write_text(content, encoding="utf-8")
        print("{:34} {:>9,} bytes".format(name, len(content)))


if __name__ == "__main__":
    main()
