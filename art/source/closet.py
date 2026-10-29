"""Supply Closet 13-B background, full screen 640x360 (classic SQ4/SQ5 drop-down menu, no bottom panel)."""
import sys
import numpy as np
from PIL import Image
from paint import Canvas, hexc, mix, to_256, FONT_B, FONT_C, FONT_M

W, H = 640, 360
c = Canvas(W, H, s=3, bg='#000000')
rng = np.random.default_rng(3)

VP = (320.0, 125.0)
BW_L, BW_R, BW_T, BW_B = 100.0, 540.0, 52.0, 186.0   # back wall


def ray(px, py, x):
    """Point on the line from the vanishing point through (px, py), at frame x."""
    t = (x - VP[0]) / (px - VP[0])
    return (x, VP[1] + (py - VP[1]) * t)


def ray_y(px, py, y):
    t = (y - VP[1]) / (py - VP[1])
    return (VP[0] + (px - VP[0]) * t, y)


def rwall(x, v):
    """Right wall: frame x, height fraction v (0 floor, 1 ceiling)."""
    yb = ray(BW_R, BW_B, x)[1]
    yt = ray(BW_R, BW_T, x)[1]
    return (x, yb + (yt - yb) * v)


def lwall(x, v):
    yb = ray(BW_L, BW_B, x)[1]
    yt = ray(BW_L, BW_T, x)[1]
    return (x, yb + (yt - yb) * v)


# ---------------------------------------------------------------- ceiling
ceil = [(0, 0), (W, 0), ray(BW_R, BW_T, W), (BW_R, BW_T), (BW_L, BW_T), ray(BW_L, BW_T, 0)]
c.paint(c.mpoly(ceil), c.vgrad('#8a9a94', '#b8c6bc', 0, BW_T))
# ceiling tile grid converging on the vanishing point
for i in range(0, 13):
    x = BW_L + (BW_R - BW_L) * i / 12
    c.paint(c.mline([(x, BW_T), ray_y(x, BW_T, -5)], 0.8), '#6f7d78', 0.8)
for y in (BW_T - 14, BW_T - 31):
    xl = ray_y(BW_L, BW_T, y)[0]
    xr = ray_y(BW_R, BW_T, y)[0]
    c.paint(c.mline([(xl, y), (xr, y)], 0.8), '#6f7d78', 0.8)
# the loose tile with the scratched combination (above the crate)
t0 = ray_y(BW_L + 36.7 * 1, BW_T, BW_T - 14)
tile = [ray_y(BW_L + 36.7, BW_T, BW_T - 14), ray_y(BW_L + 73.3, BW_T, BW_T - 14),
        ray_y(BW_L + 73.3, BW_T, BW_T - 31), ray_y(BW_L + 36.7, BW_T, BW_T - 31)]
tile_drop = [(tile[0][0] + 1, tile[0][1] + 4), (tile[1][0], tile[1][1] + 1), tile[2], (tile[3][0] - 1, tile[3][1] + 3)]
c.paint(c.mpoly(tile_drop), '#3a2f48')                        # dark gap behind it
c.paint(c.mpoly([(p[0], p[1]) for p in tile]), '#c9d3c8')
c.paint(c.mline([tile[0], tile[1]], 1.0), '#7d8a84')
cx_t = (tile[0][0] + tile[1][0] + tile[2][0] + tile[3][0]) / 4
cy_t = (tile[0][1] + tile[2][1]) / 2
c.paint(c.mtext((cx_t, cy_t), "4-8-15", 7.5, FONT_M, anchor='mm'), '#5c5068', 0.9)
for k in range(5):
    x0 = cx_t - 16 + rng.random() * 30
    c.paint(c.mline([(x0, cy_t - 5), (x0 + 3, cy_t + 4)], 0.4), '#8a7f94', 0.6)

# ceiling vent and a duct running toward the back
c.paint(c.mpoly([(420, 8), (480, 8), (474, 22), (426, 22)]), '#5c6a84')
for k in range(5):
    c.paint(c.mline([(428 + k * 1, 10 + k * 2.6), (472 - k * 1, 10 + k * 2.6)], 0.9), '#2a2630')
c.paint(c.mpoly([(150, 0), (176, 0), (196, BW_T - 6), (184, BW_T - 6)]), c.hgrad('#b8c7dc', '#55627c', 150, 196))
# hanging lamp cord
c.paint(c.mline([(320, 0), (320, 22)], 1.2), '#2c2433')

# ---------------------------------------------------------------- back wall
c.paint(c.mrect(BW_L, BW_T, BW_R, BW_B), c.vgrad('#a6d394', '#86b27a', BW_T, BW_B))
# pale grey panel band and panel seams (SQ6 DeepShip mint/grey)
c.paint(c.mrect(BW_L, BW_T, BW_R, BW_T + 12), c.vgrad('#c9cfca', '#aeb5b0', BW_T, BW_T + 12))
c.paint(c.mrect(BW_L, BW_T + 12, BW_R, BW_T + 13.2), '#5f7a5a')
for x in np.arange(BW_L + 55, BW_R, 55):
    c.paint(c.mrect(x - 0.6, BW_T + 13, x + 0.6, BW_B - 14), '#6b8a63', 0.9)
    c.paint(c.mrect(x + 0.6, BW_T + 13, x + 1.6, BW_B - 14), '#c3dcb3', 0.6)
# rivets
for x in np.arange(BW_L + 6, BW_R, 13.75):
    c.paint(c.mellipse(x, BW_T + 6, 0.9, 0.9), '#7d857f')
# purple accent stripe and steel baseboard
c.paint(c.mrect(BW_L, BW_B - 14, BW_R, BW_B - 10), c.vgrad('#8b5a9b', '#6b386b', BW_B - 14, BW_B - 10))
c.paint(c.mrect(BW_L, BW_B - 10, BW_R, BW_B), c.vgrad('#7f8ea6', '#56627a', BW_B - 10, BW_B))

# steel blue-grey pipes running along the top (SQ5 Eureka engineering)
for yy, r, col in ((BW_T + 17, 3.2, '#7b8faa'), (BW_T + 24, 2.2, '#6a7c96')):
    c.paint(c.mrect(BW_L, yy - r, BW_R, yy + r), c.vgrad('#b8c7dc', col, yy - r, yy + r))
    c.paint(c.mrect(BW_L, yy + r - 0.8, BW_R, yy + r), '#3e4660')
    for x in (150, 262, 395, 505):
        c.paint(c.mrect(x, yy - r - 0.8, x + 4, yy + r + 0.8), c.vgrad('#d3dbe6', '#5c6a84', yy - r, yy + r))
# vertical pipe down the left of the back wall with a valve
c.paint(c.mrect(108, BW_T + 17, 114, BW_B - 10), c.hgrad('#b8c7dc', '#55627c', 108, 114))
c.paint(c.mellipse(111, 120, 6, 2.2), '#a23a3a')
c.paint(c.mellipse(111, 119.4, 5, 1.4), '#d86050')

# ---------------------------------------------------------------- left wall
lw = [(0, ray(BW_L, BW_T, 0)[1]), (BW_L, BW_T), (BW_L, BW_B), (0, ray(BW_L, BW_B, 0)[1])]
c.paint(c.mpoly(lw), c.hgrad('#7d9a72', '#9ab88c', 0, BW_L))
# grey top band on the side wall
v_band = 1 - 12 / (BW_B - BW_T)
c.paint(c.mpoly([lwall(0, 1), lwall(BW_L, 1), lwall(BW_L, v_band), lwall(0, v_band)]), '#a9b0aa')
v_strip_t, v_strip_b = 14 / (BW_B - BW_T), 10 / (BW_B - BW_T)
c.paint(c.mpoly([lwall(0, v_strip_t), lwall(BW_L, v_strip_t), lwall(BW_L, v_strip_b), lwall(0, v_strip_b)]), '#6b386b')
c.paint(c.mpoly([lwall(0, v_strip_b), lwall(BW_L, v_strip_b), lwall(BW_L, 0), lwall(0, 0)]), '#56627a')
# intercom speaker on the left wall (Sterilis talks through it)
spk = [lwall(42, 0.78), lwall(72, 0.78), lwall(72, 0.56), lwall(42, 0.56)]
c.paint(c.mpoly(spk), '#4a494a')
spk_in = [lwall(45, 0.75), lwall(69, 0.75), lwall(69, 0.59), lwall(45, 0.59)]
c.paint(c.mpoly(spk_in), '#2a2630')
for i in range(6):
    v = 0.61 + i * 0.024
    c.paint(c.mline([lwall(46, v), lwall(68, v)], 0.7), '#6b6d6b')
c.glow(*lwall(66, 0.8), 3, 3, '#ff3020', 0.9)
c.paint(c.mellipse(*lwall(66, 0.8), 1.0, 1.0), '#ff6040')
# joke sign on the left wall
sg = [lwall(14, 0.52), lwall(40, 0.52), lwall(40, 0.36), lwall(14, 0.36)]
c.paint(c.mpoly(sg), '#e8e0c0')
sx, sy = lwall(27, 0.44)
c.paint(c.mtext((sx, sy), "WASH\nHANDS\nOR ELSE", 4.2, FONT_C, anchor='mm', spacing=-0.6), '#7a2020')

# ---------------------------------------------------------------- right wall
rw = [ray(BW_R, BW_T, W), (BW_R, BW_T), (BW_R, BW_B), ray(BW_R, BW_B, W)]
c.paint(c.mpoly(rw), c.hgrad('#93b186', '#6f8c66', BW_R, W))
c.paint(c.mpoly([rwall(BW_R, 1), rwall(W, 1), rwall(W, v_band), rwall(BW_R, v_band)]), '#9aa19c')
c.paint(c.mpoly([rwall(BW_R, v_strip_t), rwall(W, v_strip_t), rwall(W, v_strip_b), rwall(BW_R, v_strip_b)]), '#5a2f5a')
c.paint(c.mpoly([rwall(BW_R, v_strip_b), rwall(W, v_strip_b), rwall(W, 0), rwall(BW_R, 0)]), '#4d586e')

# sliding door 13-B on the right wall
DX0, DX1, DV = 558, 628, 0.86
frame = [rwall(DX0 - 5, DV + 0.05), rwall(DX1 + 5, DV + 0.05), rwall(DX1 + 5, 0), rwall(DX0 - 5, 0)]
c.paint(c.mpoly(frame), '#5c6a84')
door = [rwall(DX0, DV), rwall(DX1, DV), rwall(DX1, 0), rwall(DX0, 0)]
c.paint(c.mpoly(door), c.hgrad('#aab6c8', '#7a879e', DX0, DX1))
# split line of the sliding door
c.paint(c.mline([rwall((DX0 + DX1) / 2, DV), rwall((DX0 + DX1) / 2, 0)], 1.0), '#3e4660')
# hazard stripes at the bottom of the door
hz = [rwall(DX0, 0.1), rwall(DX1, 0.1), rwall(DX1, 0), rwall(DX0, 0)]
c.paint(c.mpoly(hz), '#e0a830')
for i in range(8):
    xa = DX0 + i * 9
    c.paint(c.mpoly([rwall(xa, 0.1), rwall(xa + 4.5, 0.1), rwall(xa + 1, 0), rwall(xa - 3.5, 0)]), '#2a2630')
# round porthole
pc = rwall(593, 0.62)
c.paint(c.mellipse(pc[0], pc[1], 13, 17), c.vgrad('#c8d2e0', '#5c6a84', pc[1] - 17, pc[1] + 17))
c.paint(c.mellipse(pc[0], pc[1], 9.5, 13), '#2a3550')
c.paint(c.mellipse(pc[0] - 1, pc[1] - 2, 8, 11), c.vgrad('#5a7fa8', '#1e2844', pc[1] - 12, pc[1] + 12))
c.paint(c.mline([(pc[0] - 5, pc[1] - 7), (pc[0] + 1, pc[1] - 10)], 1.2), '#d8f0ff', 0.7)
# 13-B stencil, sheared to sit on the wall
lab = rwall(593, 0.34)
c.paint(c.mtext(lab, "13-B", 10, FONT_C, anchor='mm'), '#2e3350', 0.9)
# door status light + keycard slot
kp = rwall(DX0 - 2.5, 0.48)
c.paint(c.mrect(kp[0] - 2.2, kp[1] - 6, kp[0] + 2.2, kp[1] + 6), '#2a2630')
c.paint(c.mrect(kp[0] - 1.2, kp[1] - 1, kp[0] + 1.2, kp[1] + 4), '#0e0e14')
c.paint(c.mellipse(kp[0], kp[1] - 3.6, 1.3, 1.3), '#ff2a1a')
c.glow(kp[0], kp[1] - 3.6, 10, 10, '#ff2010', 0.55)

# ---------------------------------------------------------------- floor
fl = [(BW_L, BW_B), (BW_R, BW_B), ray(BW_R, BW_B, W), (W, H), (0, H), ray(BW_L, BW_B, 0)]
c.paint(c.mpoly(fl), c.vgrad('#56627e', '#3e4660', BW_B, H))
# deck plates converging on the vanishing point
for i in range(-10, 23):
    x = BW_L + (BW_R - BW_L) * i / 12
    c.paint(c.mline([(x, BW_B), ray_y(x, BW_B, H + 5)], 0.7), '#3b4256', 0.9)
y = BW_B
step = 9.0
while y < H:
    y += step
    step *= 1.32
    xl = max(-50, ray_y(BW_L, BW_B, y)[0])
    xr = min(W + 50, ray_y(BW_R, BW_B, y)[0])
    c.paint(c.mline([(xl, y), (xr, y)], 0.8), '#3b4256', 0.9)
    c.paint(c.mline([(xl, y + 1), (xr, y + 1)], 0.5), '#7884a0', 0.4)
# floor drain
c.paint(c.mellipse(368, 300, 15, 5), '#2c2f3e')
for k in range(-3, 4):
    c.paint(c.mline([(368 + k * 4, 296.5), (368 + k * 4, 303.5)], 0.8), '#6a7590', 0.8)
# a puddle (the closet always has one)
c.paint(c.mellipse(250, 312, 30, 6), '#7f9cc4', 0.45)
c.paint(c.mellipse(244, 310, 10, 1.4), '#d8ecff', 0.5)

# ---------------------------------------------------------------- shelves (center-left)
def bgrad(col, x, bw):
    base = hexc(col)
    hi, lo = mix(base, np.ones(3, np.float32), 0.55), base * 0.55
    def f(X, Y):
        t = np.clip((X - x) / bw, 0, 1)[..., None]
        return np.where(t < 0.3, mix(hi, base, t / 0.3), mix(base, lo, (t - 0.3) / 0.7))
    return f

SX0, SX1, ST, SB = 196, 336, 70, 190
SD = 9   # shelf depth toward the viewer
for xs in (SX0, SX1):
    c.paint(c.mrect(xs - 2, ST, xs + 1.5, SB), c.hgrad('#c3cad6', '#5c6a84', xs - 2, xs + 1.5))
shelf_y = [98, 128, 158, 186]
bottle_cols = ['#e04848', '#3ca848', '#3c78d8', '#e8b830', '#c050c0', '#30b8b0', '#f08040', '#e8e8e8']
for j, yy in enumerate(shelf_y):
    # bottles standing on this shelf
    if j < 3:
        x = SX0 + 4
        while x < SX1 - 8:
            bw = 6 + rng.integers(0, 6)
            bh = 13 + rng.integers(0, 11)
            col = bottle_cols[rng.integers(0, len(bottle_cols))]
            kind = rng.integers(0, 3)
            top = yy - bh
            if kind == 0:   # jug with handle
                c.paint(c.mrect(x, top + 3, x + bw, yy), bgrad(col, x, bw))
                c.paint(c.mrect(x + bw * 0.25, top, x + bw * 0.6, top + 3.5), '#e8e8e8')
            elif kind == 1:  # spray bottle
                c.paint(c.mrect(x, top + 5, x + bw, yy), bgrad(col, x, bw))
                c.paint(c.mrect(x + bw * 0.3, top + 1, x + bw * 0.7, top + 5), '#404050')
                c.paint(c.mrect(x + bw * 0.1, top, x + bw * 0.7, top + 2), '#404050')
            else:           # round-shouldered bottle
                c.paint(c.mrect(x, top + 6, x + bw, yy), bgrad(col, x, bw))
                c.paint(c.mellipse(x + bw / 2, top + 6, bw / 2, 3), bgrad(col, x, bw))
                c.paint(c.mrect(x + bw * 0.35, top + 1, x + bw * 0.65, top + 4), '#f0f0f0')
            # label
            c.paint(c.mrect(x + 1, yy - bh * 0.55, x + bw - 1, yy - bh * 0.25), '#f4f0dc', 0.9)
            c.paint(c.mrect(x + 1.5, yy - bh * 0.45, x + bw - 1.5, yy - bh * 0.4), '#404050', 0.8)
            # contact shadow, purple-tinted
            c.darken(c.mrect(x - 1, yy - 2, x + bw + 2, yy), '#6040a0', 0.5)
            x += bw + 1 + rng.integers(0, 3)
    # the shelf plank itself, front edge
    c.paint(c.mpoly([(SX0 - 3, yy), (SX1 + 2, yy), (SX1 + 4, yy + 3), (SX0 - 5, yy + 3)]), c.vgrad('#d7dde6', '#7884a0', yy, yy + 3))
    c.paint(c.mrect(SX0 - 5, yy + 3, SX1 + 4, yy + 4.2), '#3b4256')
# "DO NOT DRINK (AGAIN)" shelf tag
c.paint(c.mrect(232, 158.5, 300, 165), '#f2e48a')
c.paint(c.mtext((266, 161.8), "DO NOT DRINK (AGAIN)", 4.6, FONT_C, anchor='mm'), '#7a2020')
# a stack of toilet paper on the bottom shelf
for k in range(3):
    for m in range(2):
        cx_, cy_ = 212 + k * 11, 181 - m * 9
        c.paint(c.mrect(cx_ - 5, cy_ - 4.5, cx_ + 5, cy_ + 4.5), c.hgrad('#ffffff', '#b8b8c8', cx_ - 5, cx_ + 5))
        c.paint(c.mellipse(cx_ + 5, cy_, 1.4, 4.5), '#d0d0dc')
# a box of "SPONGES - LIVE" on the bottom shelf
c.paint(c.mrect(260, 170, 300, 186), c.vgrad('#d9a466', '#a0703e', 170, 186))
c.paint(c.mtext((280, 178), "SPONGES\nLIVE", 4.4, FONT_C, anchor='mm', spacing=-0.5), '#4a2a18')
c.paint(c.mrect(306, 174, 330, 186), c.vgrad('#6a9ad8', '#3a5a98', 174, 186))


# ---------------------------------------------------------------- duty roster terminal (green glow, SQ6-style screen)
TX0, TY0, TX1, TY1 = 128, 92, 186, 136
c.paint(c.mrect(TX0 - 3, TY0 - 3, TX1 + 3, TY1 + 6), c.vgrad('#c3cad6', '#5c6a84', TY0 - 3, TY1 + 6))
c.paint(c.mrect(TX0, TY0, TX1, TY1), '#0a1a0c')
c.paint(c.mtext((TX0 + 3, TY0 + 3), "DUTY ROSTER\n WILCO\n WILCO\n WILCO\n(ALSO WILCO)", 5.4, FONT_M, anchor="la", spacing=0.6), "#29ff18", 1.0, layer=c.emit)
c.glow((TX0 + TX1) / 2, (TY0 + TY1) / 2, 60, 55, '#1d8a14', 0.35, 1.6)
for k in range(0, int(TY1 - TY0), 2):
    c.paint(c.mrect(TX0, TY0 + k, TX1, TY0 + k + 0.6), '#000000', 0.25)
c.paint(c.mellipse(TX1 - 4, TY1 + 3, 1.2, 1.2), '#29ff18', 1.0, layer=c.emit)

# ---------------------------------------------------------------- clutter: boxes stacked by the locker, hose on the wall
for (bx0, by0, bx1, by1, col) in ((346, 168, 392, 196, '#c49a62'), (352, 150, 386, 168, '#b48a56'), (396, 178, 428, 198, '#d0a870')):
    c.darken(c.mrect(bx0 + 2, by1 - 1, bx1 + 5, by1 + 2), '#402860', 0.6)
    c.paint(c.mrect(bx0, by0, bx1, by1), c.vgrad(col, '#7a5230', by0, by1 + 10))
    c.paint(c.mrect(bx0, by0 + (by1 - by0) / 2 - 1.2, bx1, by0 + (by1 - by0) / 2 + 1.2), '#e0d0a0', 0.7)
    c.paint(c.mline([(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1), (bx0, by0)], 0.8), '#4a2e18', 0.8)
c.paint(c.mtext((369, 186), "RAGS", 6, FONT_C, anchor='mm'), '#4a2e18', 0.8)
c.paint(c.mtext((412, 190), "MORE RAGS", 3.8, FONT_C, anchor='mm'), '#4a2e18', 0.8)
# coiled yellow hose hanging on the back wall, left of the locker
for k in range(4):
    c.paint(c.mellipse(436 - k * 0.6, 112 + k * 1.2, 9 - k * 0.3, 12 - k * 0.4).__sub__(c.mellipse(436 - k * 0.6, 112 + k * 1.2, 7 - k * 0.3, 10 - k * 0.4)).clip(0, 1), '#d8b030')
c.paint(c.mrect(433, 98, 439, 102), '#5c6a84')

# ---------------------------------------------------------------- poster
PX0, PY0, PX1, PY1 = 356, 72, 424, 150
c.darken(c.mrect(PX0 + 2, PY0 + 2, PX1 + 2, PY1 + 2), '#503070', 0.6)
c.paint(c.mrect(PX0, PY0, PX1, PY1), c.vgrad('#f4ecd0', '#ddd2b0', PY0, PY1))
c.paint(c.mrect(PX0 + 3, PY0 + 3, PX1 - 3, PY0 + 22), '#283c8c')
c.paint(c.mtext(((PX0 + PX1) / 2, PY0 + 12.5), "EMPLOYEE\nOF THE MONTH", 6.6, FONT_C, anchor='mm', spacing=-0.8), '#f4ecd0')
# empty photo frame
c.paint(c.mrect(PX0 + 14, PY0 + 26, PX1 - 14, PY0 + 60), '#b89850')
c.paint(c.mrect(PX0 + 16.5, PY0 + 28.5, PX1 - 16.5, PY0 + 57.5), c.vgrad('#7a8aa8', '#4a5470', PY0 + 28, PY0 + 58))
c.paint(c.mtext(((PX0 + PX1) / 2, PY0 + 43), "?", 18, FONT_B, anchor='mm'), '#c8d0e0', 0.8)
c.paint(c.mtext(((PX0 + PX1) / 2, PY1 - 9), "(NEVER)", 8.5, FONT_C, anchor='mm'), '#c02020')
# tape at the corners
for (tx, ty) in ((PX0 + 2, PY0 + 1), (PX1 - 2, PY0 + 1)):
    c.paint(c.mrect(tx - 4, ty - 1.5, tx + 4, ty + 2), '#f8f4c8', 0.8)

# ---------------------------------------------------------------- locker (right of back wall)
LX0, LX1, LT, LB = 448, 524, 62, 196
LD = 10
# side face toward the vanishing point
c.paint(c.mpoly([(LX0, LT + 3), (LX0 + 0.1, LT), (LX0 - LD * 0.45, LT - 3), (LX0 - LD * 0.45, LB - 2), (LX0, LB)]), '#5c6372')
c.paint(c.mrect(LX0, LT, LX1, LB), c.hgrad('#b8bdc8', '#8a909e', LX0, LX1))
c.paint(c.mrect(LX0, LT, LX1, LT + 3), '#d6dae2')
c.paint(c.mline([((LX0 + LX1) / 2, LT + 3), ((LX0 + LX1) / 2, LB)], 1.0), '#4a5060')
for half in (0, 1):
    hx = LX0 + 6 + half * 38
    for k in range(5):
        c.paint(c.mrect(hx, LT + 10 + k * 3.4, hx + 26, LT + 11.4 + k * 3.4), '#4a5060')
# combination dial on the right half
c.paint(c.mellipse(494, 128, 5, 5), c.vgrad('#e8ecf2', '#6a7080', 123, 133))
c.paint(c.mellipse(494, 128, 2.2, 2.2), '#2a2630')
c.paint(c.mrect(493.6, 123, 494.4, 125.4), '#c02020')
c.paint(c.mrect(491, 140, 497, 152), '#5a6070')   # handle
c.paint(c.mtext((505, 172), "WILCO", 9, FONT_C, anchor='mm'), '#2a2e3e', 0.85)
# a dent and a sticker
c.paint(c.mellipse(466, 160, 5, 3), '#7a8090', 0.6)
c.paint(c.mrect(458, 104, 476, 114), '#e04848')
c.paint(c.mtext((467, 109), "NO\nNAPS", 3.6, FONT_C, anchor='mm', spacing=-0.6), '#ffffff')

# ---------------------------------------------------------------- crate (left, Roger's nap spot)
CX0, CX1, CT, CB = 34, 176, 226, 290
CDX, CDY = 26, -14       # top/side receding up-right
# shadow under the crate
c.darken(c.mpoly([(CX0 - 4, CB + 2), (CX1 + 10, CB + 2), (CX1 + CDX + 6, CB + CDY), (CX0 + CDX, CB + CDY)]), '#402860', 0.7)
# side face
c.paint(c.mpoly([(CX1, CT), (CX1 + CDX, CT + CDY), (CX1 + CDX, CB + CDY), (CX1, CB)]), c.vgrad('#6a4224', '#3e2416', CT, CB))
# top face
c.paint(c.mpoly([(CX0, CT), (CX1, CT), (CX1 + CDX, CT + CDY), (CX0 + CDX, CT + CDY)]), c.vgrad('#b88a58', '#c89a64', CT + CDY, CT))
for k in range(1, 5):
    t = k / 5
    c.paint(c.mline([(CX0 + CDX * t, CT + CDY * t), (CX1 + CDX * t, CT + CDY * t)], 0.6), '#7a4e2a', 0.8)
# front face planks
c.paint(c.mrect(CX0, CT, CX1, CB), c.vgrad('#b07a46', '#8a5a32', CT, CB))
for k in range(1, 4):
    yy = CT + (CB - CT) * k / 4
    c.paint(c.mrect(CX0, yy - 0.5, CX1, yy + 0.5), '#5e3a20')
# cross braces and frame
for a, b in (((CX0 + 4, CT + 4), (CX1 - 4, CB - 4)), ((CX0 + 4, CB - 4), (CX1 - 4, CT + 4))):
    c.paint(c.mline([a, b], 6), '#9a6a3c')
    c.paint(c.mline([a, b], 1.0), '#6a4224', 0.6)
for r in ((CX0, CT, CX0 + 6, CB), (CX1 - 6, CT, CX1, CB), (CX0, CT, CX1, CT + 5), (CX0, CB - 5, CX1, CB)):
    c.paint(c.mrect(*r), c.vgrad('#c48c54', '#93603a', r[1], r[3]))
c.paint(c.mrect((CX0 + CX1) / 2 - 30, CT + 25, (CX0 + CX1) / 2 + 30, CT + 37), '#a87442')
_m = c.mtext(((CX0 + CX1) / 2, CT + 31), "THIS SIDE UP", 7.5, FONT_C, anchor='mm')
_ys, _xs = np.nonzero(_m > 0)
_y0, _y1, _x0, _x1 = _ys.min(), _ys.max() + 1, _xs.min(), _xs.max() + 1
_m[_y0:_y1, _x0:_x1] = _m[_y0:_y1, _x0:_x1][::-1, ::-1].copy()   # stencilled upside down
c.paint(_m, '#3a2414', 0.75)
# rolled-up towel pillow and the drool stain
c.paint(c.mellipse(CX0 + 30, CT - 4, 16, 4.5), c.vgrad('#c8a0d8', '#8a5a9a', CT - 9, CT))
c.paint(c.mellipse(CX0 + 30, CT - 5.5, 13, 2), '#e0c4ec', 0.7)
c.paint(c.mellipse(CX0 + 58, CT - 4, 11, 3), '#7a5a3a', 0.55)
c.paint(c.mellipse(CX0 + 56, CT - 4.6, 4, 0.9), '#f0f6ff', 0.6)

# ---------------------------------------------------------------- foreground: cropped barrel bottom-right
BXc, BYt = 622, 262
c.paint(c.mrect(BXc - 30, BYt, W + 5, H + 5), c.hgrad('#5a78b8', '#28386a', BXc - 30, W))
c.paint(c.mellipse(BXc + 6, BYt, 36, 7), c.vgrad('#8aa0d0', '#4a5c98', BYt - 7, BYt + 7))
c.paint(c.mellipse(BXc + 6, BYt, 30, 5), '#30406e')
for yy in (285, 314):
    c.paint(c.mrect(BXc - 30, yy, W + 5, yy + 3), '#2a3458')
c.paint(c.mrect(BXc - 26, 291, W + 5, 308), '#e8e0c0')
c.paint(c.mtext((BXc - 24, 299.5), "INDUSTRIAL\nSOLVENT", 5.2, FONT_C, anchor='lm', spacing=-0.7), '#7a2020')

# ---------------------------------------------------------------- crisp dark edges (SQ6 objects read against the wall)
EDGE = '#2a2236'
c.paint(c.mline([(LX0, LT), (LX1, LT), (LX1, LB), (LX0, LB), (LX0, LT)], 1.0), EDGE, 0.85)
c.paint(c.mline([(LX0 - LD * 0.45, LT - 3), (LX0 - LD * 0.45, LB - 2), (LX0, LB)], 1.0), EDGE, 0.85)
c.paint(c.mline([(CX0, CT), (CX1, CT), (CX1, CB), (CX0, CB), (CX0, CT)], 1.0), EDGE, 0.85)
c.paint(c.mline([(CX0, CT), (CX0 + CDX, CT + CDY), (CX1 + CDX, CT + CDY), (CX1 + CDX, CB + CDY), (CX1, CB)], 1.0), EDGE, 0.85)
c.paint(c.mline([(CX1, CT), (CX1 + CDX, CT + CDY)], 1.0), EDGE, 0.85)
c.paint(c.mline(frame + [frame[0]], 1.0), EDGE, 0.85)
c.paint(c.mline([(PX0, PY0), (PX1, PY0), (PX1, PY1), (PX0, PY1), (PX0, PY0)], 0.8), EDGE, 0.7)
# lamp reflection and grime on the floor
for k in range(14):
    gx, gy = 40 + rng.random() * 560, 200 + rng.random() * 125
    c.paint(c.mellipse(gx, gy, 6 + rng.random() * 14, 1.5 + rng.random() * 3), '#2e2a3e', 0.18)

# ---------------------------------------------------------------- lamp (drawn last so it hangs in front)
c.paint(c.mpoly([(306, 32), (334, 32), (328, 22), (312, 22)]), c.hgrad('#e8b860', '#8a5a20', 306, 334))
c.paint(c.mellipse(320, 32, 14, 2.5), '#ffe8a0')
c.glow(320, 34, 9, 6, '#fff2c0', 1.0, 1.0)

# ---------------------------------------------------------------- lighting
X, Y = c.X, c.Y
amb = hexc('#cbbede')   # purple-tinted ambient (shadows never neutral black)
warm = hexc('#ffd890')
L = np.ones_like(c.img) * amb
# cone of amber light from the lamp down to the floor
cone = np.clip(1 - np.abs(X - 320) / (20 + (Y - 32) * 0.95), 0, 1) * (Y > 30)
pool = np.clip(1 - np.sqrt(((X - 312) / 175) ** 2 + ((Y - 262) / 62) ** 2), 0, 1)
wall = np.clip(1 - np.sqrt(((X - 320) / 160) ** 2 + ((Y - 70) / 110) ** 2), 0, 1)
L = L + warm * (0.55 * cone ** 1.2 + 0.55 * pool ** 1.1 + 0.35 * wall ** 1.5)[..., None]
# soft beam inside the cone
c.emit += (hexc('#ffd890') * 0.07 * (cone ** 2))[..., None].squeeze(-1) if False else (cone ** 2)[..., None] * hexc('#ffd890') * 0.07

img = c.finish(light=L, grain=0.0, vignette=0.4)
img.save('closet_raw.png')
q = to_256(img, noise=9)
q.save('supply_closet_bg.png')
q.resize((W * 2, H * 2), Image.NEAREST).save('supply_closet_bg_2x.png')
print('ok')
