"""Draws placeholder art for the first playable room.

Every image here is temporary: real art replaces it file for file, keeping
the same names and sizes so no scene has to change.
"""
import os
import sys
from PIL import Image, ImageDraw

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
OUT = os.path.join(ROOT, "game", "placeholders")
os.makedirs(OUT, exist_ok=True)

# Master palette draft: SQ6-style teals, purples and amber light.
WALL = (46, 74, 92)
WALL_DARK = (32, 52, 66)
FLOOR = (70, 62, 78)
FLOOR_LINE = (58, 50, 66)
TRIM = (110, 84, 150)
AMBER = (232, 176, 84)
METAL = (128, 140, 150)
METAL_DARK = (88, 98, 108)
WOOD = (140, 98, 58)
WOOD_DARK = (104, 70, 40)
INK = (20, 22, 28)
WHITE = (236, 236, 240)
PURPLE = (120, 72, 170)
SKIN = (240, 196, 160)
HAIR = (238, 206, 92)


def save(img, name):
    img.save(os.path.join(OUT, name))


def background():
    img = Image.new("RGB", (640, 360), WALL)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 639, 48], fill=WALL_DARK)
    for x in range(0, 640, 80):
        d.line([x, 0, x, 48], fill=INK)
    d.rectangle([90, 10, 170, 40], fill=(60, 92, 112), outline=INK)
    d.text((104, 18), "4-8-15", fill=WALL_DARK)
    # Ceiling lamp glow
    d.polygon([(300, 48), (340, 48), (420, 236), (220, 236)], fill=(54, 84, 102))
    d.rectangle([0, 236, 639, 359], fill=FLOOR)
    for y in range(252, 360, 18):
        d.line([0, y, 639, y], fill=FLOOR_LINE)
    d.rectangle([0, 232, 639, 238], fill=TRIM)
    # Crate
    d.rectangle([60, 222, 200, 300], fill=WOOD, outline=WOOD_DARK, width=3)
    d.line([60, 222, 200, 300], fill=WOOD_DARK, width=3)
    d.line([200, 222, 60, 300], fill=WOOD_DARK, width=3)
    d.ellipse([110, 214, 150, 226], fill=(170, 200, 210))
    # Shelves
    for y in (90, 140, 190):
        d.rectangle([230, y, 340, y + 6], fill=METAL_DARK)
        for i, x in enumerate(range(238, 332, 18)):
            colors = [(80, 170, 120), (210, 90, 90), (90, 130, 210), AMBER]
            d.rectangle([x, y - 26, x + 12, y], fill=colors[i % 4], outline=INK)
    d.rectangle([228, 70, 232, 232], fill=METAL_DARK)
    d.rectangle([338, 70, 342, 232], fill=METAL_DARK)
    # Poster
    d.rectangle([360, 80, 430, 150], fill=(230, 220, 190), outline=INK)
    d.text((366, 88), "EMPLOYEE", fill=INK)
    d.text((366, 100), "OF THE", fill=INK)
    d.text((366, 112), "MONTH", fill=INK)
    d.text((366, 132), "(NEVER)", fill=(170, 40, 40))
    # Locker
    d.rectangle([470, 90, 540, 280], fill=METAL, outline=INK, width=2)
    for y in range(104, 130, 6):
        d.line([482, y, 528, y], fill=METAL_DARK, width=2)
    d.ellipse([522, 180, 534, 192], fill=INK)
    d.text((484, 240), "WILCO", fill=INK)
    # Door
    d.rectangle([570, 80, 636, 300], fill=METAL_DARK, outline=INK, width=2)
    d.rectangle([578, 92, 628, 140], fill=(150, 200, 210), outline=INK)
    d.rectangle([576, 184, 584, 204], fill=AMBER)
    d.text((582, 260), "13-B", fill=WHITE)
    d.text((8, 344), "PLACEHOLDER ART", fill=FLOOR_LINE)
    save(img, "supply_closet_bg.png")


def roger():
    # 40x110, feet at the bottom edge. Classic white and purple suit.
    img = Image.new("RGBA", (40, 110), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([12, 98, 19, 109], fill=PURPLE)
    d.rectangle([21, 98, 28, 109], fill=PURPLE)
    d.rectangle([12, 62, 19, 98], fill=WHITE, outline=INK)
    d.rectangle([21, 62, 28, 98], fill=WHITE, outline=INK)
    d.rectangle([9, 28, 31, 64], fill=WHITE, outline=INK)
    d.rectangle([9, 56, 31, 60], fill=PURPLE)
    d.rectangle([9, 28, 31, 32], fill=PURPLE)
    d.rectangle([4, 30, 9, 58], fill=WHITE, outline=INK)
    d.rectangle([31, 30, 36, 58], fill=WHITE, outline=INK)
    d.rectangle([4, 58, 9, 63], fill=SKIN)
    d.rectangle([31, 58, 36, 63], fill=SKIN)
    d.rectangle([12, 8, 28, 27], fill=SKIN, outline=INK)
    d.rectangle([26, 15, 31, 19], fill=SKIN, outline=INK)
    d.rectangle([11, 2, 29, 10], fill=HAIR, outline=INK)
    d.rectangle([22, 13, 24, 15], fill=INK)
    save(img, "roger.png")


def mop():
    img = Image.new("RGBA", (18, 84), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([7, 0, 10, 64], fill=WOOD, outline=WOOD_DARK)
    d.polygon([(1, 83), (17, 83), (13, 64), (5, 64)], fill=(200, 196, 170), outline=INK)
    save(img, "mop.png")


def bucket():
    img = Image.new("RGBA", (30, 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.arc([4, 0, 26, 18], 180, 360, fill=INK, width=2)
    d.polygon([(2, 8), (28, 8), (25, 29), (5, 29)], fill=(220, 190, 60), outline=INK)
    save(img, "bucket.png")


def icon(name, fill, label):
    img = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([2, 2, 21, 21], fill=fill, outline=INK)
    d.text((6, 6), label, fill=INK)
    save(img, name)


background()
roger()
mop()
bucket()
icon("inv_mop.png", (200, 196, 170), "M")
icon("inv_bucket.png", (220, 190, 60), "B")
icon("inv_keycard.png", (150, 200, 210), "K")
print("placeholders written to", OUT)
