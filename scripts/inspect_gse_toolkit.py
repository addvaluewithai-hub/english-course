#!/usr/bin/env python3
"""Inspect public GSE Toolkit frontend assets for reproducible vocabulary data endpoints."""
from __future__ import annotations

import re
import urllib.parse
import urllib.request

PAGE = "https://www.english.com/gse/teacher-toolkit/user/vocabulary"
MAIN = "https://www.english.com/gse/teacher-toolkit/user/main.js"
UA = "Mozilla/5.0 curriculum-source-audit/1.0"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-GB,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=60) as response:
        data = response.read()
        print(f"FETCH {response.status} {response.geturl()} {len(data)} bytes {response.headers.get('content-type')}")
        return data


def show_context(text: str, token: str, limit: int = 25, radius: int = 700) -> None:
    start = 0
    count = 0
    lower = text.lower()
    needle = token.lower()
    while count < limit:
        idx = lower.find(needle, start)
        if idx < 0:
            break
        left = max(0, idx - radius)
        right = min(len(text), idx + len(token) + radius)
        snippet = text[left:right].replace("\n", " ")
        if any(marker in snippet.lower() for marker in ("$http", "url", "endpoint", "elastic", "service", "api", "vocabulary")):
            print(f"CONTEXT[{token}]", snippet)
            count += 1
        start = idx + len(token)


def main() -> None:
    html = fetch(PAGE).decode("utf-8", errors="replace")
    print("BASE_HREF", re.findall(r'<base[^>]+href=["\']([^"\']+)', html, flags=re.I))
    text = fetch(MAIN).decode("utf-8", errors="replace")

    urls = sorted(set(re.findall(r'https?://[^"\'\\\s)]+', text, flags=re.I)))
    print("HTTP_URLS")
    for url in urls:
        if any(k in url.lower() for k in ("english.com", "pearson", "elastic", "api")):
            print("URL", url[:1500])

    relative = sorted(set(re.findall(r'["\']([^"\']{1,250})["\']', text)))
    print("LIKELY_ENDPOINT_STRINGS")
    for value in relative:
        low = value.lower()
        if (value.startswith("/") or "http" in low) and any(k in low for k in ("vocab", "elastic", "api", "search", "export")):
            print("STRING", value)

    for token in (
        "VocabularyService",
        "vocabularyService",
        "coreVocabulary",
        "ElasticSearch",
        "$http",
        "searchVocabulary",
        "vocabulary/search",
        "vocabulary?",
        "export",
    ):
        show_context(text, token)


if __name__ == "__main__":
    main()
