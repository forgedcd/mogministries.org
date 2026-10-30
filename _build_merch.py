#!/usr/bin/env python3
"""Build the approved MOG merch experience without changing other site pages."""
import json
from pathlib import Path

ROOT = Path(__file__).parent


def build_merch():
    raw = json.loads((ROOT / "_merch_catalog.json").read_text(encoding="utf-8"))
    catalog = []
    for product in raw:
        title = product["title"]
        lower = title.lower()
        category = (
            "Headwear" if "hat" in lower or "flat bill" in lower
            else "Accessories" if "sticker" in lower else "Apparel"
        )
        catalog.append({
            "title": title,
            "handle": product["handle"],
            "price": float(product["priceRangeV2"]["minVariantPrice"]["amount"]),
            "category": category,
            "image": f"./assets/{product['handle']}.webp",
        })
    html = (ROOT / "_merch_template.html").read_text(encoding="utf-8")
    commerce = (ROOT / "_merch_commerce.js").read_text(encoding="utf-8")
    data = json.dumps(catalog, separators=(",", ":")).replace("<", "\\u003c")
    html = html.replace("__CATALOG__", data).replace("__COMMERCE__", commerce)
    html = html.replace("./assets/", "./assets/merch/v20261030/")
    (ROOT / "merch.html").write_text(html, encoding="utf-8")
    return len(catalog)


if __name__ == "__main__":
    print(f"Built MOG merch with {build_merch()} products.")
