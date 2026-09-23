#!/usr/bin/env python3
"""Probe the public GSE Toolkit vocabulary search API with a tiny C2 request."""
from __future__ import annotations

import json
import urllib.parse
import urllib.request

BASE = "https://www.english.com/gse/teacher-toolkit/user/api/v1/vocabulary/search"
TOOLKIT = "https://www.english.com/gse/teacher-toolkit/user/vocabulary"
UA = "Mozilla/5.0 curriculum-source-audit/1.0"


def fetch(label: str, params: dict[str, str]) -> None:
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "application/json, text/plain, */*",
            "Referer": TOOLKIT,
        },
    )
    print("\n===", label, "===")
    print("URL", url)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            raw = response.read()
            print("STATUS", response.status)
            print("FINAL_URL", response.geturl())
            print("CONTENT_TYPE", response.headers.get("content-type"))
            print("X_TOTAL_COUNT", response.headers.get("x-total-count"))
            print("CONTENT_RANGE", response.headers.get("content-range"))
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        print("HTTP_ERROR", exc.code, exc.reason)
        print("BODY_PREFIX", raw[:1500].decode("utf-8", errors="replace"))
        return
    except Exception as exc:
        print("ERROR", repr(exc))
        return

    print("BYTES", len(raw))
    text = raw.decode("utf-8", errors="replace")
    print("BODY_PREFIX", text[:1500])
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        print("JSON_ERROR", repr(exc))
        return

    print("TOP_TYPE", type(data).__name__)
    if isinstance(data, dict):
        print("TOP_KEYS", sorted(data.keys()))
        for key in ("count", "total", "totalCount", "hits", "data"):
            if key in data:
                value = data[key]
                if isinstance(value, list):
                    print(key.upper(), "list", len(value))
                    if value:
                        print(
                            "FIRST_ITEM_KEYS",
                            sorted(value[0].keys()) if isinstance(value[0], dict) else type(value[0]).__name__,
                        )
                        print("FIRST_ITEM", json.dumps(value[0], ensure_ascii=False)[:3000])
                else:
                    print(
                        key.upper(),
                        value if not isinstance(value, (dict, list)) else type(value).__name__,
                    )
    elif isinstance(data, list):
        print("LIST_LEN", len(data))
        if data:
            print(
                "FIRST_ITEM_KEYS",
                sorted(data[0].keys()) if isinstance(data[0], dict) else type(data[0]).__name__,
            )
            print("FIRST_ITEM", json.dumps(data[0], ensure_ascii=False)[:3000])


def main() -> None:
    print("TOOLKIT", TOOLKIT)
    print("TARGET_GSE_RANGE", "85-90", "CEFR", "C2")
    filters = {
        "gseRange": {"from": "85", "to": "90"},
        "topics": [],
        "audiences": ["GL"],
        "grammaticalCategories": [],
    }
    fetch(
        "angular-json-filter",
        {
            "page": "1",
            "size": "3",
            "sort": "gse",
            "query_string": "*",
            "filters": json.dumps(filters, separators=(",", ":")),
        },
    )
    fetch(
        "bracket-filter",
        {
            "page": "1",
            "size": "3",
            "sort": "gse",
            "query_string": "*",
            "filters[gseRange][from]": "85",
            "filters[gseRange][to]": "90",
            "filters[audiences][]": "GL",
        },
    )
    fetch(
        "unfiltered-small-control",
        {
            "page": "1",
            "size": "1",
            "sort": "gse",
            "query_string": "*",
        },
    )


if __name__ == "__main__":
    main()
