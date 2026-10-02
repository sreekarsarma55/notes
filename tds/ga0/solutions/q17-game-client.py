"""Cached client + anomaly scorer for the TDS 'Graph Detective' game.

Every call that spends budget is cached on disk, so re-running never wastes a query.
usage: python3 game.py 12 40 7      # query those node ids, print scored summaries
"""
import json
import os
import sys
import urllib.request

BASE = "https://tds-network-games.sanand.workers.dev/detective"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "nodes.json")
TOKEN = open(os.path.join(HERE, "token.txt")).read().strip()

# baseline from the game's own /sample call (20-node sample)
BASELINE = {"in_out_ratio": (1.04, 0.12), "counterparty_count": (9.15, 2.71),
            "avg_tx_size": (212.7, 186.35), "tx_volume_daily": (2244.3, 2669.45),
            "tx_count_daily": (13.8, 2.86), "dormancy_days": (3.6, 1.5), "jurisdictions": (1.75, 0.94)}


def load():
    return json.load(open(CACHE)) if os.path.exists(CACHE) else {}


def call(path, method="GET", body=None):
    req = urllib.request.Request(BASE + path, method=method, headers={"X-Session-Token": TOKEN, "Content-Type": "application/json", "User-Agent": "curl/8.5.0", "Accept": "*/*"},
                                 data=json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"_error": e.code, "_body": e.read().decode()[:300]}


def query(nid, cache):
    if str(nid) in cache:
        return cache[str(nid)], False
    d = call(f"/node/{nid}")
    if "_error" in d:
        raise SystemExit(f"node {nid}: {d}")
    cache[str(nid)] = d
    json.dump(cache, open(CACHE, "w"))
    return d, True


def z(attr, value):
    m, s = BASELINE[attr]
    return (value - m) / s if s else 0.0


def summary(d):
    a = d["attributes"]
    return (f"node {d['id']:>3} deg={d['degree']:>2} ratio={a['in_out_ratio']:<5} cpty={a['counterparty_count']:<3} "
            f"avg_tx={a['avg_tx_size']:<6} vol={a['tx_volume_daily']:<6} cnt={a['tx_count_daily']:<3} "
            f"dorm={a['dormancy_days']:<3} jur={a['jurisdictions']}")


def suspicion(d):
    """High when the three clues all point the same way: huge avg_tx, tiny in/out ratio, few counterparties."""
    a = d["attributes"]
    return z("avg_tx_size", a["avg_tx_size"]) - z("in_out_ratio", a["in_out_ratio"]) - z("counterparty_count", a["counterparty_count"])


if __name__ == "__main__":
    cache = load()
    for arg in sys.argv[1:]:
        d, spent = query(int(arg), cache)
        print(("*" if spent else " "), summary(d), f"| suspicion {suspicion(d):+.1f}")
    print(f"\nqueried so far: {len(cache)} nodes cached (anchor 3 came free with /start)")
