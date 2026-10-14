#!/usr/bin/env bash
# GA2 Q1 - the seven HTTPBin captures.  Tag: http-80e8dcf7   Quantity: 10   Status: 422
#
# IMPORTANT: paste these lines into the shell INSIDE `termlog rec httpbin.cast`.
# Do not run this file as a script. The grader reads the *recorded commands* as well as the
# outputs, and `bash q01_httpbin.sh` records only that one line. REDIRECT fails that way,
# because following /redirect-to returns byte-identical JSON to calling /get directly, so the
# command text is the only proof of how it was fetched.

capture() { task="$1"; shift; printf '\nHTTPBIN_BEGIN http-80e8dcf7 %s\n' "$task"; "$@"; printf '\nHTTPBIN_END http-80e8dcf7 %s\n' "$task"; }

capture GET curl -sS -H 'X-Exam-Tag: http-80e8dcf7' 'https://httpbin.org/get?course=TDS&tag=http-80e8dcf7'

capture POST curl -sS -X POST https://httpbin.org/post -H 'Content-Type: application/json' -d '{"tag":"http-80e8dcf7","quantity":10,"active":true}'

capture FORM curl -sS -X PUT https://httpbin.org/put -d tag=http-80e8dcf7 -d quantity=10

capture AUTH curl -sS -H 'Authorization: Bearer http-80e8dcf7' https://httpbin.org/bearer

capture REDIRECT curl -sS --location 'https://httpbin.org/redirect-to?url=https%3A%2F%2Fhttpbin.org%2Fget%3Ftag%3Dhttp-80e8dcf7'

curl -sS --cookie-jar jar.txt --output /dev/null 'https://httpbin.org/cookies/set?exam=http-80e8dcf7'
capture COOKIES curl -sS --cookie jar.txt https://httpbin.org/cookies

capture STATUS curl -sS --output /dev/null --write-out '%{http_code}\n' https://httpbin.org/status/422
