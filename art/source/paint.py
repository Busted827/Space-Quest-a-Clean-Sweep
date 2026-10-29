"""Tiny painting toolkit: float RGB canvas, supersampled polygons, gradients, lights."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_C = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_M = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def hexc(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32) / 255.0


def mix(a, b, t):
    return a + (b - a) * t


class Canvas:
    def __init__(self, w, h, s=3, bg='#000000'):
        self.w, self.h, self.s = w, h, s
        self.W, self.H = w * s, h * s
        self.img = np.zeros((self.H, self.W, 3), np.float32) + hexc(bg)
        self.emit = np.zeros((self.H, self.W, 3), np.float32)  # added after lighting
        yy, xx = np.mgrid[0:self.H, 0:self.W].astype(np.float32)
        self.X, self.Y = (xx + 0.5) / s, (yy + 0.5) / s

    # ---- masks -------------------------------------------------------------
    def _mask(self, draw_fn):
        m = Image.new('L', (self.W, self.H), 0)
        draw_fn(ImageDraw.Draw(m), self.s)
        return np.asarray(m, np.float32) / 255.0

    def mpoly(self, pts):
        return self._mask(lambda d, s: d.polygon([(x * s, y * s) for x, y in pts], fill=255))

    def mrect(self, x0, y0, x1, y1):
        return self.mpoly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])

    def mellipse(self, cx, cy, rx, ry):
        return self._mask(lambda d, s: d.ellipse([(cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s], fill=255))

    def mline(self, pts, width):
        return self._mask(lambda d, s: d.line([(x * s, y * s) for x, y in pts], fill=255, width=max(1, int(width * s)), joint='curve'))

    def mtext(self, xy, text, size, font=FONT_B, anchor='la', spacing=0):
        f = ImageFont.truetype(font, int(size * self.s))
        return self._mask(lambda d, s: d.multiline_text((xy[0] * s, xy[1] * s), text, font=f, fill=255, anchor=anchor, spacing=spacing * s, align='center'))

    # ---- painting ----------------------------------------------------------
    def paint(self, mask, color, alpha=1.0, layer=None):
        layer = self.img if layer is None else layer
        c = color(self.X, self.Y) if callable(color) else hexc(color) if isinstance(color, str) else np.asarray(color, np.float32)
        a = (mask * alpha)[..., None]
        layer[:] = layer * (1 - a) + c * a

    def glow(self, cx, cy, rx, ry, color, strength=1.0, power=2.0):
        d = np.sqrt(((self.X - cx) / rx) ** 2 + ((self.Y - cy) / ry) ** 2)
        g = np.clip(1 - d, 0, 1) ** power * strength
        self.emit += g[..., None] * hexc(color)

    def darken(self, mask, color, amount):
        """Multiply toward a tinted shadow color (purple, never black)."""
        c = hexc(color)
        a = (mask * amount)[..., None]
        self.img[:] = self.img * (1 - a) + (self.img * c) * a

    # ---- gradients ---------------------------------------------------------
    @staticmethod
    def vgrad(c0, c1, y0, y1):
        a, b = hexc(c0), hexc(c1)
        def f(X, Y):
            t = np.clip((Y - y0) / max(1e-6, (y1 - y0)), 0, 1)[..., None]
            return a + (b - a) * t
        return f

    @staticmethod
    def hgrad(c0, c1, x0, x1):
        a, b = hexc(c0), hexc(c1)
        def f(X, Y):
            t = np.clip((X - x0) / max(1e-6, (x1 - x0)), 0, 1)[..., None]
            return a + (b - a) * t
        return f

    # ---- finishing ---------------------------------------------------------
    def finish(self, light=None, grain=0.03, vignette=0.25, seed=7):
        img = self.img
        if light is not None:
            img = img * light
        img = img + self.emit
        im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).resize((self.w, self.h), Image.LANCZOS)
        a = np.asarray(im, np.float32) / 255.0
        yy, xx = np.mgrid[0:self.h, 0:self.w].astype(np.float32)
        if vignette:
            d = np.sqrt(((xx - self.w / 2) / (self.w / 2)) ** 2 + ((yy - self.h / 2) / (self.h / 2)) ** 2)
            v = 1 - vignette * np.clip(d - 0.55, 0, 1) ** 1.5
            a = a * mix(hexc('#3a2050'), np.ones(3, np.float32), v[..., None])
        rng = np.random.default_rng(seed)
        a = a + (rng.random((self.h, self.w, 1)).astype(np.float32) - 0.5) * grain * 2
        return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def _nearest(px, cents):
    out = np.empty(len(px), np.int32)
    cn = (cents ** 2).sum(1)
    for i in range(0, len(px), 40000):
        p = px[i:i + 40000]
        out[i:i + 40000] = np.argmin(cn[None, :] - 2 * p @ cents.T, axis=1)
    return out


def to_256(im, colors=256, iters=12, seed=1, noise=0.0):
    """Reduce to an SQ6-style 256-color palette (k-means, so small bright details keep their color)."""
    a = np.asarray(im.convert('RGB'), np.float32)
    px = a.reshape(-1, 3)
    rng = np.random.default_rng(seed)
    # seed from the median-cut palette, then refine
    pal = np.array(im.convert('RGB').quantize(colors, method=Image.Quantize.MEDIANCUT).getpalette()[:colors * 3], np.float32).reshape(-1, 3)
    cents = pal.copy()
    sample = px[rng.choice(len(px), min(len(px), 120000), replace=False)]
    # weight saturated pixels more so accents survive
    sat = sample.max(1) - sample.min(1)
    w = 1 + sat / 40.0
    for _ in range(iters):
        lab = _nearest(sample, cents)
        sums = np.zeros_like(cents); np.add.at(sums, lab, sample * w[:, None])
        cnt = np.zeros(len(cents)); np.add.at(cnt, lab, w)
        nz = cnt > 0
        cents[nz] = sums[nz] / cnt[nz, None]
    if noise:
        px = px + (rng.random((len(px), 1), dtype=np.float32) - 0.5) * 2 * noise
    lab = _nearest(px, cents)
    out = np.clip(cents[lab], 0, 255).astype(np.uint8).reshape(a.shape)
    return Image.fromarray(out)
