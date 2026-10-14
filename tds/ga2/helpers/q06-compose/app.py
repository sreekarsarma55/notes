"""GA2 Q6 - FastAPI counter service backed by Redis INCR (runs as the `api` compose service)."""
import os

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")
r = redis.from_url(REDIS_URL, decode_responses=True)

app = FastAPI(title="TDS GA2 Q6 - compose + redis")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"],
                   allow_headers=["*"], expose_headers=["*"])


@app.post("/hit/{key}")
async def hit(key: str):
    """Atomic increment in Redis, so counts survive worker restarts and are shared by workers."""
    return {"key": key, "count": await r.incr(f"hits:{key}")}


@app.get("/count/{key}")
async def count(key: str):
    value = await r.get(f"hits:{key}")
    return {"key": key, "count": int(value or 0)}


@app.get("/healthz")
async def healthz():
    try:
        await r.ping()                      # really ping Redis, not a static response
    except Exception:
        return JSONResponse({"status": "error", "redis": "down"}, status_code=503)
    return {"status": "ok", "redis": "up"}


@app.get("/")
async def root():
    return {"status": "ok", "endpoints": ["POST /hit/{key}", "GET /count/{key}", "GET /healthz"]}
