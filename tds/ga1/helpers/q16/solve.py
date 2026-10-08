"""Tangram solver for the TDS GA1 Q16 board.

Coordinates follow the game's adapter.js exactly: a pose is (x, y, orientation 0-7, reflected) with x, y
integer 1/16 units, and a rotated vertex is a + b*sqrt(2) in 1/16 units. The target silhouette is given in
pixels (32 px per unit = 2 px per 1/16 unit) and was traced from a raster, so it is off by ~1 px.

Search: the remaining uncovered region's top-left corner must be the top-left corner of the next piece
(the usual exact-cover ordering). Try every remaining piece/orientation there, keep placements that lie
inside the region, recurse. Candidate translations are rounded to the 1/16 grid with a +/-1 neighbourhood
to absorb the tracing error; exactness is then checked with the game's own match key (match.mjs).
"""
import itertools
import json
import math
import re
import sys

from shapely.geometry import Polygon
from shapely.ops import unary_union

R2 = math.sqrt(2)
PIECES = [  # id, local vertices (units), reflections that matter
    ("large-a", [(0, 0), (4, 0), (0, 4)], [False]),
    ("large-b", [(0, 0), (4, 0), (0, 4)], [False]),
    ("medium", [(-2, 0), (2, 0), (0, 2)], [False]),
    ("small-a", [(0, 0), (2, 0), (0, 2)], [False]),
    ("small-b", [(0, 0), (2, 0), (0, 2)], [False]),
    ("square", [(0, 0), (2, 0), (2, 2), (0, 2)], [False]),
    ("parallelogram", [(0, 0), (2, 0), (4, 2), (2, 2)], [False, True]),
]


def rotated(x, y, o, refl):
    """adapter.js rotatedLocal: returns ((a, b), (a, b)) meaning (a + b*sqrt2)/16 units."""
    if refl:
        x = -x
    return {
        0: ((16 * x, 0), (16 * y, 0)),
        1: ((0, 8 * (x - y)), (0, 8 * (x + y))),
        2: ((-16 * y, 0), (16 * x, 0)),
        3: ((0, -8 * (x + y)), (0, 8 * (x - y))),
        4: ((-16 * x, 0), (-16 * y, 0)),
        5: ((0, 8 * (y - x)), (0, -8 * (x + y))),
        6: ((16 * y, 0), (-16 * x, 0)),
        7: ((0, 8 * (x + y)), (0, 8 * (y - x))),
    }[o]


val = lambda ab: ab[0] + ab[1] * R2            # 1/16 units
px = lambda ab: 2 * val(ab)                    # pixels


def piece_poly(verts, o, refl, X, Y):
    pts = []
    for (x, y) in verts:
        rx, ry = rotated(x, y, o, refl)
        pts.append((px(rx) + 2 * X, px(ry) + 2 * Y))
    return Polygon(pts)


def local_anchor(verts, o, refl):
    """Top-most then left-most vertex of the rotated piece, in pixels relative to the pose origin."""
    pts = [(px(rotated(x, y, o, refl)[0]), px(rotated(x, y, o, refl)[1])) for x, y in verts]
    miny = min(p[1] for p in pts)
    return min((p for p in pts if p[1] <= miny + 0.5), key=lambda p: p[0])


def region_anchor(region):
    pts = []
    geoms = getattr(region, "geoms", [region])
    for g in geoms:
        pts += list(g.exterior.coords)
        for ring in g.interiors:
            pts += list(ring.coords)
    miny = min(p[1] for p in pts)
    return min((p for p in pts if p[1] <= miny + 3), key=lambda p: p[0])


def clean(g):
    return g.buffer(-1.6, join_style=2).buffer(1.6, join_style=2)


def solve(target, max_solutions=1):
    total = target.area
    sols = []

    def rec(region, remaining, placed):
        if len(sols) >= max_solutions:
            return
        if not remaining:
            if region.area < 0.03 * total:
                sols.append(list(placed))
            return
        if region.is_empty or region.area < 0.5 * 1024:
            return
        ax, ay = region_anchor(region)
        tried = set()
        for idx in remaining:
            pid, verts, refls = PIECES[idx]
            kind = tuple(verts)
            for o in range(8):
                for refl in refls:
                    lx, ly = local_anchor(verts, o, refl)
                    X0, Y0 = round((ax - lx) / 2), round((ay - ly) / 2)
                    for dX, dY in itertools.product((0, -1, 1), repeat=2):
                        X, Y = X0 + dX, Y0 + dY
                        key = (kind, o, refl, X, Y)
                        if key in tried or not (0 <= X <= 384 and 0 <= Y <= 288):
                            continue
                        tried.add(key)
                        P = piece_poly(verts, o, refl, X, Y)
                        outside = P.difference(region).area
                        if outside > 0.025 * P.area + 30:
                            continue
                        rest = [i for i in remaining if i != idx]
                        placed.append({"id": pid, "x": X, "y": Y, "orientation": o, "reflected": refl})
                        rec(clean(region.difference(P)), rest, placed)
                        placed.pop()
                        if len(sols) >= max_solutions:
                            return
                        break  # one grid neighbour per orientation is enough once it fits

    rec(target, list(range(len(PIECES))), [])
    return sols


if __name__ == "__main__":
    t = open(sys.argv[1]).read()
    path = re.search(r'svg_path:"([^"]+)"', t).group(1)
    rings = []
    for sub in path.split("Z"):
        pts = [tuple(map(float, m)) for m in re.findall(r"(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)", sub)]
        if len(pts) >= 3:
            rings.append(Polygon(pts))
    # even-odd fill: XOR the rings
    target = rings[0]
    for r in rings[1:]:
        target = target.symmetric_difference(r)
    sols = solve(target, max_solutions=int(sys.argv[2]) if len(sys.argv) > 2 else 20)
    json.dump(sols, open("solutions.json", "w"))
    print(len(sols), "approximate solutions")
    for s in sols[:3]:
        print(json.dumps(s))
