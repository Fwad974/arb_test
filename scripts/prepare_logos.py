#!/usr/bin/env python3
"""Turn client logo files into clean, full-colour, optically balanced WebP files.

    pip install pillow numpy
    python3 scripts/prepare_logos.py SOURCE_DIR assets/images/clients

Each source file is named <slug>.png / .jpg / .webp (the slug used in content.py).
Every output is <slug>.webp on a 360x160 transparent canvas, in the logo's own colours:

- A plain light box behind a logo (white, cream, light grey) disappears: the background
  colour is read from the image's border and removed where it touches the border, with
  soft, anti-aliased edges. White details inside a mark (text in a coloured ellipse, a
  white stripe) stay, because they do not touch the border.
- Size is optical: each logo is scaled so it covers about the same area, then centred,
  so a sparse dotted mark and a heavy wordmark look equally weighted.
- --match DIR places each logo in the box its namesake in DIR occupies instead, so
  replacing a set keeps every logo exactly where it was (used to turn the earlier
  monochrome set into colour).
- --mono makes the earlier monochrome set instead: black ink only, contrast normalised
  per logo (the site no longer uses it).

The site shows the logos in full colour; in dark mode each sits on a white tile, so dark
wordmarks stay legible and brand colours stay true. Only build.py's standard library is
needed to build the site; this script is just for preparing new logos.
"""
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

W, H, PAD = 360, 160, 6
TARGET_INK = 0.115   # share of the canvas covered by ink after scaling (monochrome)
TARGET_AREA = 0.30   # share of the canvas covered by the logo after scaling (colour)
BG_TOLERANCE = 30    # how far (0-255, per channel) a pixel may be from the box colour


def load(path, longest=1200):
    im = Image.open(path).convert('RGBA')
    if max(im.size) > longest:
        im.thumbnail((longest, longest), Image.LANCZOS)
    return im


def to_ink(path):
    """Monochrome: how much darker each pixel is than the logo's background, 0..1."""
    rgba = np.asarray(load(path)).astype(np.float32)
    rgb, alpha = rgba[..., :3], rgba[..., 3] / 255.0
    lum = rgb @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    edge_lum = np.concatenate([lum[0], lum[-1], lum[:, 0], lum[:, -1]])
    edge_alpha = np.concatenate([alpha[0], alpha[-1], alpha[:, 0], alpha[:, -1]])
    opaque = edge_lum[edge_alpha > 0.9]
    bg = float(np.median(opaque)) if opaque.size > edge_lum.size * 0.5 else 255.0
    bg = max(bg, 200.0)
    visible = alpha > 0.5
    darkest = float(np.percentile(lum[visible], 3)) if visible.any() else 0.0
    t = np.clip((bg - 8.0 - lum) / max(bg - 8.0 - darkest, 1.0), 0.0, 1.0) ** 0.85
    return t * alpha


def border_region(candidate):
    """Pixels of the boolean mask `candidate` connected to the image border (4-connected)."""
    h, w = candidate.shape
    seen = np.zeros_like(candidate)
    queue = deque()
    for x in range(w):
        for y in (0, h - 1):
            if candidate[y, x] and not seen[y, x]:
                seen[y, x] = True
                queue.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if candidate[y, x] and not seen[y, x]:
                seen[y, x] = True
                queue.append((y, x))
    while queue:
        y, x = queue.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and candidate[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                queue.append((ny, nx))
    return seen


def colour_to_alpha(rgb, bg):
    """Remove the colour bg from pixels (GIMP's colour-to-alpha): returns (rgb, alpha 0..1)."""
    up = (rgb - bg) / np.maximum(255.0 - bg, 1.0)
    down = (bg - rgb) / np.maximum(bg, 1.0)
    a = np.where(rgb > bg, up, down).max(axis=-1).clip(0.0, 1.0)
    out = np.where(a[..., None] > 1e-3, (rgb - bg) / np.maximum(a[..., None], 1e-3) + bg, rgb)
    return out.clip(0.0, 255.0), a


def to_colour(path):
    """Colour: the logo with any plain light box behind it made transparent."""
    rgba = np.asarray(load(path)).astype(np.float32)
    rgb, alpha = rgba[..., :3].copy(), rgba[..., 3] / 255.0
    edge = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
    edge_alpha = np.concatenate([alpha[0], alpha[-1], alpha[:, 0], alpha[:, -1]])
    opaque = edge[edge_alpha > 0.9]
    if opaque.shape[0] > edge.shape[0] * 0.5:
        bg = np.median(opaque, axis=0)
        if bg.mean() > 200:
            near = (np.abs(rgb - bg).max(axis=-1) <= BG_TOLERANCE) & (alpha > 0.5)
            region = border_region(near)
            # the anti-aliased edge just outside the removed box
            grown = np.asarray(Image.fromarray(region.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(7))) > 0
            ring = grown & ~region
            new_rgb, a = colour_to_alpha(rgb[ring], bg)
            rgb[ring] = new_rgb
            alpha[ring] = alpha[ring] * a
            alpha[region] = 0.0
    return Image.fromarray(np.dstack([rgb, alpha * 255.0]).round().astype(np.uint8), 'RGBA')


def trim(im, threshold=10):
    box = Image.fromarray((np.asarray(im)[..., 3] > threshold).astype(np.uint8) * 255).getbbox()
    return im.crop(box)


def place_colour(im, box=None):
    """Scale onto the 360x160 canvas: into `box` (x0, y0, x1, y1) if given, else optically."""
    im = trim(im)
    bw, bh = im.size
    if box:
        x0, y0, x1, y1 = box
        scale = min((x1 - x0) / bw, (y1 - y0) / bh)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    else:
        coverage = float((np.asarray(im)[..., 3] / 255.0).mean())
        scale = (TARGET_AREA * W * H / (bw * bh * max(coverage, 0.05))) ** 0.5
        scale = min(scale, (W - 2 * PAD) / bw, (H - 2 * PAD) / bh)
        cx, cy = W / 2, H / 2
    nw, nh = max(1, round(bw * scale)), max(1, round(bh * scale))
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(im.resize((nw, nh), Image.LANCZOS), (round(cx - nw / 2), round(cy - nh / 2)))
    return canvas


def place_mono(ink):
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


def main(argv):
    mono = '--mono' in argv
    match = None
    if '--match' in argv:
        i = argv.index('--match')
        match = Path(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    args = [a for a in argv if not a.startswith('--')]
    if len(args) != 2:
        sys.exit(__doc__)
    src, dst = Path(args[0]), Path(args[1])
    dst.mkdir(parents=True, exist_ok=True)
    for path in sorted(p for p in src.iterdir() if p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp')):
        out = dst / f'{path.stem}.webp'
        if mono:
            logo = place_mono(to_ink(path))
        else:
            box = None
            if match and (match / f'{path.stem}.webp').exists():
                box = Image.open(match / f'{path.stem}.webp').convert('RGBA').getchannel('A').point(lambda v: 255 if v > 10 else 0).getbbox()
            logo = place_colour(to_colour(path), box)
        logo.save(out, 'WEBP', lossless=True, method=6)
        print(f'{path.stem:32s} {out.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main(sys.argv[1:])
