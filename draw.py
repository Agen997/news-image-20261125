#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news front page, 'THE DAILY GLOBE'.

Fresh design, written from scratch for the news-image-20261125 bounty:
a navy-and-gold broadsheet on warm paper. Lead: the Gaza strikes.
All stories verified against Reuters / BBC / AP / One Turn reporting
of Wednesday 25 November 2026. Output: entry.png, 1024x1024.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 233)
NAVY = (20, 33, 61)
NAVY2 = (30, 48, 88)
NAVY3 = (13, 22, 44)
GOLD = (201, 162, 39)
GOLD_LT = (226, 196, 110)
RED = (163, 22, 33)
INK = (26, 26, 26)
GRAY = (96, 92, 80)
ORANGE = (216, 108, 44)
SMOKE = (150, 148, 140)
WHITE = (250, 248, 242)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines fitting width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill, leading=None):
    """Draw wrapped paragraph; returns y after the last line."""
    if leading is None:
        leading = int(fnt.size * 1.32)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, color, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def draw_globe(draw, cx, cy, r):
    """Simple line globe: circle, meridians, parallels."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD_LT, width=3)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=GOLD_LT, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=GOLD_LT, width=2)
    draw.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45],
             start=200, end=340, fill=GOLD_LT, width=2)
    draw.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45],
             start=20, end=160, fill=GOLD_LT, width=2)


def draw_lead_art():
    """Night skyline over Gaza: silhouettes, smoke, searchlights."""
    px0, py0, px1, py1 = 624, 152, 1000, 436
    panel = Image.new("RGBA", (px1 - px0, py1 - py0), (0, 0, 0, 0))
    d = ImageDraw.Draw(panel)
    # sky gradient bands
    for i in range(py1 - py0):
        t = i / (py1 - py0)
        c = tuple(int(NAVY3[k] + (NAVY2[k] - NAVY3[k]) * t) for k in range(3))
        d.line([(0, i), (px1 - px0, i)], fill=c + (255,))
    # stars
    import random
    rnd = random.Random(25)
    for _ in range(46):
        sx = rnd.randint(4, px1 - px0 - 4)
        sy = rnd.randint(4, 110)
        r = rnd.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(235, 230, 210, 255))
    # crescent moon
    d.ellipse([300, 22, 344, 66], fill=(240, 232, 200, 255))
    d.ellipse([312, 16, 352, 62], fill=NAVY2 + (255,))
    # searchlight beams (translucent)
    beam = Image.new("RGBA", panel.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(beam)
    bd.polygon([(60, 250), (120, 250), (210, 30), (170, 30)],
               fill=(255, 240, 190, 60))
    bd.polygon([(300, 250), (330, 250), (250, 60), (225, 60)],
               fill=(255, 240, 190, 46))
    panel = Image.alpha_composite(panel, beam)
    d = ImageDraw.Draw(panel)
    # smoke plume
    for (sx, sy, sr, col) in [(150, 120, 34, ORANGE), (168, 92, 44, SMOKE),
                              (140, 66, 30, SMOKE), (185, 60, 26, (190, 186, 176))]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=col + (235,))
    d.ellipse([138, 108, 176, 146], fill=(232, 120, 50, 255))
    # buildings
    base = py1 - py0
    for (bx, bw, bh, lit) in [(0, 62, 120, True), (58, 46, 168, True),
                              (100, 70, 96, False), (166, 52, 150, True),
                              (214, 64, 110, False), (274, 48, 176, True),
                              (318, 58, 128, False)]:
        d.rectangle([bx, base - bh, bx + bw, base], fill=(8, 14, 30, 255))
        if lit:
            for wy in range(base - bh + 14, base - 10, 26):
                for wx in range(bx + 10, bx + bw - 8, 20):
                    if rnd.random() < 0.55:
                        d.rectangle([wx, wy, wx + 7, wy + 10],
                                    fill=(255, 214, 120, 255))
    return panel, (px0, py0)


def draw_shop_icon(d, x, y):
    """Tiny storefront with striped awning."""
    d.rectangle([x, y + 18, x + 64, y + 46], outline=NAVY, width=3)
    d.rectangle([x + 8, y + 28, x + 26, y + 46], outline=NAVY, width=2)
    d.rectangle([x + 38, y + 28, x + 56, y + 46], outline=NAVY, width=2)
    for i, cx in enumerate(range(x, x + 64, 16)):
        col = RED if i % 2 == 0 else WHITE
        d.polygon([(cx, y + 4), (cx + 16, y + 4), (cx + 13, y + 20),
                   (cx + 3, y + 20)], fill=col, outline=NAVY)


def draw_rocket_icon(d, x, y):
    """Tiny rocket launching."""
    d.ellipse([x + 22, y - 2, x + 42, y + 34], fill=NAVY)
    d.polygon([(x + 22, y + 22), (x + 8, y + 38), (x + 24, y + 32)], fill=RED)
    d.polygon([(x + 42, y + 22), (x + 56, y + 38), (x + 40, y + 32)], fill=RED)
    d.ellipse([x + 27, y + 8, x + 37, y + 18], fill=GOLD_LT)
    d.polygon([(x + 28, y + 36), (x + 36, y + 36), (x + 32, y + 50)],
              fill=ORANGE)
    d.ellipse([x + 26, y + 44, x + 38, y + 54], fill=(255, 214, 120))


def draw_derrick_icon(d, x, y):
    """Tiny oil derrick."""
    d.line([(x + 10, y + 48), (x + 26, y + 2)], fill=NAVY, width=3)
    d.line([(x + 54, y + 48), (x + 26, y + 2)], fill=NAVY, width=3)
    d.line([(x + 14, y + 34), (x + 50, y + 34)], fill=NAVY, width=2)
    d.line([(x + 19, y + 20), (x + 45, y + 20)], fill=NAVY, width=2)
    d.line([(x + 26, y + 2), (x + 44, y + 2)], fill=NAVY, width=3)
    d.ellipse([x + 40, y - 4, x + 52, y + 8], fill=GOLD)
    d.rectangle([x + 2, y + 44, x + 62, y + 50], fill=NAVY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header band ----
    d.rectangle([0, 0, W, 104], fill=NAVY)
    draw_globe(d, 58, 52, 34)
    d.text((106, 24), "THE DAILY GLOBE", font=SERIF_B(50), fill=WHITE)
    for (txt, y, fnt, col) in [
            ("WEDNESDAY", 22, SANS_B(25), GOLD_LT),
            ("25 NOVEMBER 2026", 54, SANS_B(23), WHITE)]:
        d.text((1000 - d.textlength(txt, font=fnt), y), txt, font=fnt,
               fill=col)
    rule(d, 0, 104, W, GOLD, 4)

    # ---- kicker strip ----
    d.text((24, 118), "THE WORLD IN ONE PAGE", font=SANS_B(19), fill=NAVY)
    d.text((560, 118), "COMPILED FROM REUTERS, BBC, AP",
           font=SANS(17), fill=GRAY)
    rule(d, 24, 148, 1000, NAVY, 1)

    # ---- lead story ----
    d.text((24, 164), "GAZA  •  LEAD STORY", font=SANS_B(20), fill=RED)
    y = 190
    for line in wrap(d, "ISRAELI STRIKE KILLS SECOND HAMAS SECURITY "
                        "CHIEF IN A DAY", SERIF_B(36), 584):
        d.text((24, y), line, font=SERIF_B(36), fill=INK)
        y += 46
    y += 6
    y = para(d, 24, y,
             "An early-morning strike on a Gaza City apartment kills "
             "Mohammad Abuelouf, his wife and two children — hours after "
             "Hamas internal security chief Naeem Abu Nahel was killed "
             "on Tuesday.",
             SANS(20), 576, INK, leading=25)

    art, (ax, ay) = draw_lead_art()
    img.paste(art, (ax, ay), art)
    d = ImageDraw.Draw(img)
    d.text((624, 444), "Gaza City, after the early-morning strike.",
           font=SERIF(16), fill=GRAY)
    rule(d, 24, 458, 600, GOLD, 2)

    # ---- three middle columns ----
    cols = [
        (24, "LATIN AMERICA", draw_shop_icon,
         "HOSTAGES FREED AFTER CARTAGENA SUPERMARKET SIEGE",
         "Armed men held about 20 people in a supermarket in "
         "Cartagena, Colombia. All hostages were freed."),
        (356, "SPACE", draw_rocket_icon,
         "PAKISTAN'S FIRST ASTRONAUT REACHES CHINA'S SPACE STATION",
         "China's Shenzhou-24 launches from Jiuquan, carrying "
         "Pakistan's first astronaut to the Chinese space station."),
        (688, "MIDDLE EAST", draw_derrick_icon,
         "HOUTHIS SAY THEY HIT SAUDI REFINERY AND RIYADH",
         "Yemen's Houthis claim strikes on the Ras Tanura refinery "
         "and Riyadh; Saudi defences say four drones were "
         "intercepted."),
    ]
    for (x, chip, icon, head, body) in cols:
        icon(d, x + 4, 474)
        d.text((x + 84, 486), chip, font=SANS_B(19), fill=RED)
        rule(d, x, 528, x + 288, NAVY, 1)
        y = 540
        for line in wrap(d, head, SERIF_B(23), 288):
            d.text((x, y), line, font=SERIF_B(23), fill=INK)
            y += 29
        y += 4
        para(d, x, y, body, SANS(18), 288, INK, leading=23)

    rule(d, 24, 758, 1000, NAVY, 1)

    # ---- also today ----
    d.text((24, 772), "ALSO TODAY", font=SANS_B(20), fill=NAVY)
    briefs = [
        ("DR CONGO", "Military aircraft missing; rebels claim they shot "
         "it down."),
        ("INDONESIA", "Rescuers search for dozens of miners trapped in a "
         "flooded mine."),
        ("SPAIN", "Country heads to a snap election."),
        ("PACIFIC", "Solomon Islands and Australia sign a security "
         "treaty."),
    ]
    bx, bw = 24, 238
    for (tag, text) in briefs:
        d.text((bx, 806), tag, font=SANS_B(17), fill=RED)
        para(d, bx, 830, text, SANS(16), bw, INK, leading=20)
        bx += bw + 6

    # ---- markets footer ----
    d.rectangle([0, 916, W, 1000], fill=NAVY)
    d.text((24, 928), "MARKETS", font=SANS_B(20), fill=GOLD_LT)
    d.text((150, 928), "AI SELL-OFF DEEPENS AS TARIFF FEARS RETURN",
           font=SANS_B(19), fill=WHITE)
    sport = "SPORT — Real Madrid 5–1 PSV"
    d.text((1000 - d.textlength(sport, font=SANS_B(17)), 930), sport,
           font=SANS_B(17), fill=GOLD_LT)
    d.text((24, 962),
           "Nikkei −2.8%   •   Nasdaq −1.5%   •   S&P 500 −0.5%   •   "
           "Brent $87.41   •   Gold $3,516   •   Bitcoin $59,258",
           font=SANS(18), fill=(210, 208, 198))

    d.text((24, 1006), "Wednesday, 25 November 2026  •  Sources: Reuters, "
                        "BBC, AP, AFP",
           font=SANS(14), fill=GRAY)

    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
