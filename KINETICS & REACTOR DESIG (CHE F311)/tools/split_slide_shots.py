#!/usr/bin/env python3
"""Split the Classroom-app slide screenshots in Slides/*.pdf into single-slide images.

Each page of these decks is a tablet screenshot (1620x2160) showing four slide
thumbnails in a fixed 2x2 grid on a white page.  This tool extracts the native
embedded PNG of every page (no PDF re-rendering losses), crops the four cells,
skips empty cells, upscales 2x with Lanczos for comfortable on-screen reading,
and saves the slides sequentially numbered (page-major, row-major) so the file
numbers match the slide numbers printed on the slides themselves.

Grid measured on the 1620x2160 screenshots (Ch3-krd, Ch4-_Krd):
  columns x = [153, 749) and [841, 1437)      (596 px wide)
  rows    y = [537, 1007) and [1430, 1900)    (470 px tall)

Usage:
    python3 tools/split_slide_shots.py <deck.pdf> <out-dir> [--start N]
"""
import io
import os
import sys

import numpy as np
import pymupdf
from PIL import Image

# (x0, y0, x1, y1) of each cell in the 1620x2160 screenshot, row-major
CELLS = [
    (153,  537,  749, 1007),
    (841,  537, 1437, 1007),
    (153, 1430,  749, 1900),
    (841, 1430, 1437, 1900),
]
BLANK_THRESHOLD = 0.995   # cell is skipped if this fraction of its pixels is near-white
SCALE = 2                 # lanczos upscale for readability


def cell_is_blank(arr):
    """arr: HxW grayscale array of the cell."""
    return (arr > 235).mean() > BLANK_THRESHOLD


def main():
    pdf, outdir = sys.argv[1], sys.argv[2]
    start = int(sys.argv[sys.argv.index('--start') + 1]) if '--start' in sys.argv else 1
    os.makedirs(outdir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(pdf))[0].split('-')[0].replace('_-', '-').replace('_', '-')
    doc = pymupdf.open(pdf)
    n = start - 1
    blanks = []
    for pno in range(len(doc)):
        page = doc[pno]
        xrefs = [im[0] for im in page.get_images(full=True)]
        if not xrefs:
            raise SystemExit(f'page {pno + 1}: no embedded image — unexpected layout')
        info = doc.extract_image(xrefs[0])
        img = Image.open(io.BytesIO(info['image'])).convert('RGB')
        if img.size != (1620, 2160):
            raise SystemExit(f'page {pno + 1}: embedded image {img.size}, expected (1620, 2160)')
        for (x0, y0, x1, y1) in CELLS:
            crop = img.crop((x0, y0, x1, y1))
            g = np.asarray(crop.convert('L'))
            if cell_is_blank(g):
                blanks.append((pno + 1, (x0, y0)))
                continue
            n += 1
            crop = crop.resize((crop.width * SCALE, crop.height * SCALE), Image.LANCZOS)
            crop.save(os.path.join(outdir, f'{stem}-slide-{n:02d}.jpg'), quality=88)
    print(f'{os.path.basename(pdf)}: wrote {n - start + 1} slides to {outdir}')
    if blanks:
        print(f'  skipped blank cells (page, cell-topleft): {blanks}')


if __name__ == '__main__':
    main()
