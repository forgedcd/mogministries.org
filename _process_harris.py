#!/usr/bin/env python3
"""Process the Lt. Harris photo — same warm-dark treatment as the other new photos."""
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import os

SRC = "/home/user/workspace/uploaded_attachments/251071019f1f43d6b21e0fb141bdeba4/IMG_0816.jpeg"
OUT_DIR = "/home/user/workspace/mog-site/assets/img"
SLUG = "lt-harris"

# Crop hint: portrait, keep both figures, focus slightly right of center on Harris's face
CROP_RATIO = (4, 5)   # portrait-ish
FOCUS = (0.55, 0.35)  # slightly right, upper third for the faces

BRIGHTNESS = 0.72
SATURATION = 0.48
CONTRAST   = 1.12
WARM_BLEND = 0.12
VIGNETTE_STRENGTH = 0.35


def crop_focus(img, ratio_w, ratio_h, fx, fy):
    w, h = img.size
    target_ratio = ratio_w / ratio_h
    src_ratio = w / h
    if src_ratio > target_ratio:
        # source is wider than target — crop width
        new_w = int(h * target_ratio)
        new_h = h
    else:
        new_w = w
        new_h = int(w / target_ratio)
    cx = int(w * fx)
    cy = int(h * fy)
    left = max(0, min(w - new_w, cx - new_w // 2))
    top  = max(0, min(h - new_h, cy - new_h // 2))
    return img.crop((left, top, left + new_w, top + new_h))


def warm_blend(img, amount):
    warm = Image.new("RGB", img.size, (255, 190, 120))
    return Image.blend(img, warm, amount)


def vignette(img, strength):
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    # radial gradient
    max_r = int(((w/2)**2 + (h/2)**2) ** 0.5)
    steps = 80
    for i in range(steps):
        alpha = int(255 * (i / steps) * strength)
        r = int(max_r * (1 - i / steps))
        draw.ellipse([w/2 - r, h/2 - r, w/2 + r, h/2 + r], fill=255 - alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=max_r // 8))
    black = Image.new("RGB", (w, h), (0, 0, 0))
    return Image.composite(img, black, mask)


def process(img):
    img = ImageEnhance.Brightness(img).enhance(BRIGHTNESS)
    img = ImageEnhance.Color(img).enhance(SATURATION)
    img = ImageEnhance.Contrast(img).enhance(CONTRAST)
    img = warm_blend(img, WARM_BLEND)
    img = vignette(img, VIGNETTE_STRENGTH)
    return img


def main():
    src = Image.open(SRC).convert("RGB")
    src = crop_focus(src, *CROP_RATIO, *FOCUS)
    out = process(src)
    for w in (1600, 800):
        h = int(w * CROP_RATIO[1] / CROP_RATIO[0])
        resized = out.resize((w, h), Image.LANCZOS)
        path = os.path.join(OUT_DIR, f"{SLUG}-{w}.webp")
        resized.save(path, "WEBP", quality=82, method=6)
        print(f"wrote {path}  {resized.size}")


if __name__ == "__main__":
    main()
