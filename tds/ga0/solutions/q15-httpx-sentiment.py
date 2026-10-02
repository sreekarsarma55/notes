import httpx

TEXT = "5Zj3G 4HTa9 9F4FxQ jThMKFwixCXZJoWXN JVVst1C5N4Lpg"

response = httpx.post(
    "https://api.openai.com/v1/chat/completions",
    headers={"Authorization": "Bearer dummy-api-key"},
    json={
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "Analyze the sentiment of the text the user sends. "
                           "Classify it as exactly one of: GOOD, BAD, or NEUTRAL.",
            },
            {"role": "user", "content": TEXT},
        ],
    },
)
response.raise_for_status()
print(response.json()["choices"][0]["message"]["content"])
