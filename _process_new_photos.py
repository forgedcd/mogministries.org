"""Process the 8 new photos with the site's warm-black treatment.

Each source photo produces two WebP outputs at 1600 and 800 wide.
Treatment: brightness 0.72, saturation 0.48, contrast 1.12, warm gold
shadow tint, vignette. Consistent with yard-vertical/yard-teaching pattern.
"""
from PIL import Image, ImageEnhance, ImageFilter
from pathlib import Path
import math

SRC = Path("/home/user/workspace/uploaded_attachments/f80a9145b442494ea8f39873c8824031")
DST = Path("/home/user/workspace/mog-site/assets/img")

# (source_filename, output_slug, crop_hint)
# crop_hint: None = center, or (target_ratio_w, target_ratio_h, focus_x_ratio, focus_y_ratio)
PHOTOS = [
    ("IMG_8020.jpeg",       "baptism-water",   (3, 4, 0.5, 0.45)),  # portrait crop, keep face+water
    ("FullSizeRender.jpeg", "warden-suwannee", (3, 4, 0.5, 0.55)),  # portrait, keep faces
    ("IMG_0235.jpeg",       "hopedealer-stage",(3, 2, 0.5, 0.5)),   # landscape
    ("IMG_8959.jpeg",       "yard-prayer",     (3, 4, 0.55, 0.55)),  # portrait
    ("image000001.jpeg",    "chapel-family",   (3, 2, 0.5, 0.55)),   # landscape group
    ("image000002.jpeg",    "chapel-teaching", (3, 4, 0.45, 0.55)),  # portrait teaching
    ("1000005539.jpeg",     "county-preach",   (3, 4, 0.5, 0.5)),
    ("1000005540.jpeg",     "county-prayer",   (3, 4, 0.5, 0.55)),
]

def smart_crop(img, ratio_w, ratio_h, fx, fy):
    W, H = img.size
    target = ratio_w / ratio_h
    current = W / H
    if abs(current - target) < 0.01:
        return img
    if current > target:
        # too wide, crop width
        new_w = int(H * target)
        cx = int(W * fx)
        left = max(0, min(W - new_w, cx - new_w // 2))
        return img.crop((left, 0, left + new_w, H))
    else:
        new_h = int(W / target)
        cy = int(H * fy)
        top = max(0, min(H - new_h, cy - new_h // 2))
        return img.crop((0, top, W, top + new_h))

def warm_darken(img):
    # brightness / saturation / contrast
    img = ImageEnhance.Brightness(img).enhance(0.72)
    img = ImageEnhance.Color(img).enhance(0.48)
    img = ImageEnhance.Contrast(img).enhance(1.12)
    # warm gold shadow tint via blended overlay
    tint = Image.new("RGB", img.size, (28, 20, 10))
    img = Image.blend(img, tint, 0.12)
    # subtle vignette
    W, H = img.size
    vig = Image.new("L", (W, H), 0)
    px = vig.load()
    cx, cy = W / 2, H / 2
    max_d = math.hypot(cx, cy)
    for y in range(H):
        for x in range(W):
            d = math.hypot(x - cx, y - cy) / max_d
            # inner ~55% stays clear, outer darkens up to ~55
            v = int(max(0, (d - 0.5)) * 110)
            px[x, y] = min(255, v)
    vig = vig.filter(ImageFilter.GaussianBlur(radius=W * 0.02))
    black = Image.new("RGB", img.size, (8, 6, 3))
    img = Image.composite(black, img, vig)
    return img

def process(src_name, slug, crop_hint):
    print(f"→ {src_name}  →  {slug}")
    img = Image.open(SRC / src_name).convert("RGB")
    if crop_hint:
        img = smart_crop(img, *crop_hint)
    img = warm_darken(img)
    # 1600 wide
    W1 = 1600
    H1 = int(img.height * (W1 / img.width))
    big = img.resize((W1, H1), Image.LANCZOS)
    big.save(DST / f"{slug}-1600.webp", "WEBP", quality=82, method=6)
    # 800 wide
    W2 = 800
    H2 = int(img.height * (W2 / img.width))
    small = img.resize((W2, H2), Image.LANCZOS)
    small.save(DST / f"{slug}-800.webp", "WEBP", quality=82, method=6)
    print(f"   {W1}x{H1} + {W2}x{H2}")

if __name__ == "__main__":
    for row in PHOTOS:
        process(*row)
    print("done")
