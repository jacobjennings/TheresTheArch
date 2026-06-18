#!/usr/bin/env python3
"""Generate assets/icon.png — a simple Gateway-Arch silhouette app icon.

Reproducible placeholder icon used for packaged builds (e.g. the Linux
AppImage). Run with Pillow installed:  python assets/make_icon.py
"""
import math
import os

from PIL import Image, ImageDraw

W = H = 512
SS = 2  # supersample for smoother edges
w, h = W * SS, H * SS

BG_TOP = (18, 22, 32)
BG_BOTTOM = (30, 38, 56)
ARCH = (203, 209, 219)      # stainless-steel light
ARCH_EDGE = (150, 158, 172)

cx = w / 2
baseline = h * 0.90
halfw_o, yo_apex = w * 0.40, h * 0.10
halfw_i, yi_apex = w * 0.255, h * 0.30
ko, ki = 2.4 / halfw_o, 2.4 / halfw_i


def curve(x, halfw, apex):
    d = x - cx
    norm = (math.cosh(min(abs(d), halfw) / halfw * 2.4) - 1) / (math.cosh(2.4) - 1)
    return apex + norm * (baseline - apex)


img = Image.new("RGB", (w, h), BG_TOP)
draw = ImageDraw.Draw(img)

# vertical background gradient
for y in range(h):
    t = y / h
    c = tuple(int(BG_TOP[i] + (BG_BOTTOM[i] - BG_TOP[i]) * t) for i in range(3))
    draw.line([(0, y), (w, y)], fill=c)

# arch silhouette = area between outer and inner catenaries, flat leg bottoms
N = 240
outer = [(cx - halfw_o + 2 * halfw_o * i / N,
          curve(cx - halfw_o + 2 * halfw_o * i / N, halfw_o, yo_apex)) for i in range(N + 1)]
inner = [(cx + halfw_i - 2 * halfw_i * i / N,
          curve(cx + halfw_i - 2 * halfw_i * i / N, halfw_i, yi_apex)) for i in range(N + 1)]
poly = outer + [(cx + halfw_i, baseline)] + inner + [(cx - halfw_i, baseline)]
draw.polygon(poly, fill=ARCH, outline=ARCH_EDGE)

img = img.resize((W, H), Image.LANCZOS)
out = os.path.join(os.path.dirname(__file__), "icon.png")
img.save(out)
print("wrote", out, img.size)
