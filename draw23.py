#!/usr/bin/env python3
"""Front page for make.fun's news-image-20261123 contest: the world news
of Monday 23 November 2026, drawn as one newspaper page.

Every story below was verified against at least two published sources
dated 23 November 2026:
  1. LEAD — Nvidia reinstates Jensen Huang as chief executive, 11 days
     after he resigned; shares jump about 33%.
     (OneTurn, Daily Mirror, NYT.)
  2. Iran vows to use all available means against the US naval blockade;
     Iran says it shot down a US drone over the Persian Gulf; Trump says
     US strikes could resume after the New Year if no deal is reached.
     (Just Security Early Edition 23 Nov, OneTurn, Algemeiner.)
  3. Ukraine sinks the Russian corvette Merkury at Benghazi port, Libya,
     with seven naval drones; Zelenskyy hails the operation.
     (OneTurn, Daily Mirror.)
  4. The EU proposes its 22nd sanctions package on Russia: about 60 more
     banks cut from SWIFT, crypto platforms targeted, 70+ shadow-fleet
     vessels listed, plus sports and visa bans.
     (Reuters, LB.ua, APA, UATV.)
  5. Bangladesh vows to arrest former prime minister Sheikh Hasina if
     she returns from India.
     (Just Security, Daily Mirror.)
  6. India pledges 1.4 billion euros to help Nepal rebuild after the
     August glacier floods; Nepal PM Balendra Shah visits New Delhi.
     (OneTurn, Daily Summary of World.)
Ticker: US stocks rebound sharply after the AI sell-off (S&P 500 up
4.82%; Nikkei fell over 5%) -- Houthis claim an attack on a Saudi oil
refinery -- Germany's Merz calls on Russia to stop "dangerous
provocations".

Deliberately left out, because they happened or were first reported on
an earlier day: the COP31 collapse (22 Nov), the capture of "Chapo
Isidro" (21 Nov), the Dymer apartment strike (22 Nov), the Democrats
winning 258 House seats (22 Nov), the Trump-Xi-Putin Shenzhen summit
(19-20 Nov), the Iranian strike on Bahrain (21 Nov), and the S&P 500
Friday fall (20 Nov).

Flat-shape illustrations only -- no photos and no borrowed artwork.
Running this file writes entry.png (1024 x 1024) next to it.
"""

import math

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
PAPER = (248, 243, 233)
INK = (24, 24, 24)
RED = (176, 46, 38)
GREY = (98, 98, 98)
GREEN = (18, 110, 60)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Split text into lines that each fit inside width (measured)."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_block(draw, x, y, text, fnt, fill, width, max_bottom,
               centre=False, gap=1.15):
    """Draw wrapped text starting at (x, y); assert it stays above
    max_bottom so nothing ever overflows its panel."""
    lines = wrap(draw, text, fnt, width)
    for line in lines:
        lx = x + (width - draw.textlength(line, font=fnt)) / 2 if centre else x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += int(fnt.size * gap)
    assert y <= max_bottom, (
        f"text block overflows: ends at y={y}, panel bottom is {max_bottom} "
        f"for text starting {text[:40]!r}")
    return y


def panel_head(draw, x, y, w, tag, head, body, bottom,
               head_size=23, body_size=16):
    draw.text((x, y), tag, font=font(BOLD, 18), fill=RED)
    y = draw_block(draw, x, y + 25, head, font(BOLD, head_size), INK, w,
                   bottom, gap=1.12)
    draw_block(draw, x, y + 4, body, font(PLAIN, body_size), GREY, w,
               bottom, gap=1.18)


# ------------------------------------------------------------------ scenes
def scene_chip(d, x, y, w, h):
    """A green computer chip on a dark board, with a rising share-price
    chart and a big +33% -- Nvidia's comeback day."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 42, 30))
    # circuit traces
    for ty in (0.18, 0.42, 0.68):
        d.line([x + 12, y + h * ty, x + w - 12, y + h * ty],
               fill=(34, 84, 58), width=2)
    # the chip, centre-left
    cx, cy = x + w * 0.34, y + h * 0.52
    cw, ch = w * 0.34, h * 0.56
    for k in range(4):
        px = cx - cw / 2 + k * cw / 3
        d.line([px, cy - ch / 2 - 12, px, cy - ch / 2], fill=(120, 200, 140),
               width=3)
        d.line([px, cy + ch / 2, px, cy + ch / 2 + 12], fill=(120, 200, 140),
               width=3)
    d.rectangle([cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2],
                fill=(18, 110, 60), outline=(150, 230, 170), width=3)
    d.rectangle([cx - cw / 4, cy - ch / 4, cx + cw / 4, cy + ch / 4],
                fill=(10, 70, 40), outline=(150, 230, 170), width=2)
    # rising chart, right of the chip
    pts = []
    for i, (fx, fy) in enumerate(((0.56, 0.72), (0.64, 0.66), (0.72, 0.70),
                                  (0.80, 0.52), (0.88, 0.44), (0.95, 0.26))):
        pts.append((x + w * fx, y + h * fy))
    d.line(pts, fill=(255, 210, 90), width=5, joint="curve")
    ax, ay = pts[-1]
    d.polygon([(ax, ay - 16), (ax + 16, ay + 4), (ax - 2, ay + 10)],
              fill=(255, 210, 90))
    d.text((x + w * 0.56, y + h * 0.06), "+33%", font=font(BOLD, 44),
           fill=(255, 210, 90))


def scene_blockade(d, x, y, w, h):
    """Grey sea under a pale sky: a warship on the horizon, a small
    drone overhead with a dashed flight path -- the Gulf standoff."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 232))
    d.ellipse([x + w * 0.08, y + h * 0.08, x + w * 0.24, y + h * 0.20],
              fill=(255, 244, 200))
    # drone in the sky, right side
    dx, dy = x + w * 0.72, y + h * 0.22
    d.line([x + w * 0.30, dy + 14, dx - 22, dy + 14], fill=GREY, width=2)
    d.rectangle([dx - 22, dy - 6, dx + 22, dy + 6], fill=(60, 64, 72))
    d.rectangle([dx - 6, dy - 14, dx + 6, dy + 14], fill=(60, 64, 72))
    d.ellipse([dx - 30, dy - 3, dx - 18, dy + 3], fill=RED)
    d.ellipse([dx + 18, dy - 3, dx + 30, dy + 3], fill=RED)
    # sea
    base = y + h * 0.58
    d.rectangle([x, base, x + w, y + h], fill=(30, 78, 110))
    for wy in (0.66, 0.76, 0.88):
        d.line([x + 10, y + h * wy, x + w - 10, y + h * wy],
               fill=(120, 170, 200), width=2)
    # warship silhouette
    sx0 = x + w * 0.10
    d.polygon([(sx0, base + h * 0.10), (sx0 + w * 0.52, base + h * 0.10),
               (sx0 + w * 0.46, base + h * 0.26),
               (sx0 + w * 0.08, base + h * 0.26)], fill=(52, 58, 66))
    d.rectangle([sx0 + w * 0.14, base - h * 0.06, sx0 + w * 0.30,
                 base + h * 0.10], fill=(52, 58, 66))
    d.line([sx0 + w * 0.20, base - h * 0.06, sx0 + w * 0.20,
            base - h * 0.18], fill=(52, 58, 66), width=4)
    d.rectangle([sx0 + w * 0.55, base + h * 0.02, sx0 + w * 0.58,
                 base + h * 0.10], fill=RED)


def scene_drones(d, x, y, w, h):
    """Night at the harbour: a grey corvette at anchor, three small
    naval drones closing in with white wakes, an orange blast."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 30, 48))
    for sx, sy in ((0.10, 0.10), (0.42, 0.06), (0.78, 0.12), (0.92, 0.05)):
        px, py = x + w * sx, y + h * sy
        d.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(255, 255, 255))
    d.ellipse([x + w * 0.80, y + h * 0.06, x + w * 0.94, y + h * 0.20],
              fill=(240, 238, 220))
    base = y + h * 0.62
    d.rectangle([x, base, x + w, y + h], fill=(10, 42, 66))
    # corvette
    hx0 = x + w * 0.34
    d.polygon([(hx0, base + h * 0.04), (hx0 + w * 0.58, base + h * 0.04),
               (hx0 + w * 0.50, base + h * 0.18),
               (hx0 + w * 0.06, base + h * 0.18)], fill=(120, 126, 134))
    d.rectangle([hx0 + w * 0.10, base - h * 0.10, hx0 + w * 0.30,
                 base + h * 0.04], fill=(120, 126, 134))
    d.line([hx0 + w * 0.16, base - h * 0.10, hx0 + w * 0.16,
            base - h * 0.24], fill=(120, 126, 134), width=4)
    # blast where the drones hit, at the bow
    bx, by = hx0 + w * 0.52, base - h * 0.02
    for r, col in ((26, (255, 205, 90)), (16, (240, 120, 40)),
                   (8, (255, 240, 180))):
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=col)
    # three drone boats with wakes, lower left
    for fx, fy in ((0.08, 0.82), (0.20, 0.90), (0.06, 0.94)):
        px, py = x + w * fx, y + h * fy
        d.rectangle([px, py, px + 22, py + 7], fill=(200, 200, 200))
        d.line([px - 26, py + 3, px, py + 3], fill=(220, 230, 240), width=2)


def scene_eu(d, x, y, w, h):
    """EU blue with a ring of gold stars, a bank building crossed by a
    red cut, and a small shadow-fleet ship below."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 48, 110))
    cx, cy, r = x + w * 0.50, y + h * 0.30, min(30, int(h * 0.24))
    for k in range(12):
        ang = -math.pi / 2 + k * math.pi / 6
        sx, sy = cx + r * math.cos(ang), cy + r * math.sin(ang)
        d.polygon([(sx, sy - 5), (sx + 1.5, sy - 1.5), (sx + 5, sy),
                   (sx + 1.5, sy + 1.5), (sx, sy + 5), (sx - 1.5, sy + 1.5),
                   (sx - 5, sy), (sx - 1.5, sy - 1.5)], fill=(255, 210, 0))
    # bank building, lower half
    bx0, by0 = x + w * 0.22, y + h * 0.56
    bw, bh = w * 0.56, h * 0.30
    d.polygon([(bx0 - 6, by0), (bx0 + bw / 2, by0 - h * 0.10),
               (bx0 + bw + 6, by0)], fill=(235, 235, 230))
    d.rectangle([bx0, by0, bx0 + bw, by0 + bh], fill=(235, 235, 230))
    for k in range(3):
        px = bx0 + bw * (0.16 + k * 0.28)
        d.rectangle([px, by0 + 6, px + bw * 0.12, by0 + bh - 6],
                    fill=(24, 48, 110))
    # red cut across the bank
    d.line([bx0 - 8, by0 + bh + 4, bx0 + bw + 8, by0 - 8], fill=RED, width=5)
    # small ship, bottom strip
    d.rectangle([x + w * 0.68, y + h - 16, x + w * 0.94, y + h - 8],
                fill=(150, 150, 150))
    d.rectangle([x + w * 0.76, y + h - 26, x + w * 0.82, y + h - 16],
                fill=(150, 150, 150))


def scene_court(d, x, y, w, h):
    """A courthouse in Dhaka green: columns, a flag, and a wooden
    gavel -- an arrest vowed on return."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 96, 60))
    # flag on a pole, top left
    d.line([x + 14, y + 10, x + 14, y + 44], fill=(255, 255, 255), width=3)
    d.rectangle([x + 14, y + 10, x + 44, y + 26], fill=(0, 106, 78))
    d.ellipse([x + 22, y + 13, x + 34, y + 23], fill=RED)
    # courthouse: pediment and three columns
    cx = x + w * 0.50
    base = y + h - h * 0.22
    d.polygon([(x + w * 0.10, base - h * 0.52),
               (cx, base - h * 0.68),
               (x + w * 0.90, base - h * 0.52)], fill=(240, 234, 220))
    for kx in (0.18, 0.44, 0.70):
        px = x + w * kx
        d.rectangle([px, base - h * 0.50, px + w * 0.08, base],
                    fill=(240, 234, 220))
    d.rectangle([x + w * 0.10, base, x + w * 0.90, base + h * 0.06],
                fill=(200, 190, 170))
    # gavel, bottom right
    gx, gy = x + w * 0.72, y + h - h * 0.16
    d.rectangle([gx, gy, gx + 34, gy + 12], fill=(120, 76, 40))
    d.line([gx + 17, gy + 12, gx + 30, gy + 34], fill=(120, 76, 40), width=5)
    d.rectangle([x, base + h * 0.06, x + w, y + h], fill=(10, 60, 38))


def scene_mountains(d, x, y, w, h):
    """Himalayan peaks with snow caps, a half-rebuilt house below, and
    a rising sun -- Nepal rebuilds with India's help."""
    d.rectangle([x, y, x + w, y + h], fill=(180, 214, 230))
    d.ellipse([x + w * 0.68, y + h * 0.06, x + w * 0.90, y + h * 0.28],
              fill=(255, 214, 110))
    base = y + h - h * 0.30
    # three peaks, snow-capped
    for px0, pw, ph, col in ((0.02, 0.44, 0.62, (90, 110, 140)),
                             (0.34, 0.52, 0.72, (70, 92, 122)),
                             (0.66, 0.36, 0.52, (100, 122, 150))):
        apex = (x + w * (px0 + pw / 2), base - h * ph)
        d.polygon([(x + w * px0, base), apex, (x + w * (px0 + pw), base)],
                  fill=col)
        d.polygon([apex, (apex[0] - w * pw * 0.14, apex[1] + h * ph * 0.30),
                   (apex[0] + w * pw * 0.14, apex[1] + h * ph * 0.30)],
                  fill=(255, 255, 255))
    # half-rebuilt house: frame on the left, finished wall on the right
    hx0 = x + w * 0.30
    d.rectangle([hx0, base, hx0 + w * 0.40, base + h * 0.24],
                fill=(190, 150, 110))
    d.polygon([(hx0 - 6, base), (hx0 + w * 0.20, base - h * 0.16),
               (hx0 + w * 0.40 + 6, base)], fill=(150, 60, 50))
    d.rectangle([hx0 + w * 0.16, base + h * 0.10, hx0 + w * 0.26,
                 base + h * 0.24], fill=(90, 60, 40))
    d.rectangle([x, base + h * 0.24, x + w, y + h], fill=(110, 140, 90))


# ------------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(img)
    M = 36

    d.text((PAGE / 2, 18), "T H E   W O R L D   I N   O N E   I M A G E",
           font=font(BOLD, 26), fill=INK, anchor="ma")
    date_font = font(BOLD, 58)
    while d.textlength("MONDAY 23 NOVEMBER 2026", font=date_font) > PAGE - 2 * M:
        date_font = font(BOLD, date_font.size - 2)
    d.text((PAGE / 2, 52), "MONDAY 23 NOVEMBER 2026", font=date_font,
           fill=INK, anchor="ma")
    d.line([M, 138, PAGE - M, 138], fill=INK, width=5)
    d.line([M, 146, PAGE - M, 146], fill=INK, width=2)

    # lead: Huang returns to Nvidia, shares jump 33%
    d.rectangle([M, 162, PAGE - M, 442], outline=INK, width=3)
    scene_chip(d, M + 10, 172, 452, 260)
    lx = M + 486
    lw = PAGE - M - lx - 8
    d.text((lx, 180), "TECH \u00b7 NVIDIA", font=font(BOLD, 22), fill=RED)
    y = draw_block(d, lx, 212, "HUANG RETURNS TO NVIDIA",
                   font(BOLD, 38), INK, lw, 442 - 10, gap=1.12)
    draw_block(d, lx, y + 8,
               "Jensen Huang is chief executive again, 11 days after "
               "he resigned \u2014 and shares jump about 33% as "
               "investors cheer the comeback.",
               font(PLAIN, 21), GREY, lw, 442 - 10, gap=1.2)

    # row of three: Iran, Ukraine, EU
    y0, y1 = 456, 724
    cw = (PAGE - 2 * M - 24) // 3
    cells = [
        (scene_blockade, "IRAN \u00b7 US STANDOFF",
         "IRAN VOWS TO FIGHT US BLOCKADE",
         "Tehran says it shot down a US drone over the Gulf; Trump "
         "warns strikes could resume after the New Year."),
        (scene_drones, "UKRAINE \u00b7 LIBYA",
         "UKRAINE SINKS RUSSIAN CORVETTE",
         "Seven naval drones strike the Merkury at Benghazi port; "
         "Zelenskyy hails the operation."),
        (scene_eu, "EU \u00b7 SANCTIONS",
         "EU READIES 22ND SANCTIONS PACKAGE",
         "About 60 more banks cut from SWIFT, crypto platforms hit, "
         "70+ shadow-fleet ships listed, plus sports and visa bans."),
    ]
    for i, (scene, tag, head, body) in enumerate(cells):
        x0 = M + i * (cw + 12)
        d.rectangle([x0, y0, x0 + cw, y1], outline=INK, width=3)
        scene(d, x0 + 8, y0 + 8, cw - 16, 78)
        panel_head(d, x0 + 12, y0 + 94, cw - 24, tag, head, body, y1 - 8,
                   head_size=23, body_size=16)

    # row of two: Bangladesh, Nepal
    y0, y1 = 738, 950
    cw2 = (PAGE - 2 * M - 12) // 2
    cells2 = [
        (scene_court, "BANGLADESH \u00b7 POLITICS",
         "DHAKA VOWS TO ARREST HASINA",
         "Bangladesh says it will arrest former prime minister "
         "Sheikh Hasina if she returns from India."),
        (scene_mountains, "INDIA \u00b7 NEPAL",
         "INDIA PLEDGES \u20ac1.4BN FOR NEPAL",
         "New Delhi will help rebuild after the August glacier "
         "floods, as Nepal PM Balendra Shah visits."),
    ]
    for i, (scene, tag, head, body) in enumerate(cells2):
        x0 = M + i * (cw2 + 12)
        d.rectangle([x0, y0, x0 + cw2, y1], outline=INK, width=3)
        scene(d, x0 + 8, y0 + 8, 168, y1 - y0 - 16)
        panel_head(d, x0 + 188, y0 + 12, cw2 - 200, tag, head, body,
                   y1 - 8, head_size=24, body_size=18)

    # ticker
    d.line([M, 958, PAGE - M, 958], fill=INK, width=3)
    ticker = ("ALSO TODAY \u00b7 US stocks rebound after the AI sell-off "
              "(S&P 500 up 4.82%; Nikkei fell over 5%) \u00b7 Houthis claim "
              "an attack on a Saudi oil refinery \u00b7 Germany\u2019s Merz "
              "calls on Russia to stop \u201cdangerous provocations\u201d")
    tick_font = font(BOLD, 18)
    while len(wrap(d, ticker, tick_font, PAGE - 2 * M)) > 2:
        tick_font = font(BOLD, tick_font.size - 1)
    draw_block(d, M, 966, ticker, tick_font, INK, PAGE - 2 * M, 1024 - 4,
               centre=True, gap=1.12)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
