#!/usr/bin/env bash
# GA2 Q1 - the seven HTTPBin captures. Run these INSIDE `termlog rec httpbin.cast`.
# Tag: http-80e8dcf7   Quantity: 10   Status: 422

capture() { task="$1"; shift; printf '\nHTTPBIN_BEGIN http-80e8dcf7 %s\n' "$task"; "$@"; printf '\nHTTPBIN_END http-80e8dcf7 %s\n' "$task"; }

capture GET curl -sS -H 'X-Exam-Tag: http-80e8dcf7' 'https://httpbin.org/get?course=TDS&tag=http-80e8dcf7'

capture POST curl -sS -X POST https://httpbin.org/post -H 'Content-Type: application/json' -d '{"tag":"http-80e8dcf7","quantity":10,"active":true}'

capture FORM curl -sS -X PUT https://httpbin.org/put -d tag=http-80e8dcf7 -d quantity=10

capture AUTH curl -sS -H 'Authorization: Bearer http-80e8dcf7' https://httpbin.org/bearer

capture REDIRECT curl -sSL -G https://httpbin.org/redirect-to --data-urlencode 'url=https://httpbin.org/get?tag=http-80e8dcf7'

curl -sS -c jar.txt -o /dev/null 'https://httpbin.org/cookies/set?exam=http-80e8dcf7'
capture COOKIES curl -sS -b jar.txt https://httpbin.org/cookies

capture STATUS curl -sS -o /dev/null -w '%{http_code}\n' https://httpbin.org/status/422
