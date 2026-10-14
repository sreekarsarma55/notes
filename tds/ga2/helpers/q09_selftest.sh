#!/usr/bin/env bash
# GA2 Q9 self-test: replays exactly what the quiz grader does to your tunnelled Ollama.
# usage: bash q09_selftest.sh https://your-tunnel.trycloudflare.com/v1/chat/completions <model>
URL="$1"; MODEL="$2"
if [ -z "$URL" ] || [ -z "$MODEL" ]; then
  echo "usage: bash q09_selftest.sh <https://.../v1/chat/completions> <model>"; exit 1
fi
TOKEN="TK$(tr -dc 'A-F0-9' </dev/urandom | head -c 6)"
A=$((10 + RANDOM % 80)); B=$((10 + RANDOM % 80))

ask() {  # ask <prompt>
  curl -sS -m 120 "$URL" -H 'Content-Type: application/json' \
    -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":$1}],\"stream\":false,\"temperature\":0}"
}

echo "--- echo test (token $TOKEN)"
R1=$(ask "\"Output ONLY this exact token and nothing else: $TOKEN\"")
echo "$R1" | head -c 400; echo
echo "$R1" | grep -qi "$TOKEN" && echo "ECHO PASS" || echo "ECHO FAIL"

echo "--- arithmetic test ($A + $B = $((A+B)))"
R2=$(ask "\"What is $A + $B? Reply with only the number.\"")
echo "$R2" | head -c 400; echo
echo "$R2" | grep -q "$((A+B))" && echo "MATH PASS" || echo "MATH FAIL"

echo "--- CORS preflight (the grader runs in your browser, so this must succeed)"
curl -sS -m 30 -i -X OPTIONS "$URL" \
  -H 'Origin: https://exam.sanand.workers.dev' \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: content-type' | head -12
