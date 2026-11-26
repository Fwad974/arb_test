#!/usr/bin/env python3
"""Turn client logo files into clean, monochrome, optically balanced WebP files.

    pip install pillow numpy
    python3 scripts/prepare_logos.py SOURCE_DIR assets/images/clients

Each source file is named <slug>.png / .jpg / .webp (the slug used in content.py).
Every output is <slug>.webp on a 360x160 transparent canvas, in black ink only:

- Backgrounds disappear. Ink comes from how much darker a pixel is than the logo's
  own background (white, cream, or transparent), so boxes behind logos vanish and
  white details inside a mark (e.g. text in an ellipse) stay knocked out.
- Contrast is normalised per logo, so pale teal or green logos are not faint.
- Size is optical: each logo is scaled so it carries about the same amount of ink,
  then centred, so a sparse dotted mark and a heavy wordmark look equally weighted.

The site shows these at reduced opacity in light mode and inverted in dark mode,
so the same file works on both backgrounds. Only build.py's standard library is
needed to build the site; this script is just for preparing new logos.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

W, H, PAD = 360, 160, 6
TARGET_INK = 0.115   # share of the canvas covered by ink after scaling


def to_ink(path):
    rgba = np.asarray(Image.open(path).convert('RGBA')).astype(np.float32)
    rgb, alpha = rgba[..., :3], rgba[..., 3] / 255.0
    lum = rgb @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)

    # Background: the logo's opaque border colour if it has one, otherwise white.
    edge_lum = np.concatenate([lum[0], lum[-1], lum[:, 0], lum[:, -1]])
    edge_alpha = np.concatenate([alpha[0], alpha[-1], alpha[:, 0], alpha[:, -1]])
    opaque = edge_lum[edge_alpha > 0.9]
    bg = float(np.median(opaque)) if opaque.size > edge_lum.size * 0.5 else 255.0
    bg = max(bg, 200.0)

    visible = alpha > 0.5
    darkest = float(np.percentile(lum[visible], 3)) if visible.any() else 0.0
    t = np.clip((bg - 8.0 - lum) / max(bg - 8.0 - darkest, 1.0), 0.0, 1.0) ** 0.85
    return t * alpha


def place(ink):
    ys, xs = np.where(ink > 0.04)
    ink = ink[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    bh, bw = ink.shape
    coverage = float(ink.mean())
    scale = (TARGET_INK * W * H / (bw * bh * max(coverage, 0.02))) ** 0.5
    scale = min(scale, (W - 2 * PAD) / bw, (H - 2 * PAD) / bh)
    nw, nh = max(1, round(bw * scale)), max(1, round(bh * scale))
    mask = Image.fromarray((ink * 255).astype(np.uint8), 'L').resize((nw, nh), Image.LANCZOS)
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    black = Image.new('RGBA', (nw, nh), (0, 0, 0, 255))
    black.putalpha(mask)
    canvas.alpha_composite(black, ((W - nw) // 2, (H - nh) // 2))
    return canvas


def main(src, dst):
    dst.mkdir(parents=True, exist_ok=True)
    for path in sorted(p for p in src.iterdir() if p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp')):
        out = dst / f'{path.stem}.webp'
        place(to_ink(path)).save(out, 'WEBP', lossless=True, method=6)
        print(f'{path.stem:32s} {out.stat().st_size // 1024} KB')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(Path(sys.argv[1]), Path(sys.argv[2]))
