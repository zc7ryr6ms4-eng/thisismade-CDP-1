"""Gerätefront im Klemmbaustein-Stil: weiße Steine, rote Anzeigen und Akzente.

Gleiches Layout und gleiche Klickflächen wie face.py – nur anders gezeichnet.
"""
import math

import cairo

from .face import (CANVAS_H, CANVAS_W, DEV_H, DEV_W, DISC_C, DISC_R, DISPLAY, ENTER, FADER_X,  # noqa: F401
                   FADER_Y0, FADER_Y1, HUB_R, JOG_TRAVEL, KEY_H, KEY_W, KEYS, KNOB_C, KNOB_R, MARGIN_BOTTOM,
                   MARGIN_TOP, MARGIN_X, MEM, MEM_H, MEM_W, MEM_Y, SHUTTLE, SMALL, SMALL_H, SMALL_W, SMALL_Y,
                   TOP_BTNS, TOP_H, TOP_W, TOP_Y, TR_H, TR_Y, TRANSPORT, WELL_R, _circle, _display, _icon,
                   _rgb, _rrect, _text, hit)

NAME = "brick"

# Farbpalette (klassische Spielzeugstein-Farben)
RED = (0.79, 0.10, 0.10)
YELLOW = (0.98, 0.79, 0.05)
BLUE = (0.00, 0.33, 0.75)
GREEN = (0.00, 0.57, 0.26)
ORANGE = (1.00, 0.50, 0.00)
WHITE = (0.965, 0.965, 0.955)
BASE = (0.93, 0.93, 0.92)          # Grundplatte
WELL = (0.84, 0.84, 0.85)          # runde Platte unter der Disc
LABEL = (0.86, 0.86, 0.87)         # Beschriftungsfliesen
BLACK = (0.13, 0.13, 0.14)
DARK_GREY = (0.39, 0.40, 0.42)
LIGHT_GREY = (0.63, 0.65, 0.68)
TAN = (0.89, 0.80, 0.62)

PITCH = 30          # Noppenraster
STUD_R = 9.0
SIDE = 7.0          # sichtbare Steinflanke


def _shade(c, f):
    return tuple(max(0.0, min(1.0, v * f)) for v in c)


def _lighten(c, a):
    return tuple(min(1.0, v + (1 - v) * a) for v in c)


def _ink(c):
    """Lesbare Schriftfarbe auf Farbe c."""
    return BLACK if (0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]) > 0.55 else WHITE


# ----------------------------------------------------------------- Grundformen
def stud(cr, cx, cy, color, r=STUD_R, flat=False):
    """Eine Noppe: Schatten, Zylinderflanke, Deckel mit Glanzlicht."""
    h = 0 if flat else 4.5
    _circle(cr, cx + 1.5, cy + h + 2, r)
    _rgb(cr, (0, 0, 0), 0.22)
    cr.fill()
    if h:
        cr.rectangle(cx - r, cy, 2 * r, h)
        _circle(cr, cx, cy + h, r)
        _rgb(cr, _shade(color, 0.72))
        cr.fill()
    _circle(cr, cx, cy, r)
    g = cairo.LinearGradient(cx - r, cy - r, cx + r, cy + r)
    g.add_color_stop_rgb(0, *_lighten(color, 0.35))
    g.add_color_stop_rgb(0.55, *color)
    g.add_color_stop_rgb(1, *_shade(color, 0.85))
    cr.set_source(g)
    cr.fill()
    _circle(cr, cx - r * 0.35, cy - r * 0.35, r * 0.28)
    _rgb(cr, (1, 1, 1), 0.35)
    cr.fill()


def _studs_in(cr, x, y, w, h, color, r=STUD_R, pitch=PITCH):
    nx = max(1, int(w // pitch))
    ny = max(1, int(h // pitch))
    ox = x + (w - (nx - 1) * pitch) / 2
    oy = y + (h - (ny - 1) * pitch) / 2 - 2
    for j in range(ny):
        for i in range(nx):
            stud(cr, ox + i * pitch, oy + j * pitch, color, r)


def block(cr, x, y, w, h, color, pressed=False, r=4, studs=False, stud_r=STUD_R, side=SIDE):
    """Ein Stein (mit Noppen) oder eine Fliese (glatt) in Draufsicht mit Flanke unten."""
    oy = side * 0.6 if pressed else 0.0
    s = side - oy
    _rrect(cr, x + 2, y + s + 3, w, h, r)
    _rgb(cr, (0, 0, 0), 0.28)
    cr.fill()
    _rrect(cr, x, y + oy, w, h + s, r)
    _rgb(cr, _shade(color, 0.68))
    cr.fill()
    _rrect(cr, x, y + oy, w, h, r)
    g = cairo.LinearGradient(0, y + oy, 0, y + oy + h)
    g.add_color_stop_rgb(0, *_lighten(color, 0.10))
    g.add_color_stop_rgb(1, *color)
    cr.set_source(g)
    cr.fill()
    cr.rectangle(x + r, y + oy + 1, w - 2 * r, 1.4)
    _rgb(cr, (1, 1, 1), 0.35)
    cr.fill()
    if studs:
        _studs_in(cr, x, y + oy, w, h, color, stud_r)
    return oy


def round_tile(cr, cx, cy, r, color, pressed=False):
    oy = 3.0 if pressed else 0.0
    s = 6 - oy
    _circle(cr, cx + 2, cy + s + 3, r)
    _rgb(cr, (0, 0, 0), 0.28)
    cr.fill()
    cr.rectangle(cx - r, cy + oy, 2 * r, s)
    _circle(cr, cx, cy + oy + s, r)
    _rgb(cr, _shade(color, 0.68))
    cr.fill()
    _circle(cr, cx, cy + oy, r)
    g = cairo.LinearGradient(cx - r, cy - r, cx + r, cy + r)
    g.add_color_stop_rgb(0, *_lighten(color, 0.25))
    g.add_color_stop_rgb(1, *_shade(color, 0.9))
    cr.set_source(g)
    cr.fill()
    return oy


def trans_led(cr, cx, cy, on, color=(1.0, 0.15, 0.10), r=6):
    """Durchsichtige runde 1x1-Platte als Leuchte."""
    _circle(cr, cx + 1, cy + 2, r)
    _rgb(cr, (0, 0, 0), 0.25)
    cr.fill()
    _circle(cr, cx, cy, r)
    if on:
        g = cairo.RadialGradient(cx - r * 0.3, cy - r * 0.3, 0.5, cx, cy, r)
        g.add_color_stop_rgb(0, *_lighten(color, 0.7))
        g.add_color_stop_rgb(1, *color)
        cr.set_source(g)
    else:
        _rgb(cr, _shade(color, 0.45), 0.75)
    cr.fill()
    _circle(cr, cx - r * 0.35, cy - r * 0.35, r * 0.3)
    _rgb(cr, (1, 1, 1), 0.5)
    cr.fill()


# ----------------------------------------------------------------- Gesamtbild
def draw(cr, st):
    draw_static(cr)
    draw_dynamic(cr, st)


def draw_static(cr):
    # Grundplatte
    _rrect(cr, 3, 12, DEV_W, DEV_H, 10)
    _rgb(cr, (0, 0, 0), 0.30)
    cr.fill()
    _rrect(cr, 0, 0, DEV_W, DEV_H + 8, 10)
    _rgb(cr, _shade(BASE, 0.78))
    cr.fill()
    _rrect(cr, 0, 0, DEV_W, DEV_H, 10)
    _rgb(cr, BASE)
    cr.fill()
    for j in range(int(DEV_H // PITCH)):
        for i in range(int(DEV_W // PITCH)):
            cx, cy = PITCH / 2 + i * PITCH, PITCH / 2 + j * PITCH
            if (cx - DISC_C[0]) ** 2 + (cy - DISC_C[1]) ** 2 < (WELL_R + 8) ** 2:
                continue
            stud(cr, cx, cy, BASE, 8.0)

    # Namensschild
    block(cr, 26, 14, 330, 44, WHITE)
    _text(cr, "thisismade", 44, 45, 25, BLACK, align="left", bold=True)
    _text(cr, "CD PLAYER · CDP-01", 196, 44, 13, DARK_GREY, align="left", bold=True)

    # runde Grundplatte für die Disc
    cx, cy = DISC_C
    _circle(cr, cx + 3, cy + 10, WELL_R)
    _rgb(cr, (0, 0, 0), 0.30)
    cr.fill()
    _circle(cr, cx, cy + 7, WELL_R)
    _rgb(cr, _shade(WELL, 0.75))
    cr.fill()
    _circle(cr, cx, cy, WELL_R)
    _rgb(cr, WELL)
    cr.fill()
    n = 40
    for i in range(n):
        a = 2 * math.pi * i / n
        stud(cr, cx + math.cos(a) * (WELL_R - 12), cy + math.sin(a) * (WELL_R - 12), WELL, 7.0)

    # Display-Rahmen (schwarzer Stein mit Noppenreihe)
    x, y, w, h = DISPLAY
    block(cr, x - 10, y - 34, w + 20, h + 44, BLACK, r=5)
    for i in range(int((w + 20) // PITCH)):
        stud(cr, x - 10 + PITCH / 2 + i * PITCH + 3, y - 19, BLACK, 8)
    _rrect(cr, x, y, w, h, 4)
    g = cairo.LinearGradient(0, y, 0, y + h)
    g.add_color_stop_rgb(0, 0.05, 0.02, 0.02)
    g.add_color_stop_rgb(1, 0.08, 0.03, 0.03)
    cr.set_source(g)
    cr.fill()

    # Beschriftungsfliesen
    for t, tx, ty, tw in (("VOLUME", KNOB_C[0] - 40, KNOB_C[1] + KNOB_R + 12, 80),
                          ("MEMORY", 630, MEM_Y - 28, 90), ("SHUTTLE", SHUTTLE[0], MEM_Y - 28, 90),
                          ("TEMPO", FADER_X - 40, FADER_Y0 - 38, 80)):
        block(cr, tx, ty, tw, 20, LABEL, r=3, side=4)
        _text(cr, t, tx + tw / 2, ty + 15, 11, DARK_GREY, bold=True)


def draw_dynamic(cr, st):
    P = st.pressed
    on = st.power_on

    # Tasten oben (schwarze Fliesen, Power rot)
    for rid, t, x in TOP_BTNS:
        col = RED if rid == "power" else WHITE
        oy = block(cr, x, TOP_Y, TOP_W, TOP_H, col, rid in P, r=3, side=5)
        _text(cr, t, x + TOP_W / 2, TOP_Y + oy + 17, 10, _ink(col), bold=True)
    trans_led(cr, 1146, 31, st.bt_led and on, (0.2, 0.55, 1.0), 5)

    # Disc
    if st.disc_loaded:
        _disc(cr, st)
    else:
        cr.save()
        cr.translate(*DISC_C)
        cr.rotate(st.disc_angle)
        _hub(cr)
        cr.restore()
        _text(cr, "NO DISC", DISC_C[0], DISC_C[1] + 82, 15, BLACK, bold=True)
        _text(cr, "OPEN = Ordner · FILES = Dateien · oder hierher ziehen",
              DISC_C[0], DISC_C[1] + 104, 11, DARK_GREY)

    # Display-Inhalt (gleiche Anzeige wie klassisch)
    _display(cr, st)

    # Ziffernblock: runde Fliesen
    for lab, x, y in KEYS:
        kid = "key_" + lab
        col = WHITE
        r = min(KEY_W, KEY_H) / 2
        cx, cy = x + KEY_W / 2, y + KEY_H / 2 - 2
        oy = round_tile(cr, cx, cy, r, col, kid in P)
        text = {"T": "TIME", "C": "CLR"}.get(lab, lab)
        _text(cr, text, cx, cy + oy + (7 if len(text) == 1 else 4), 20 if len(text) == 1 else 11,
              RED if lab in "TC" else BLACK, bold=True)
    x, y, w, h = ENTER
    oy = block(cr, x, y, w, h - 6, RED, "enter" in P, studs=False)
    stud(cr, x + w / 2 - 15, y + oy + 18, RED, 8)
    stud(cr, x + w / 2 + 15, y + oy + 18, RED, 8)
    _text(cr, "ENTER", x + w / 2, y + oy + 64, 13, WHITE, bold=True)

    # Lautstärke: runde blaue Platte mit Noppen, dreht sich mit dem Wert
    _knob(cr, st.level_norm)

    # Memory A/B/C: orange Steine mit Leuchte
    for i, (rid, t, x) in enumerate(MEM):
        oy = block(cr, x, MEM_Y, MEM_W, MEM_H - 4, WHITE, rid in P)
        _text(cr, t, x + 26, MEM_Y + oy + 29, 22, BLACK, bold=True)
        trans_led(cr, x + MEM_W - 16, MEM_Y + oy + 19, st.cue_set[i] and on)

    # Shuttle: Schiene + gelber 1x2-Stein
    x, y, w, h = SHUTTLE
    block(cr, x, y + 12, w, h - 24, LIGHT_GREY, r=3, side=3)
    _text(cr, "REW", x + 16, y + h + 14, 10, BLACK, bold=True)
    _text(cr, "FF", x + w - 12, y + h + 14, 10, BLACK, bold=True)
    jx = x + w / 2 + st.jog * JOG_TRAVEL
    block(cr, jx - 26, y, 52, h - 6, RED, "jog" in P, r=3, studs=False)
    stud(cr, jx - 12, y + 17, RED, 8)
    stud(cr, jx + 12, y + 17, RED, 8)

    # Tempo-Fader: Schiene + roter 1x2-Stein
    _fader(cr, st.varispeed_norm)

    # Laufwerkstasten: große Steine mit aufgedrucktem Symbol
    colors = {"prev": WHITE, "next": WHITE, "stop": WHITE, "play": RED}
    for rid, x, w in TRANSPORT:
        col = colors[rid]
        oy = block(cr, x, TR_Y, w, TR_H - 6, col, rid in P)
        for k in range(int(w // PITCH)):
            stud(cr, x + (w - (int(w // PITCH) - 1) * PITCH) / 2 + k * PITCH, TR_Y + oy + 16, col, 8)
        _rrect(cr, x + 12, TR_Y + oy + 32, w - 24, 34, 3)
        _rgb(cr, LABEL if col == WHITE else WHITE)
        cr.fill()
        _icon(cr, rid, x + w / 2, TR_Y + oy + 49, RED if col == WHITE else BLACK)

    # kleine Tasten: weiße Fliesen mit Leuchte
    leds = {"vs_display": st.stretch, "repeat": st.repeat > 0, "shuffle": st.shuffle, "eject": None}
    for rid, t, x in SMALL:
        oy = block(cr, x, SMALL_Y, SMALL_W, SMALL_H - 4, WHITE, rid in P, r=3, side=5)
        _text(cr, t, x + (SMALL_W - 14) / 2, SMALL_Y + oy + 20, 10, BLACK, bold=True)
        if leds[rid] is not None:
            trans_led(cr, x + SMALL_W - 13, SMALL_Y + oy + 15, leds[rid] and on, r=5)

    if not on:
        _rrect(cr, 0, 0, DEV_W, DEV_H, 10)
        _rgb(cr, (0, 0, 0), 0.18)
        cr.fill()


def _hub(cr):
    """Runder 2x2-Stein als Spindel."""
    _circle(cr, 2, 8, 44)
    _rgb(cr, (0, 0, 0), 0.3)
    cr.fill()
    _circle(cr, 0, 6, 44)
    _rgb(cr, _shade(RED, 0.7))
    cr.fill()
    _circle(cr, 0, 0, 44)
    _rgb(cr, RED)
    cr.fill()
    for dx, dy in ((-14, -14), (14, -14), (-14, 14), (14, 14)):
        stud(cr, dx, dy, RED, 9)


def _disc(cr, st):
    cx, cy = DISC_C
    _circle(cr, cx + 3, cy + 12, DISC_R)
    _rgb(cr, (0, 0, 0), 0.35)
    cr.fill()
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(st.disc_angle)
    col = WHITE
    # Flanke der runden Platte
    _circle(cr, 0, 7, DISC_R)
    _rgb(cr, _shade(col, 0.65))
    cr.fill()
    _circle(cr, 0, 0, DISC_R)
    _rgb(cr, col)
    cr.fill()
    cover = getattr(st, "cover", None)
    inner = DISC_R - 40
    if cover is not None:
        cr.save()
        _circle(cr, 0, 0, inner)
        cr.clip()
        cw, ch = cover.get_width(), cover.get_height()
        s = 2 * inner / min(cw, ch)
        cr.scale(s, s)
        cr.set_source_surface(cover, -cw / 2, -ch / 2)
        cr.paint()
        cr.restore()
    else:
        ink = _ink(col)
        lines = st.disc_lines or []
        if lines:
            _text(cr, lines[0][:20], 0, -118, 22, ink, bold=True)
        for i, ln in enumerate(lines[1:5]):
            _text(cr, ln[:28], 0, -92 + i * 16, 12, ink, bold=True)
        _text(cr, "thisismade", 0, 140, 18, ink, bold=True)
    # Noppenring am Rand
    n = 30
    for i in range(n):
        a = 2 * math.pi * i / n
        stud(cr, math.cos(a) * (DISC_R - 20), math.sin(a) * (DISC_R - 20), col, 9)
    _hub(cr)
    cr.restore()


def _knob(cr, value):
    cx, cy = KNOB_C
    a = math.radians(225 - 270 * max(0.0, min(1.0, value)))
    # Skala aus kleinen Fliesen
    for i in range(11):
        t = math.radians(225 - 27 * i)
        px, py = cx + math.cos(t) * (KNOB_R + 12), cy - math.sin(t) * (KNOB_R + 12)
        _circle(cr, px, py, 3)
        _rgb(cr, RED if i * 0.1 <= value + 1e-6 else LIGHT_GREY)
        cr.fill()
    round_tile(cr, cx, cy, KNOB_R, WHITE)
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(-a + math.pi / 2)
    for dx, dy in ((-15, -15), (15, -15), (-15, 15), (15, 15)):
        stud(cr, dx, dy, WHITE, 8)
    _rrect(cr, -4, -KNOB_R + 4, 8, 18, 2)
    _rgb(cr, RED)
    cr.fill()
    cr.restore()


def _fader(cr, value):
    x = FADER_X
    for i in range(9):
        y = FADER_Y1 - i * (FADER_Y1 - FADER_Y0) / 8
        cr.rectangle(x - 34, y - 1, 14 if i != 4 else 18, 2)
        _rgb(cr, RED if i == 4 else LIGHT_GREY)
        cr.fill()
    block(cr, x - 6, FADER_Y0 - 10, 12, FADER_Y1 - FADER_Y0 + 20, LIGHT_GREY, r=3, side=3)
    cy = FADER_Y1 - max(0.0, min(1.0, value)) * (FADER_Y1 - FADER_Y0)
    block(cr, x - 26, cy - 15, 52, 26, RED, r=3, side=5)
    stud(cr, x - 12, cy - 3, RED, 8)
    stud(cr, x + 12, cy - 3, RED, 8)
