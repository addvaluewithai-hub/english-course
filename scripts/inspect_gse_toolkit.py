#!/usr/bin/env python3
"""Inspect public GSE Toolkit frontend assets for reproducible vocabulary data endpoints."""
from __future__ import annotations

import re
import urllib.parse
import urllib.request

PAGE = "https://www.english.com/gse/teacher-toolkit/user/vocabulary"
UA = "Mozilla/5.0 curriculum-source-audit/1.0"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-GB,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=60) as response:
        data = response.read()
        print(f"FETCH {response.status} {response.geturl()} {len(data)} bytes {response.headers.get('content-type')}")
        return data


def main() -> None:
    html = fetch(PAGE).decode("utf-8", errors="replace")
    print("PAGE_PREFIX", html[:500].replace("\n", " "))
    srcs = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html, flags=re.I)
    print("SCRIPT_COUNT", len(srcs))
    print("SCRIPTS", srcs)

    patterns = [
        re.compile(r'https?://[^"\'\s)]+', re.I),
        re.compile(r'["\']([^"\']*(?:api|vocab|download|search)[^"\']*)["\']', re.I),
    ]
    seen: set[str] = set()
    for src in srcs[:30]:
        url = urllib.parse.urljoin(PAGE, src)
        try:
            text = fetch(url).decode("utf-8", errors="replace")
        except Exception as exc:
            print("SCRIPT_ERROR", url, repr(exc))
            continue
        print("SCRIPT", url)
        matches: list[str] = []
        for pattern in patterns:
            for match in pattern.finditer(text):
                value = match.group(1) if match.lastindex else match.group(0)
                if value in seen:
                    continue
                seen.add(value)
                lower = value.lower()
                if any(key in lower for key in ("vocab", "/api", "download", "search", "graphql")):
                    matches.append(value)
                if len(matches) >= 100:
                    break
            if len(matches) >= 100:
                break
        for value in matches:
            print("MATCH", value[:1000])


if __name__ == "__main__":
    main()
