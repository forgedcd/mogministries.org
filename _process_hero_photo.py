"""Turn IMG_8958 into a portrait hero image that blends with the black/gold site."""
from PIL import Image, ImageEnhance, ImageFilter

SRC = "/home/user/workspace/uploaded_attachments/b135f379fb7f46e387b504a7d8759971/IMG_8958.jpg"
OUT_BASE = "/home/user/workspace/mog-site/assets/img/yard-vertical"

im = Image.open(SRC).convert("RGB")
w, h = im.size  # 1711 x 956

# Target aspect ratio 2:3 (portrait) to match the old cell image slot (1024x1536)
target_ratio = 2 / 3  # w/h
# We need to crop w/h == 2/3 => new_w = h*2/3 for a given h. Since source is landscape,
# we'll crop the width to make it portrait, keeping the center of interest (subject teaching).
# Frank (the teacher in black) sits roughly centered horizontally; slight right bias in the frame.
# Compute portrait crop width from full height:
new_w = int(h * target_ratio)  # 956 * 2/3 = 637
# Center the crop around x = 720 (Frank's position) for a stronger portrait composition
cx = 720
left = max(0, cx - new_w // 2)
right = left + new_w
if right > w:
    right = w
    left = right - new_w
crop = im.crop((left, 0, right, h))  # portrait

# Upscale to 1024x1536 to match old slot dimensions
target = crop.resize((1024, 1536), Image.LANCZOS)

# --- Tonal grading: darken + desaturate slightly + warm shadows ---
target = ImageEnhance.Brightness(target).enhance(0.70)
target = ImageEnhance.Color(target).enhance(0.42)
target = ImageEnhance.Contrast(target).enhance(1.14)

# --- Warm-black overlay + top-down gold cast + bottom vignette ---
# We recolor by blending each pixel toward warm tones based on its luminance,
# then apply a vertical darkening gradient.
photo_data = target.load()
w2, h2 = target.size

# Top-down warm gold cast strength (fades from 0 at top down to 0 at 55% and back up at bottom)
# Bottom of the image gets pushed to near-black to blend with page background.
import math
for y in range(h2):
    # Vertical darkening: heavy at very top (sky) AND heavy at bottom to blend into page.
    t = y / (h2 - 1)
    # bell curve peaked around 0.45 with 1.0 dark at edges
    dark_boost = max(0.0, abs(t - 0.45) * 1.55 - 0.15)  # 0 near center, up to ~0.7 at edges
    dark_boost = min(0.72, dark_boost)

    # Warm gold tint mixed into shadows (stronger where dark_boost is higher)
    tint_r, tint_g, tint_b = 24, 18, 10

    for x in range(w2):
        pr, pg, pb = photo_data[x, y]
        # Base warm cast: shift blue slightly toward gold in shadows
        lum = (pr * 299 + pg * 587 + pb * 114) / 1000
        shadow_w = max(0.0, 1.0 - lum / 180)  # more shadow influence in darker pixels
        wr = int(pr + (tint_r - pr) * 0.10 * shadow_w)
        wg = int(pg + (tint_g - pg) * 0.10 * shadow_w)
        wb = int(pb + (tint_b - pb) * 0.22 * shadow_w)

        # Apply dark gradient overlay (blend toward warm black)
        a = dark_boost
        r = int(wr * (1 - a) + 10 * a)
        g = int(wg * (1 - a) + 8 * a)
        b = int(wb * (1 - a) + 6 * a)
        photo_data[x, y] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

# Save at two widths
target.save(OUT_BASE + "-1024.webp", "WEBP", quality=84, method=6)
target.resize((512, 768), Image.LANCZOS).save(OUT_BASE + "-512.webp", "WEBP", quality=82, method=6)
print("saved", OUT_BASE + "-1024.webp")
