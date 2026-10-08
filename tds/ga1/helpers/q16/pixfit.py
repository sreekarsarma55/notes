"""Pixel-level refinement: rasterise candidate layouts like the target and minimise the XOR with it.

The target svg_path is a traced raster, so comparing at the pixel level is the fairest test. Coordinate
descent over each piece's (X, Y) within +/-R ticks (orientation fixed), repeated until nothing improves.
Writes the best layouts (several solutions' starting points) to refined.json for the exact key check.
"""
import itertools
import json
import math
import re
import sys

import numpy as np
from PIL import Image, ImageDraw

from solve import PIECES, rotated

W, H = 768, 576
R2 = math.sqrt(2)
verts = {p[0]: p[1] for p in PIECES}


def target_mask():
    t = open("target.txt").read()
    path = re.search(r'svg_path:"([^"]+)"', t).group(1)
    img = Image.new("1", (W, H), 0)
    d = ImageDraw.Draw(img)
    for sub in path.split("Z"):
        pts = [tuple(map(float, m)) for m in re.findall(r"(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)", sub)]
        if len(pts) >= 3:
            d.polygon(pts, fill=1)
    return np.array(img, dtype=bool)


def piece_pts(pose):
    out = []
    for x, y in verts[pose["id"]]:
        rx, ry = rotated(x, y, pose["orientation"], pose["reflected"])
        out.append((2 * (rx[0] + rx[1] * R2 + pose["x"]), 2 * (ry[0] + ry[1] * R2 + pose["y"])))
    return out


def mask(state):
    img = Image.new("1", (W, H), 0)
    d = ImageDraw.Draw(img)
    for pose in state:
        d.polygon(piece_pts(pose), fill=1)
    return np.array(img, dtype=bool)


def score(state, T):
    return int(np.count_nonzero(mask(state) ^ T))


def refine(state, T, R=4):
    best = score(state, T)
    improved = True
    while improved:
        improved = False
        for i in range(len(state)):
            x0, y0 = state[i]["x"], state[i]["y"]
            for dx, dy in itertools.product(range(-R, R + 1), repeat=2):
                state[i]["x"], state[i]["y"] = x0 + dx, y0 + dy
                s = score(state, T)
                if s < best:
                    best, x0, y0, improved = s, x0 + dx, y0 + dy, True
            state[i]["x"], state[i]["y"] = x0, y0
    return state, best


if __name__ == "__main__":
    T = target_mask()
    sols = json.load(open("solutions.json"))
    results = []
    seen = set()
    for si, s in enumerate(sols):
        sig = tuple((p["id"], p["orientation"], p["reflected"]) for p in sorted(s, key=lambda p: p["id"]))
        if sig in seen:
            continue
        seen.add(sig)
        st, sc = refine([dict(p) for p in s], T)
        print(si, "xor px", sc, json.dumps(st))
        results.append({"solution": si, "xor": sc, "pieces": st})
    results.sort(key=lambda r: r["xor"])
    json.dump(results, open("refined.json", "w"))
