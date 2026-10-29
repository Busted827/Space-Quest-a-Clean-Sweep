"""Mop + bucket props, then the preview: room + Roger + props + classic SQ4/SQ5 grey top bar."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from paint import Canvas, hexc, to_256, FONT_C

W, H = 640, 360


def prop(draw_fn, box):
    """Draw with the painter onto black and onto a coverage mask; return a cropped RGBA sprite."""
    c = Canvas(W, H, s=3)
    cov = np.zeros((c.H, c.W), np.float32)
    def p(mask, color, alpha=1.0):
        c.paint(mask, color, alpha)
        cov[:] = np.maximum(cov, mask * alpha)
    draw_fn(c, p)
    rgb = Image.fromarray((np.clip(c.img, 0, 1) * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
    a = Image.fromarray((cov * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
    a = a.point(lambda v: 255 if v >= 110 else 0)
    rgb = Image.fromarray((np.asarray(rgb, np.float32) * np.array([0.86, 0.83, 0.93])).astype(np.uint8))  # room's lavender ambient
    im = rgb.convert('RGBA'); im.putalpha(a)
    return im.crop(box), box


def mop(c, p):
    # handle leaning on the back wall, head on the floor
    p(c.mline([(442, 128), (452, 236)], 2.4), '#c8a060')
    p(c.mline([(442.4, 128), (452.4, 236)], 0.8), '#f0d090', 0.8)
    p(c.mpoly([(444, 232), (460, 232), (468, 248), (436, 248)]), '#e8e4d0')
    for k in range(9):
        x = 438 + k * 3.6
        p(c.mline([(452 + (x - 452) * 0.3, 234), (x, 249)], 1.0), '#b8b4a0', 0.9)
    p(c.mrect(446, 229, 458, 234), '#6b6d6b')
    edge = c.mline([(444, 232), (460, 232), (468, 248), (436, 248), (444, 232)], 0.8)
    p(edge, '#2a2236', 0.8)


def bucket(c, p):
    x0, x1, y0, y1 = 470, 500, 226, 252
    p(c.mpoly([(x0, y0), (x1, y0), (x1 - 3, y1), (x0 + 3, y1)]), c.hgrad('#ffe060', '#c08a10', x0, x1))
    p(c.mellipse((x0 + x1) / 2, y0, 15, 3.2), '#8a6a10')
    p(c.mellipse((x0 + x1) / 2, y0 + 0.6, 12.5, 2.2), '#6fa0c8')          # grey-blue mop water
    for yy in (232, 246):
        p(c.mline([(x0 + 0.5, yy), (x1 - 0.5, yy)], 1.0), '#a87010')
    # wire handle
    p(c._mask(lambda d, s: d.arc([(x0 + 1) * s, (y0 - 14) * s, (x1 - 1) * s, (y0 + 6) * s], 180, 360, fill=255, width=int(1.2 * s))), '#5c6a84')
    p(c.mline([(x0, y0), (x1, y0), (x1 - 3, y1), (x0 + 3, y1), (x0, y0)], 0.8), '#2a2236', 0.85)


def shadow(im, cx, cy, rx, ry, amount=0.45):
    a = np.asarray(im.convert('RGB'), np.float32)
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    d = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
    m = (np.clip(1 - d, 0, 1) ** 0.6 * amount)[..., None]
    tint = hexc('#5a3c8a') * 255
    a = a * (1 - m) + (a * tint / 255) * m
    return Image.fromarray(a.astype(np.uint8)).convert('RGBA')


def top_bar(im):
    """SQ4/SQ5 idle bar: thin grey strip, title left, score right. It drops down into the icon bar on hover."""
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 10], fill=(170, 170, 170, 255))
    d.line([0, 10, W, 10], fill=(90, 90, 90, 255))
    f = ImageFont.truetype(FONT_C, 9)
    d.text((5, 0), "Roger Wilco and the Clean Sweep", font=f, fill=(20, 20, 20, 255))
    d.text((W - 5, 0), "Score: 0 of 500", font=f, fill=(20, 20, 20, 255), anchor='ra')
    return im


if __name__ == '__main__':
    bg = Image.open('supply_closet_bg.png').convert('RGBA')
    m, mb = prop(mop, (432, 124, 472, 252))
    b, bb = prop(bucket, (466, 208, 504, 254))
    m.save('prop_mop.png'); b.save('prop_bucket.png')
    roger = Image.open('roger_side.png')
    rx, ry = 262, 318
    scene = shadow(bg, rx + roger.width / 2, ry - 1, 15, 3.5)
    scene = shadow(scene, 452, 248, 18, 3, 0.35)
    scene = shadow(scene, 486, 252, 17, 3, 0.4)
    scene.alpha_composite(m, mb[:2])
    scene.alpha_composite(b, bb[:2])
    scene.alpha_composite(roger, (rx, ry - roger.height))
    scene.convert('RGB').save('preview_no_bar.png')
    top_bar(scene)
    scene.convert('RGB').save('preview.png')
    scene.convert('RGB').resize((W * 2, H * 2), Image.NEAREST).save('preview_2x.png')
    print('ok')
