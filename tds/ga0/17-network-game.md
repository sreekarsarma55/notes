# Q17 — Network Game: Graph Detective (1 mark)

## Problem

`https://tds-network-games.sanand.workers.dev/detective/` is a game played on a
120-node financial transaction graph. Using a **limited number of queries** (55), find
the compromised account and report the **shortest path** from your anchor node to
it. Winning returns a signed completion token (a JWT), which you submit.

The question says outright that *AI coding agents might help*.

## How it is actually graded

```text
JWT header.payload.signature, ES256 (P-256); JWKS key kid "tds-2025"
1. signature verifies against the game's public JWKS (embedded in q.js)
2. sub      == your email
3. game     == "detective"
4. week_id  == the CURRENT ISO week at the moment you press Check
5. completed_at within the last 7 days
```

Point 4 matters most: **a token only works during the ISO week it was earned in.**

## What we did and why

We played through the game's HTTP API with a small cached client
([`solutions/q17-game-client.py`](solutions/q17-game-client.py)) instead of clicking
through it. Every paid query is cached on disk, so a re-run never wastes budget.

```text
/start   → week 2026-W40, anchor node 3 (free), 55-query budget, three clues:
           • individual transaction sizes dwarf the rest of the network
           • moves huge sums out but almost never receives
           • surprisingly few counterparties for that much activity
/sample  → 20 random nodes: a BASELINE mean and std for every attribute
/node/id → one node's attributes and neighbours (costs 1 query)
```

**Scoring suspects:** each clue maps to one attribute, so we turned them into
z-scores against the baseline:

```text
suspicion = z(avg_tx_size) − z(in_out_ratio) − z(counterparty_count)
            big tx size      ↑ sends ≫ receives   ↓ few counterparties
```

**Search:** start at the anchor, query the neighbours most likely to lead somewhere,
and follow the suspicion score. This is a guided breadth-first search, not a sweep
of the whole graph. Node **40** scored far above everything else. The path we found
was **3 → 0 → 40**, and the game's own token reports `path_is_shortest: true`.

```text
result: score 836 · 9 queries used of 55 · 5 unique nodes · 0 wrong guesses
        path_is_shortest: true · play style "Clean Arrest"
```

Why it was done this way: a high score comes from few queries and a provably
shortest path. Turning the clues into a numeric score means we query only nodes
that could plausibly be the target.

## Verification

```text
decoded the JWT: sub = email, game = detective, week_id = 2026-W40
verified the ES256 signature against the JWKS in q.js (WebCrypto in Node)   valid
header: alg ES256; the JWKS has a single key, kid tds-2025
quiz                                                                    green
```

## Traps

| Trap | Detail |
|---|---|
| **The token expires with the week** | Earned in W40 means Check must happen in W40 (ends Mon 5 Oct 2026 05:29 IST, which is the end of Sunday in UTC). Later, replay the game for a new token. |
| **Wrong guesses cost points** | Gather evidence first and only submit a suspect once you're confident. |
| **Cloudflare blocks Python's default User-Agent** | `urllib` requests got error 1010. Send `User-Agent: curl/8.5.0`. |
| **Paste the JWT exactly** | Three dot-separated parts with no spaces or newlines. |
| **Don't publish the token** | It's tied to your email. These notes include the method, not the token. |
