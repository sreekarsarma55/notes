// Exact search over every (orientation, reflected, X, Y) that reproduces each piece's approximate footprint.
// Different poses can draw the same polygon but land on different exact lattices (sqrt2 parts), so the
// true layout may need a "different" pose than the one the approximate solver chose.
// usage: node variants.mjs <solutionIndex> <tolPx>
import fs from "node:fs";
import { webcrypto } from "node:crypto"; if (!globalThis.crypto) globalThis.crypto = webcrypto;
import { TANGRAM_CONFIG as C, tangramAdapter as A, tangramPolygons } from "./games/tangram/adapter.js";
import { computeMatchKey } from "./visual/kernel.js";

const target = fs.readFileSync("../target.txt", "utf8").match(/expected_match_key:"([0-9a-f]+)"/)[1];
const sols = JSON.parse(fs.readFileSync("../solutions.json", "utf8"));
const si = Number(process.argv[2] ?? 0), TOL = Number(process.argv[3] ?? 2.5);
const order = C.inventory.map(p => p.id);
const base = { pieces: order.map(id => ({ ...sols[si].find(p => p.id === id) })) };
const R2 = Math.SQRT2;
const toPx = v => [2 * (Number(v.x.a) + Number(v.x.b) * R2), 2 * (Number(v.y.a) + Number(v.y.b) * R2)];

function polyOf(pose) {
  const st = structuredClone(base);
  const i = order.indexOf(pose.id);
  st.pieces[i] = { ...pose };
  return tangramPolygons(st, C)[i].vertices.map(toPx);
}
const sortPts = pts => [...pts].sort((a, b) => a[0] - b[0] || a[1] - b[1]);

// candidate poses per piece
const cands = base.pieces.map(p => {
  const ref = sortPts(polyOf(p));
  const out = [];
  for (let o = 0; o < 8; o++) for (const r of [false, true]) {
    const at0 = sortPts(polyOf({ ...p, x: 0, y: 0, orientation: o, reflected: r }));
    // translation that best maps at0 onto ref, if the shapes are congruent in this pose
    const dx = (ref[0][0] - at0[0][0]) / 2, dy = (ref[0][1] - at0[0][1]) / 2;
    for (let X = Math.floor(dx) - 1; X <= Math.ceil(dx) + 1; X++) for (let Y = Math.floor(dy) - 1; Y <= Math.ceil(dy) + 1; Y++) {
      if (X < 0 || Y < 0 || X > 384 || Y > 288) continue;
      const pose = { id: p.id, x: X, y: Y, orientation: o, reflected: r };
      const pts = sortPts(polyOf(pose));
      const err = Math.max(...pts.map((q, k) => Math.hypot(q[0] - ref[k][0], q[1] - ref[k][1])));
      if (err <= TOL) out.push({ pose, pts: polyOf(pose), err });
    }
  }
  // de-duplicate identical polygons (same exact vertex set)
  const seen = new Map();
  for (const c of out) {
    const key = sortPts(c.pts).map(q => q.map(n => n.toFixed(6)).join(",")).join(";");
    if (!seen.has(key) || seen.get(key).err > c.err) seen.set(key, c);
  }
  return [...seen.values()].sort((a, b) => a.err - b.err);
});
console.log("candidates per piece:", cands.map((c, i) => order[i] + "=" + c.length).join(" "));

// float SAT strict-overlap test (touching allowed)
function overlap(a, b) {
  for (const poly of [a, b]) for (let i = 0; i < poly.length; i++) {
    const p = poly[i], q = poly[(i + 1) % poly.length];
    const ax = -(q[1] - p[1]), ay = q[0] - p[0];
    const pa = a.map(v => v[0] * ax + v[1] * ay), pb = b.map(v => v[0] * ax + v[1] * ay);
    if (Math.max(...pa) <= Math.min(...pb) + 1e-6 || Math.max(...pb) <= Math.min(...pa) + 1e-6) return false;
  }
  return true;
}
let tested = 0;
const chosen = [];
async function dfs(i) {
  if (i === 7) {
    tested++;
    const st = { pieces: chosen.map(c => c.pose) };
    if (A.validate(st, C).invalid) return false;
    if (await computeMatchKey(A, st, C) === target) {
      console.log("EXACT", JSON.stringify(st.pieces));
      fs.writeFileSync("../exact.json", JSON.stringify(st));
      return true;
    }
    return false;
  }
  for (const c of cands[i]) {
    if (chosen.some(d => overlap(d.pts, c.pts))) continue;
    chosen.push(c);
    if (await dfs(i + 1)) return true;
    chosen.pop();
  }
  return false;
}
const t0 = Date.now();
const ok = await dfs(0);
console.log(ok ? "found" : "not found", "full layouts tested:", tested, "secs", (Date.now() - t0) / 1000);
