#!/usr/bin/env python3
"""Build docs/index.html for GitHub Pages from index.html.

index.html is also the source of the Claude Artifact, which is written without
<!doctype>, <head> or <body> (the Artifact host adds them). This script adds them
so the same page works as a standalone file on GitHub Pages.

Usage: python3 tools/build_pages.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = '<div class="page">'

src = (ROOT / "index.html").read_text(encoding="utf-8")
head, sep, body = src.partition(MARKER)
if not sep:
    raise SystemExit(f"marker {MARKER!r} not found in index.html")
head = head.replace('<meta charset="utf-8">', "").strip()

page = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
{head}
</head>
<body>
{sep}{body.strip()}
</body>
</html>
"""
out = ROOT / "docs" / "index.html"
out.write_text(page, encoding="utf-8")
print(f"wrote {out.relative_to(ROOT)} ({len(page):,} chars)")
