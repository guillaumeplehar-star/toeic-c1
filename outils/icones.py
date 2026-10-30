#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dessine les icônes de l'appli (demande Pillow : py -m pip install pillow) :

    py outils\\icones.py

icon-192.png, icon-512.png, apple-touch-icon.png (180 px) et icon-maskable-512.png (marge de sécurité
pour les icônes rondes d'Android). Police : Segoe UI gras (Windows), sinon Arial gras, sinon DejaVu.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLUE, LIGHT, WHITE, RED = (43, 86, 168), (178, 201, 240), (255, 255, 255), (232, 96, 84)
FONTS = [r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "/System/Library/Fonts/Supplemental/Arial Bold.ttf"]


def font(size):
    for path in FONTS:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    sys.exit("Aucune police grasse trouvée.")


def draw(size, scale):
    """scale : part de l'icône occupée par le dessin (1 pour une icône carrée, moins pour une icône masquable)."""
    s = 4 * size                                   # dessiné en grand puis réduit : bords nets
    img = Image.new("RGB", (s, s), BLUE)
    d = ImageDraw.Draw(img)
    k = s * scale
    cx, cy = s / 2, s / 2
    big = font(int(k * 0.40))
    small = font(int(k * 0.13))
    d.text((cx, cy - k * 0.20), "CAP", font=small, fill=LIGHT, anchor="ms")
    d.text((cx, cy + k * 0.17), "945", font=big, fill=WHITE, anchor="ms")
    w = k * 0.50                                    # the target line under the score
    d.rounded_rectangle((cx - w / 2, cy + k * 0.25, cx + w / 2, cy + k * 0.285), radius=k * 0.02, fill=RED)
    return img.resize((size, size), Image.LANCZOS)


def main():
    for name, size, scale in [("icon-192.png", 192, 1), ("icon-512.png", 512, 1), ("apple-touch-icon.png", 180, 1),
                              ("icon-maskable-512.png", 512, 0.78)]:
        draw(size, scale).save(os.path.join(ROOT, name), optimize=True)
        print(name)


if __name__ == "__main__":
    main()
