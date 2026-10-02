# Q18 — Local Ollama Endpoint (3 marks)

## Problem

Run Ollama on your own machine, expose it on the internet with **ngrok**, and make
every response carry an `X-Email: <your email>` header. Submit the ngrok URL.

## How it is actually graded

```text
1. hostname contains "ngrok"
2. fetch(`${url}/api/version`, { headers: {"ngrok-skip-browser-warning": true} })
   — from YOUR BROWSER, so cross-origin CORS rules apply
3. body JSON has a "version" field           → Ollama is really behind the tunnel
4. response.headers.get("x-email") === your email
```

It looks simple, but four separate things each have to be right.

## What we did and why

**Terminal 1 — Ollama with CORS open:**

```bash
export OLLAMA_ORIGINS="*"     # must be EXPORTED in the shell that runs ollama serve
ollama serve
```

**Terminal 2 — ngrok with a traffic policy**
([`solutions/q18-ngrok-policy.yml`](solutions/q18-ngrok-policy.yml)):

```yaml
on_http_request:
  - actions:
      - type: add-headers
        config: { headers: { host: "localhost:11434" } }
on_http_response:
  - actions:
      - type: add-headers
        config:
          headers:
            x-email: "23f3002028@ds.study.iitm.ac.in"
            access-control-expose-headers: "*"
            access-control-allow-headers: "Authorization,Content-Type,User-Agent,Accept,Ngrok-skip-browser-warning"
```

```bash
ngrok http 11434 --traffic-policy-file ~/ngrok-policy.yml
```

Why each line is there. Each one fixes a failure we either saw or reproduced:

| Line | Problem it solves |
|---|---|
| `OLLAMA_ORIGINS="*"` (exported) | Ollama rejects browser origins it doesn't know. The first try set it without `export`, so `ollama serve` never saw it. |
| `host: localhost:11434` | Ollama only accepts its own Host header (DNS-rebinding protection). Through ngrok the Host is `*.ngrok-free.dev`, which gets rejected. |
| `x-email` | The header the grader actually checks. |
| `access-control-expose-headers: *` | Cross-origin JavaScript can read only a few "safelisted" headers. Without this, `headers.get("x-email")` returns `null` even though the header was sent. |
| `access-control-allow-headers: …ngrok-skip-browser-warning` | The grader sends a custom header, so the browser sends a CORS **preflight** first, and that has to allow the header. |
| Traffic policy, not `--response-header-add` | The old flag is deprecated and splits values on commas, which gave `ERROR: Malformed header: Content-Type`. |

Submitted: `https://ambiance-cough-handclasp.ngrok-free.dev` (your URL will be
different).

## Verification

```text
curl through the tunnel                                     version 0.11.4, x-email present
Playwright: replayed the grader's exact fetch from a
different origin in headless Chrome                         PASS, JS sees x-email
quiz                                                        green
```

## Traps

| Trap | Detail |
|---|---|
| **Both processes must stay up until Saved** | Closing the laptop or the terminal ends the tunnel. A free-plan URL may change on restart. |
| **curl passing doesn't mean the browser passes** | curl ignores CORS. Test from a browser page on another origin. |
| **Placeholder URLs** | Copy the real `Forwarding` URL ngrok prints. A literal `YOUR-URL` gives HTTP 421. |
| **The ngrok interstitial page** | Free ngrok shows a warning page to browsers unless `ngrok-skip-browser-warning` is sent. The grader sends it; your own tests should too. |
