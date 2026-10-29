"""Roger Wilco sprite, SQ6 style: white/purple janitor suit (SQ4 manual art + SQ6 sprite), 1px outline, 3 flat shades."""
import numpy as np
from PIL import Image
from paint import Canvas, hexc

PAL = {
    'skin':   ('#f2c4a8', '#dea28c', '#b47868'),
    'hair':   ('#fae48c', '#e8c860', '#b48c38'),
    'tunic':  ('#f2f0f2', '#d6d3d6', '#a8a6a8'),
    'gold':   ('#f6cc58', '#e0a830', '#a87420'),
    'sleeve': ('#cab8dc', '#ad9abd', '#86699e'),
    'cuff':   ('#8a5a8e', '#6b386b', '#4a2050'),
    'emblem': ('#3c56b4', '#283c8c', '#1a2866'),
    'belt':   ('#4a3a4a', '#312031', '#221624'),
    'buckle': ('#eef0f6', '#c0c4d0', '#8a90a0'),
    'pants':  ('#8c8e8c', '#6b6d6b', '#4c4e4c'),
    'boot':   ('#605f60', '#4a494a', '#2e2d2e'),
}
OUTLINE = hexc('#1c1222')
ORDER = list(PAL)           # paint order = later wins


def build(parts, w, h, light_dir=-1, s=4, shade_rule=None):
    """parts: list of (material, maskfn(canvas)) painted in order. Returns RGBA image."""
    c = Canvas(w, h, s=s)
    mat = np.full((h, w), -1, np.int32)
    part_id = np.full((h, w), -1, np.int32)
    cover_any = np.zeros((h, w), np.float32)
    for i, (m, fn) in enumerate(parts):
        hi = fn(c)
        lo = hi.reshape(h, s, w, s).mean(axis=(1, 3))
        on = lo >= 0.5
        mat[on] = ORDER.index(m)
        part_id[on] = i
        cover_any = np.maximum(cover_any, lo)
    rgba = np.zeros((h, w, 4), np.float32)
    # per-part horizontal shading: lit side / mid / shadow side
    for i, (m, fn) in enumerate(parts):
        ys, xs = np.nonzero(part_id == i)
        if len(xs) == 0:
            continue
        pal = [hexc(x) for x in PAL[m]]
        for y in np.unique(ys):
            row = xs[ys == y]
            x0, x1 = row.min(), row.max()
            span = max(1, x1 - x0)
            for x in row:
                t = (x - x0) / span
                if light_dir > 0:
                    t = 1 - t
                if shade_rule and shade_rule(m, i, x, y) is not None:
                    k = shade_rule(m, i, x, y)
                elif span >= 3 and t < 0.22:
                    k = 0
                elif span >= 2 and t > 0.68:
                    k = 2
                else:
                    k = 1
                rgba[y, x, :3] = pal[k]
                rgba[y, x, 3] = 1
    return rgba, mat, part_id


def outline(rgba, part_id, mat, inner_pairs=()):
    h, w = part_id.shape
    out = rgba.copy()
    filled = rgba[..., 3] > 0
    # exterior outline (1px, all 8 neighbours so corners close)
    pad = np.pad(filled, 1)
    near = np.zeros_like(filled)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            near |= pad[1 + dy:h + 1 + dy, 1 + dx:w + 1 + dx]
    ext = near & ~filled
    out[ext, :3] = OUTLINE
    out[ext, 3] = 1
    # interior lines where an arm/front part overlaps a body part behind it
    names = [ORDER[m] if m >= 0 else None for m in range(len(ORDER))]
    for y in range(h):
        for x in range(w):
            a = mat[y, x]
            if a < 0:
                continue
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < h and 0 <= xx < w and mat[yy, xx] >= 0 and part_id[yy, xx] != part_id[y, x]:
                    pa, pb = ORDER[a], ORDER[mat[yy, xx]]
                    if (pa, pb) in inner_pairs:
                        out[y, x, :3] = OUTLINE * 0.6 + rgba[y, x, :3] * 0.4
    return out


def save(rgba, path, scale=1):
    im = Image.fromarray((np.clip(rgba, 0, 1) * 255).astype(np.uint8), 'RGBA')
    if scale != 1:
        im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    im.save(path)
    return im


def px(rgba, pts, color):
    col = hexc(color)
    for x, y in pts:
        rgba[y, x, :3] = col
        rgba[y, x, 3] = 1


# =============================================================== FRONT VIEW
def front(k=1.1, back=False):
    """k scales the 118 px design; 1.1 gives ~130 px, the art guide's 115 px re-scaled to a full 360 px screen."""
    W, H = int(np.ceil(44 * k)) + 1, int(np.ceil(122 * k))
    o = 1   # x offset so the outline fits
    P = lambda pts: (lambda c: c.mpoly([(x * k + o, y * k + 1) for x, y in pts]))
    E = lambda cx, cy, rx, ry: (lambda c: c.mellipse(cx * k + o, cy * k + 1, rx * k, ry * k))
    parts = [
        # legs (behind arms): wide enough to read as trousers, not stilts
        ('pants', P([(12.8, 54), (21.2, 54), (20.6, 64), (20.2, 103), (14.0, 103), (13.4, 64)])),
        ('pants', P([(20.8, 54), (29.2, 54), (28.6, 64), (28.0, 103), (21.8, 103), (21.4, 64)])),
        ('boot', P([(14.0, 103), (20.3, 103), (20.5, 113), (21.2, 117.6), (12.6, 117.6), (13.4, 113)])),
        ('boot', P([(21.7, 103), (28.0, 103), (28.6, 113), (29.4, 117.6), (20.8, 117.6), (21.5, 113)])),
        ('cuff', P([(13.6, 101.5), (20.5, 101.5), (20.5, 105.6), (13.6, 105.6)])),
        ('cuff', P([(21.5, 101.5), (28.4, 101.5), (28.4, 105.6), (21.5, 105.6)])),
        # neck and tunic
        ('skin', P([(18.6, 18.5), (23.4, 18.5), (23.6, 23.5), (18.4, 23.5)])),
        ('tunic', P([(10.4, 24.2), (31.6, 24.2), (31.0, 37), (29.8, 52), (12.2, 52), (11.0, 37)])),
        ('gold', P([(16.0, 21.6), (26.0, 21.6), (26.6, 24.6), (24.0, 26.4), (18.0, 26.4), (15.4, 24.6)])),
        ('skin', P([(18.8, 21.6), (23.2, 21.6), (22.6, 24.2), (19.4, 24.2)])),
        ('gold', P([(10.0, 23.8), (16.0, 23.2), (12.8, 25.8), (12.4, 37), (11.0, 37)])),
        ('gold', P([(32.0, 23.8), (26.0, 23.2), (29.2, 25.8), (29.6, 37), (31.0, 37)])),
        ('emblem', P([(17.0, 31.0), (25.0, 31.0), (21.0, 40.5)])),
        ('belt', P([(12.1, 51.2), (29.9, 51.2), (29.9, 55.0), (12.1, 55.0)])),
        ('buckle', P([(19.0, 51.4), (23.0, 51.4), (23.0, 54.8), (19.0, 54.8)])),
        # arms (in front of the body)
        ('sleeve', P([(10.6, 24.4), (7.6, 26.4), (6.4, 33), (6.2, 44), (6.8, 56), (11.0, 56), (11.4, 44), (11.8, 33)])),
        ('sleeve', P([(31.4, 24.4), (34.4, 26.4), (35.6, 33), (35.8, 44), (35.2, 56), (31.0, 56), (30.6, 44), (30.2, 33)])),
        ('cuff', P([(6.6, 53.6), (11.2, 53.6), (11.2, 58.2), (6.6, 58.2)])),
        ('cuff', P([(30.8, 53.6), (35.4, 53.6), (35.4, 58.2), (30.8, 58.2)])),
        ('skin', P([(6.8, 58), (11.0, 58), (11.6, 62), (10.6, 65.6), (7.6, 65.6), (6.4, 62)])),
        ('skin', P([(31.0, 58), (35.2, 58), (35.6, 62), (34.4, 65.6), (31.4, 65.6), (30.4, 62)])),
        # head: long jaw, thin face
        ('skin', E(15.4, 11.8, 1.2, 2.0)),
        ('skin', E(26.6, 11.8, 1.2, 2.0)),
        ('skin', P([(15.8, 6.0), (26.2, 6.0), (26.6, 11), (25.8, 15.6), (23.2, 19.6), (18.8, 19.6), (16.2, 15.6), (15.4, 11)])),
        # blond quiff swept up and back, higher on his right
        ('hair', P([(15.0, 10.6), (14.8, 5.6), (16.0, 2.8), (18.8, 0.9), (22.6, 0.0), (25.8, 0.8), (27.4, 3.0), (27.2, 6.8), (26.6, 10.0),
                    (25.8, 6.6), (23.6, 5.6), (20.6, 5.9), (17.6, 6.6), (16.0, 7.8)])),
    ]
    if back:
        # back view: no emblem or face; the swept-back hair covers the whole head; collar is a full gold ring
        parts = [p for j, p in enumerate(parts) if j not in (9, 12)]
        parts.append(('hair', P([(15.2, 12.0), (14.8, 5.6), (16.0, 2.8), (18.8, 0.9), (22.6, 0.0), (25.8, 0.8), (27.4, 3.0), (27.2, 6.8),
                                 (26.8, 12.0), (25.4, 15.2), (23.6, 16.6), (21.0, 17.2), (18.4, 16.6), (16.6, 15.2)])))

    def rule(m, i, x, y):
        # cast shadow under the collar and under the belt line, chin shadow on the neck
        if m == 'tunic' and y <= 28 * k:
            return 2 if x > 23 * k else 1
        if m == 'skin' and 19 * k <= y <= 24 * k and i == 6:
            return 2
        if m == 'pants' and y <= 57 * k:
            return 2
        return None

    rgba, mat, pid = build(parts, W, H, light_dir=-1, shade_rule=rule)
    inner = {('tunic', 'sleeve'), ('pants', 'skin'), ('pants', 'cuff'), ('pants', 'sleeve'), ('belt', 'sleeve'),
             ('tunic', 'gold'), ('skin', 'hair'), ('boot', 'cuff'), ('pants', 'boot'), ('pants', 'pants'), ('boot', 'boot'), ('cuff', 'cuff')}
    rgba = outline(rgba, pid, mat, inner)
    # --- face details, placed by hand (SQ6: thin brows, small dark eyes, long nose line, goofy grin)
    if back:
        X = lambda x: int(round(x * k)) + o
        Y = lambda y: int(round(y * k)) + 1
        # a few swept strands so the back of the head isn't a blank egg
        for (x0, y0, x1, y1) in ((18.5, 5, 19.5, 13), (23.5, 4, 22.5, 13)):
            n = int(max(abs(y1 - y0), 1))
            px(rgba, [(X(x0 + (x1 - x0) * t / n), Y(y0 + t)) for t in range(0, n + 1)], '#c8a448')
        return rgba
    X = lambda x: int(round(x * k)) + o
    Y = lambda y: int(round(y * k)) + 1
    px(rgba, [(X(17), Y(10)), (X(18), Y(10)), (X(19), Y(10)), (X(23), Y(10)), (X(24), Y(10)), (X(25), Y(10))], '#b48c38')   # brows
    px(rgba, [(X(18), Y(12)), (X(24), Y(12))], '#ffffff')                                                  # eye whites
    px(rgba, [(X(19), Y(12)), (X(23), Y(12))], '#2a1a28')                                                  # pupils
    px(rgba, [(X(21), Y(13)), (X(21), Y(14)), (X(22), Y(15))], '#b47868')                                     # long nose
    px(rgba, [(X(18), Y(16)), (X(24), Y(16))], '#a05850')                                                  # grin corners
    px(rgba, [(X(19), Y(17)), (X(20), Y(17)), (X(21), Y(17)), (X(22), Y(17)), (X(23), Y(17))], '#7a3030')           # mouth
    px(rgba, [(X(20), Y(18)), (X(21), Y(18)), (X(22), Y(18))], '#f2c4a8')                                     # lower lip light
    px(rgba, [(X(20), Y(52))], '#ffffff')                                                              # buckle shine
    return rgba


# =============================================================== SIDE VIEW (facing right)
def side(k=1.1):
    W, H = int(np.ceil(40 * k)) + 1, int(np.ceil(122 * k))
    o = 1
    P = lambda pts: (lambda c: c.mpoly([(x * k + o, y * k + 1) for x, y in pts]))
    E = lambda cx, cy, rx, ry: (lambda c: c.mellipse(cx * k + o, cy * k + 1, rx * k, ry * k))
    parts = [
        # far leg (a touch behind), then near leg
        ('pants', P([(14.6, 54), (23.8, 54), (23.4, 66), (22.6, 103), (16.0, 103), (15.4, 66)])),
        ('boot', P([(16.0, 103), (22.6, 103), (23.0, 112), (26.8, 114), (27.4, 117.6), (15.4, 117.6), (15.6, 112)])),
        ('pants', P([(16.4, 54), (27.0, 54), (26.4, 66), (25.4, 103), (18.4, 103), (17.6, 66)])),
        ('cuff', P([(18.0, 101.5), (25.6, 101.5), (25.6, 105.6), (18.0, 105.6)])),
        ('boot', P([(18.4, 105), (25.4, 105), (25.8, 112), (29.6, 114), (30.2, 117.6), (17.8, 117.6), (18.0, 112)])),
        # neck, tunic (chest a little forward), belt
        ('skin', P([(18.4, 17.5), (23.2, 17.5), (23.6, 23.5), (18.4, 23.5)])),
        ('tunic', P([(15.0, 24.2), (25.0, 23.4), (28.0, 28), (28.6, 36), (27.4, 52), (15.6, 52), (14.4, 40), (14.2, 30)])),
        ('gold', P([(17.6, 21.4), (23.8, 21.0), (25.4, 24.6), (17.4, 25.0)])),
        ('emblem', P([(26.2, 30.5), (28.6, 30.5), (28.0, 38.5), (26.0, 33)])),
        ('belt', P([(15.4, 51.2), (27.6, 51.2), (27.6, 55.0), (15.4, 55.0)])),
        ('buckle', P([(26.0, 51.4), (28.0, 51.4), (28.0, 54.8), (26.0, 54.8)])),
        # near arm hanging, slight forward swing of the hand
        ('gold', P([(17.0, 24.0), (23.8, 23.6), (24.6, 26.8), (16.4, 27.0)])),
        ('sleeve', P([(16.6, 25.0), (24.4, 25.0), (24.8, 33), (24.4, 44), (24.8, 55.6), (18.8, 55.6), (18.0, 44), (17.0, 33)])),
        ('cuff', P([(19.2, 53.4), (24.6, 53.4), (24.8, 58.0), (19.4, 58.0)])),
        ('skin', P([(19.6, 58), (24.8, 58), (25.6, 62), (24.6, 65.6), (21.0, 65.6), (19.8, 62)])),
        # head in profile: long jaw, nose out front, quiff swept back
        ('skin', P([(16.2, 7), (25.8, 5.6), (26.6, 9.5), (28.2, 12.6), (26.8, 13.4), (26.8, 15.6), (25.8, 17.0), (25.6, 19.4),
                    (21.6, 20.0), (18.4, 18.4), (16.0, 14)])),
        ('hair', P([(14.6, 15.0), (14.0, 9.0), (15.0, 4.6), (18.0, 1.6), (22.6, 0.0), (26.6, 0.6), (28.0, 2.4), (27.2, 5.0),
                    (25.4, 6.4), (22.0, 6.6), (21.0, 8.2), (20.0, 11.6), (18.6, 14.6), (16.6, 16.4)])),
        ('skin', E(19.4, 12.0, 1.4, 2.2)),   # ear
    ]

    def rule(m, i, x, y):
        if m == 'skin' and i == 5:
            return 2
        if m == 'pants' and i == 0:
            return 2
        if m == 'boot' and i == 1:
            return 2
        if m == 'tunic' and y <= 27 * k:
            return 2
        return None

    rgba, mat, pid = build(parts, W, H, light_dir=1, shade_rule=rule)   # facing right: lit from the front
    inner = {('tunic', 'sleeve'), ('pants', 'skin'), ('pants', 'cuff'), ('pants', 'sleeve'), ('belt', 'sleeve'),
             ('pants', 'pants'), ('boot', 'boot'), ('tunic', 'gold'), ('belt', 'skin'), ('pants', 'boot'), ('hair', 'skin')}
    rgba = outline(rgba, pid, mat, inner)
    X = lambda x: int(round(x * k)) + o
    Y = lambda y: int(round(y * k)) + 1
    px(rgba, [(X(23), Y(9)), (X(24), Y(9)), (X(25), Y(9))], '#b48c38')    # brow
    px(rgba, [(X(25), Y(11))], '#ffffff')
    px(rgba, [(X(24), Y(11))], '#2a1a28')                                  # eye
    px(rgba, [(X(24), Y(17)), (X(25), Y(17))], '#7a3030')                  # mouth
    px(rgba, [(X(23), Y(16))], '#a05850')                                  # grin crease
    return rgba


if __name__ == '__main__':
    views = {'front': front(), 'side': side(), 'back': front(back=True)}
    for n, r in views.items():
        save(r, f'roger_{n}.png')
    # turnaround sheet: front, side, back, and side mirrored (facing left)
    from PIL import Image
    ims = [Image.open(f'roger_{n}.png') for n in ('front', 'side', 'back')]
    ims.append(ims[1].transpose(Image.FLIP_LEFT_RIGHT))
    gap = 8
    sheet = Image.new('RGBA', (sum(i.width for i in ims) + gap * 5, max(i.height for i in ims) + gap * 2), (224, 228, 232, 255))
    x = gap
    for i in ims:
        sheet.alpha_composite(i, (x, sheet.height - gap - i.height)); x += i.width + gap
    sheet.save('roger_turnaround.png')
    sheet.resize((sheet.width * 5, sheet.height * 5), Image.NEAREST).save('roger_turnaround_5x.png')
