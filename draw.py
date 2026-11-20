#!/usr/bin/env python3
"""Render the Thursday 19 November 2026 world-news front page.

One 1024x1024 PNG, fully deterministic: fixed geometry, fixed fonts,
no randomness, no network access. Six stories, all dated 19 Nov 2026:
  1. Xi hosts Trump and Putin in Shenzhen (first trilateral summit)
  2. ICJ finds Myanmar committed genocide against the Rohingya
  3. Ukraine strikes the Kerch Bridge rail section again
  4. Israel wraps up its Gaza ground raid beyond the Yellow Line
  5. Anthropic's Nasdaq debut as ANT, record $81.3bn raise
  6. US Senate rejects the Iran war-powers resolution, 48-51
"""
import math

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
CREAM = (248, 246, 239)
BLACK = (20, 20, 20)
RED = (150, 30, 30)
MUTED = (95, 92, 85)

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
SERIF_BOLD = FONT_DIR + "LiberationSerif-Bold.ttf"
SERIF = FONT_DIR + "LiberationSerif-Regular.ttf"
SANS_BOLD = FONT_DIR + "LiberationSans-Bold.ttf"
SANS = FONT_DIR + "LiberationSans-Regular.ttf"


def load(path, px):
    return ImageFont.truetype(path, px)


def split_text(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    out, current = [], ""
    for word in words:
        candidate = (current + " " + word).strip()
        if draw.textlength(candidate, font=fnt) <= width:
            current = candidate
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def shrink_to_fit(draw, text, path, px, width, limit=2):
    """Lower the point size until the text wraps into at most `limit` lines."""
    while px > 13:
        fnt = load(path, px)
        lines = split_text(draw, text, fnt, width)
        if len(lines) <= limit:
            return fnt, lines
        px -= 1
    fnt = load(path, px)
    return fnt, split_text(draw, text, fnt, width)[:limit]


def five_star(draw, cx, cy, outer, fill):
    """Draw a filled five-point star centred on (cx, cy)."""
    points = []
    for step in range(10):
        angle = math.radians(-90 + step * 36)
        radius = outer if step % 2 == 0 else outer * 0.40
        points.append((cx + radius * math.cos(angle),
                       cy + radius * math.sin(angle)))
    draw.polygon(points, fill=fill)


# ---------------------------------------------------------------- pictures
def pic_summit(draw, x0, y0, x1, y1):
    """A globe with three stars above it: three leaders, one table."""
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2 + 8
    for sx in (cx - 88, cx, cx + 88):
        five_star(draw, sx, y0 + 26, 15, RED if sx == cx else BLACK)
    draw.ellipse([cx - 62, cy - 48, cx + 62, cy + 48], outline=BLACK, width=4)
    draw.ellipse([cx - 26, cy - 48, cx + 26, cy + 48], outline=BLACK, width=2)
    draw.line([(cx - 62, cy), (cx + 62, cy)], fill=BLACK, width=2)
    draw.arc([cx - 62, cy - 48, cx + 62, cy + 48], 200, 340, fill=BLACK, width=2)
    draw.line([(x0 + 30, y1 - 10), (x1 - 30, y1 - 10)], fill=BLACK, width=3)


def pic_scales(draw, x0, y0, x1, y1):
    """The scales of justice: a post, a beam and two hanging pans."""
    cx = (x0 + x1) // 2
    beam_y = y0 + 34
    draw.line([(cx, y0 + 12), (cx, y1 - 16)], fill=BLACK, width=5)
    draw.line([(cx - 96, beam_y), (cx + 96, beam_y)], fill=BLACK, width=4)
    five_star(draw, cx, y0 + 12, 10, RED)
    for side in (-1, 1):
        px = cx + side * 96
        draw.line([(px, beam_y), (px - 26, beam_y + 46)], fill=BLACK, width=2)
        draw.line([(px, beam_y), (px + 26, beam_y + 46)], fill=BLACK, width=2)
        draw.arc([px - 26, beam_y + 34, px + 26, beam_y + 58], 0, 180,
                 fill=BLACK, width=3)
    draw.line([(x0 + 24, y1 - 16), (x1 - 24, y1 - 16)], fill=BLACK, width=3)


def pic_bridge(draw, x0, y0, x1, y1):
    """An arched bridge over water, with a blast bursting mid-span."""
    mid = (x0 + x1) // 2
    deck_y = y1 - 42
    draw.line([(x0 + 14, deck_y), (x1 - 14, deck_y)], fill=BLACK, width=4)
    draw.arc([x0 + 40, deck_y - 62, x1 - 40, deck_y + 62], 180, 360,
             fill=BLACK, width=4)
    for post_x in (x0 + 78, mid, x1 - 78):
        draw.line([(post_x, deck_y - 30), (post_x, deck_y)], fill=BLACK, width=3)
    draw.line([(x0 + 40, deck_y), (x0 + 40, y1 - 18)], fill=BLACK, width=3)
    draw.line([(x1 - 40, deck_y), (x1 - 40, y1 - 18)], fill=BLACK, width=3)
    burst_y = deck_y - 44
    for k in range(10):
        angle = math.radians(k * 36)
        tip = 30 if k % 2 == 0 else 18
        draw.line([(mid + 9 * math.cos(angle), burst_y + 9 * math.sin(angle)),
                   (mid + tip * math.cos(angle), burst_y + tip * math.sin(angle))],
                  fill=RED, width=3)
    draw.ellipse([mid - 10, burst_y - 10, mid + 10, burst_y + 10], fill=RED)
    for wave_y in (deck_y + 14, deck_y + 24):
        wave = [(xx, wave_y + 3 * math.sin(xx / 13.0))
                for xx in range(x0 + 24, x1 - 20, 4)]
        draw.line(wave, fill=MUTED, width=2)


def pic_tank(draw, x0, y0, x1, y1):
    """A tank hull with a turret, crossing a dashed yellow line."""
    cx = (x0 + x1) // 2
    body_y = y0 + 62
    draw.line([(x0 + 10, y1 - 22), (x1 - 10, y1 - 22)], fill=BLACK, width=2)
    for seg in range(6):
        sx = x0 + 22 + seg * 34
        draw.line([(sx, y1 - 22), (sx + 18, y1 - 22)], fill=(214, 164, 32),
                  width=5)
    draw.rectangle([cx - 74, body_y, cx + 74, body_y + 26], fill=BLACK)
    draw.rectangle([cx - 30, body_y - 26, cx + 34, body_y], fill=BLACK)
    draw.line([(cx + 34, body_y - 16), (cx + 96, body_y - 24)], fill=BLACK,
              width=6)
    for wheel in range(5):
        wx = cx - 58 + wheel * 29
        draw.ellipse([wx - 9, body_y + 28, wx + 9, body_y + 46], fill=BLACK)
    draw.text((x0 + 16, y0 + 6), "YELLOW LINE", font=load(SANS_BOLD, 15),
              fill=MUTED)


def pic_chart(draw, x0, y0, x1, y1):
    """A steeply rising share-price line with a ticker label."""
    base = y1 - 20
    draw.line([(x0 + 26, y0 + 12), (x0 + 26, base)], fill=BLACK, width=2)
    draw.line([(x0 + 26, base), (x1 - 14, base)], fill=BLACK, width=2)
    pts = [(x0 + 44, base - 14), (x0 + 96, base - 20), (x0 + 148, base - 18),
           (x0 + 200, base - 44), (x0 + 252, base - 50), (x0 + 304, base - 76),
           (x0 + 356, base - 84)]
    draw.line(pts, fill=RED, width=5)
    tip_x, tip_y = pts[-1]
    draw.polygon([(tip_x, tip_y - 14), (tip_x + 14, tip_y + 2),
                  (tip_x - 2, tip_y + 2)], fill=RED)
    draw.text((x0 + 34, y0 + 8), "ANT  $83 \u2192 $111.50",
              font=load(SANS_BOLD, 20), fill=BLACK)


def pic_capitol(draw, x0, y0, x1, y1):
    """A domed capitol building above the 48-51 tally."""
    cx = (x0 + x1) // 2
    draw.arc([cx - 52, y0 + 2, cx + 52, y0 + 62], 180, 360, fill=BLACK, width=4)
    draw.rectangle([cx - 78, y0 + 52, cx + 78, y0 + 64], fill=BLACK)
    for col in range(5):
        col_x = cx - 62 + col * 31
        draw.rectangle([col_x, y0 + 64, col_x + 11, y0 + 88], fill=BLACK)
    draw.rectangle([cx - 86, y0 + 88, cx + 86, y0 + 96], fill=BLACK)
    tally = load(SERIF_BOLD, 26)
    text = "48 \u2013 51"
    draw.text(((x1 + x0 - draw.textlength(text, font=tally)) / 2, y0 + 100),
              text, font=tally, fill=RED)


STORIES = [
    ("XI HOSTS TRUMP & PUTIN IN SHENZHEN",
     "First-ever trilateral summit; Peace Declaration signed",
     pic_summit),
    ("ICJ: MYANMAR COMMITTED GENOCIDE",
     "Historic 9-6 ruling on the Rohingya; a first for the court",
     pic_scales),
    ("UKRAINE HITS KERCH BRIDGE AGAIN",
     "Neptune missiles hit the rail section; third strike in a week",
     pic_bridge),
    ("ISRAEL ENDS GAZA GROUND RAID",
     "Tanks pull back beyond the Yellow Line; tunnel dismantled",
     pic_tank),
    ("ANTHROPIC SOARS ON NASDAQ DEBUT",
     "Record $81.3bn raise; opened $111.50, closed $97.17",
     pic_chart),
    ("SENATE REJECTS IRAN WAR POWERS",
     "48-51 vote; first Iran war vote since the midterms",
     pic_capitol),
]


def build():
    canvas = Image.new("RGB", (SIZE, SIZE), CREAM)
    draw = ImageDraw.Draw(canvas)

    # ---- masthead ----
    title_font = load(SERIF_BOLD, 60)
    title = "THE WORLD TODAY"
    draw.text(((SIZE - draw.textlength(title, font=title_font)) / 2, 16),
              title, font=title_font, fill=BLACK)
    dateline_font = load(SANS_BOLD, 19)
    dateline = ("THURSDAY 19 NOVEMBER 2026  \u2022  GLOBAL EDITION  "
                "\u2022  $2.00")
    draw.text(((SIZE - draw.textlength(dateline, font=dateline_font)) / 2, 94),
              dateline, font=dateline_font, fill=BLACK)
    draw.line([(28, 128), (SIZE - 28, 128)], fill=BLACK, width=3)
    draw.line([(28, 133), (SIZE - 28, 133)], fill=BLACK, width=1)

    # ---- six panels, two columns by three rows ----
    margin, gap = 28, 16
    panel_w = (SIZE - 2 * margin - gap) // 2
    top, bottom = 146, 1000
    panel_h = (bottom - top - 2 * gap) // 3
    for index, (headline, standfirst, picture) in enumerate(STORIES):
        col, row = index % 2, index // 2
        px0 = margin + col * (panel_w + gap)
        py0 = top + row * (panel_h + gap)
        px1, py1 = px0 + panel_w, py0 + panel_h
        draw.rectangle([px0, py0, px1, py1], outline=BLACK, width=2)
        pad = 14
        picture(draw, px0 + pad, py0 + 8, px1 - pad, py0 + 128)
        rule_y = py0 + 136
        draw.line([(px0 + pad, rule_y), (px1 - pad, rule_y)], fill=BLACK,
                  width=1)
        head_font, head_lines = shrink_to_fit(
            draw, headline, SERIF_BOLD, 30, px1 - px0 - 2 * pad, 2)
        text_y = rule_y + 10
        for line in head_lines:
            draw.text((px0 + pad, text_y), line, font=head_font, fill=BLACK)
            text_y += head_font.size + 3
        text_y += 5
        draw.line([(px0 + pad, text_y), (px1 - pad, text_y)], fill=BLACK,
                  width=1)
        text_y += 9
        body_font = load(SANS, 18)
        for line in split_text(draw, standfirst, body_font,
                               px1 - px0 - 2 * pad):
            draw.text((px0 + pad, text_y), line, font=body_font, fill=BLACK)
            text_y += 22

    canvas.save("entry.png", format="PNG")
    print("saved entry.png")


if __name__ == "__main__":
    build()
