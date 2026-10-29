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
def corridor():
    # Service Corridor: long hall, doors along the back wall, a drip feeding a puddle.
    img = Image.new("RGB", (640, 360), WALL)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 639, 40], fill=WALL_DARK)
    for x in range(0, 640, 64):
        d.line([x, 0, x, 40], fill=INK)
    # Leaky pipe along the ceiling, dripping over the puddle
    d.rectangle([0, 44, 639, 52], fill=METAL_DARK, outline=INK)
    d.rectangle([414, 52, 426, 64], fill=METAL, outline=INK)
    for y in (76, 104, 140):
        d.ellipse([417, y, 423, y + 8], fill=(150, 170, 150))
    d.rectangle([0, 236, 639, 359], fill=FLOOR)
    for y in range(252, 360, 18):
        d.line([0, y, 639, y], fill=FLOOR_LINE)
    d.rectangle([0, 232, 639, 238], fill=TRIM)

    def door(x0, x1, label, color=METAL_DARK):
        d.rectangle([x0, 96, x1, 236], fill=color, outline=INK, width=2)
        d.line([(x0 + x1) // 2, 96, (x0 + x1) // 2, 236], fill=INK)
        d.rectangle([x0, 80, x1, 94], fill=INK)
        d.text((x0 + 4, 82), label, fill=AMBER)

    door(14, 74, "13-B")
    door(120, 190, "CREW")
    door(236, 306, "GALLEY")
    door(440, 506, "STAFF", (110, 70, 70))
    # Lift lobby archway at the far end
    d.rectangle([566, 70, 639, 236], fill=(30, 44, 56), outline=INK, width=2)
    d.text((576, 74), "LIFTS", fill=AMBER)
    # Waste chute hatch, low on the wall
    d.rectangle([520, 196, 552, 230], fill=METAL, outline=INK, width=2)
    d.text((522, 186), "CHUTE", fill=WHITE)
    # PA speaker and poster
    d.ellipse([206, 60, 226, 80], fill=METAL_DARK, outline=INK)
    d.rectangle([326, 110, 400, 180], fill=(230, 220, 190), outline=INK)
    d.text((332, 116), "A CLEAN", fill=INK)
    d.text((332, 128), "SHIP IS A", fill=INK)
    d.text((332, 140), "HAPPY SHIP", fill=INK)
    d.text((332, 162), "-Dr. P. Ure", fill=(40, 90, 120))
    d.text((8, 344), "PLACEHOLDER ART", fill=FLOOR_LINE)
    save(img, "service_corridor_bg.png")


def puddle():
    img = Image.new("RGBA", (130, 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([0, 4, 129, 29], fill=(120, 140, 120, 220), outline=(80, 96, 80))
    d.ellipse([30, 10, 70, 18], fill=(170, 190, 170, 200))
    save(img, "puddle.png")


def bucket_icons():
    # The Filth Meter: the bucket icon gets grosser at each level (0 to 5).
    water = [None, (120, 130, 120), (120, 100, 50), (80, 90, 40), (90, 60, 80), (60, 120, 30)]
    for level in range(1, 6):
        img = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rectangle([2, 2, 21, 21], fill=(220, 190, 60), outline=INK)
        d.rectangle([4, 4, 19, 9], fill=water[level])
        d.text((8, 11), str(level), fill=INK)
        save(img, "inv_bucket_%d.png" % level)


corridor()
puddle()
bucket_icons()
print("placeholders written to", OUT)
