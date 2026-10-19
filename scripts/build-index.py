#!/usr/bin/env python3
"""Rebuild index.html from issues.json. Python standard library only.

GitHub Pages serves the committed index.html. There is no build on Pages.
Run this script and commit the result whenever issues.json changes.
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "issues.json"
INDEX = ROOT / "index.html"

TEMPLATE = """\
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>@@TITLE@@</title>
<meta name="description" content="@@DESCRIPTION@@">
<style>
:root{--paper:#FFF1E5;--card:#F2DFCE;--rule:#CCC1B7;--ink:#33302E;--muted:#66605C;--claret:#990F3D;--oxford:#0F5499;--teal:#0D7680;
--serif:Georgia,'Times New Roman',Times,serif;--sans:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;
--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:18px/1.6 var(--serif);text-rendering:optimizeLegibility;-webkit-font-smoothing:antialiased}
.wrap{max-width:1180px;margin:0 auto;padding:0 32px}
.skip{position:absolute;left:-9999px;top:8px;background:var(--ink);color:#fff;padding:8px 12px;font:600 14px var(--sans);z-index:10}
.skip:focus{left:8px}
a{color:inherit;text-decoration:none}
a:focus-visible{outline:3px solid var(--oxford);outline-offset:2px;border-radius:2px}
.topbar{border-bottom:1px solid var(--rule)}
.topbar .wrap{display:flex;justify-content:space-between;align-items:center;height:48px;font:600 13px/1 var(--sans);letter-spacing:.08em;text-transform:uppercase}
.brand{font:700 20px/1 var(--serif);letter-spacing:0;text-transform:none}
.edition{color:var(--muted)}
.masthead{border-bottom:1px solid var(--rule);padding:48px 0 36px}
.eyebrow{margin:0 0 14px;font:600 14px/1 var(--sans);color:var(--claret);letter-spacing:.02em}
h1{margin:0 0 18px;font:400 clamp(36px,6vw,64px)/1.05 var(--serif);letter-spacing:-.015em;max-width:14em}
.standfirst{margin:0 0 20px;font:400 clamp(19px,2.2vw,23px)/1.45 var(--serif);color:var(--ink);max-width:62ch}
.dateline{margin:0;font:14px/1.4 var(--sans);color:var(--muted);padding-top:14px;border-top:1px solid var(--rule);display:inline-block}
.dateline em{font-style:normal}
main{padding:12px 32px 64px}
.section{margin-top:44px}
.section-label{margin:0 0 24px;padding-top:12px;border-top:4px solid var(--ink);font:700 15px/1.2 var(--sans);letter-spacing:.06em;text-transform:uppercase;color:var(--ink)}
.story{padding:0 0 28px;margin:0 0 28px;border-bottom:1px solid var(--rule);max-width:70ch}
.story h3{margin:0 0 8px;font:400 24px/1.25 var(--serif);letter-spacing:-.005em}
.story h3 a{background-image:linear-gradient(currentColor,currentColor);background-size:0 1px;background-repeat:no-repeat;background-position:0 100%;transition:color .15s,background-size .2s}
.story h3 a:hover,.story h3 a:focus-visible{color:var(--claret);background-size:100% 1px}
.kicker{margin:0 0 10px;font:600 12px/1 var(--sans);color:var(--claret);letter-spacing:.08em;text-transform:uppercase}
.meta{margin:0 0 12px;font:14px/1.4 var(--sans);color:var(--muted);display:flex;flex-wrap:wrap;gap:6px}
.who{font-weight:600;color:var(--ink)}
.story p{margin:0 0 14px}
.story.lead{max-width:none;padding-bottom:36px;margin-bottom:36px}
.story.lead h3{font-size:clamp(28px,3.6vw,40px);line-height:1.12;letter-spacing:-.01em;max-width:16em}
.story.lead > p.dek{font-size:19px;max-width:66ch}
.pick{margin:44px 0 0;background:var(--card);border-top:4px solid var(--claret);padding:28px 32px 30px}
.pick .section-label{border-top:0;padding-top:0;color:var(--claret);margin-bottom:14px}
.pick p{margin:0;font:400 clamp(19px,2vw,22px)/1.5 var(--serif);max-width:68ch}
.foot{border-top:1px solid var(--rule);padding:24px 0 40px;font:14px/1.5 var(--sans);color:var(--muted)}
.foot em{font-style:normal}
@media (min-width:900px){
 .front{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:0 48px;align-items:start}
 .front .pick{margin-top:44px}
}
@media (max-width:600px){
 body{font-size:17px}
 .wrap,main{padding-left:18px;padding-right:18px}
 .masthead{padding:32px 0 28px}
 .story h3{font-size:21px}
 .story.lead h3{font-size:clamp(26px,8vw,32px)}
 .pick{padding:22px 20px;margin-left:-18px;margin-right:-18px}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style></head><body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><span class="brand">@@TITLE@@</span><span class="edition">Weekly</span></div></div>
<header class="masthead"><div class="wrap">
<p class="eyebrow">@@EYEBROW@@</p>
<h1>@@TITLE@@</h1>
<p class="standfirst">@@TAGLINE@@</p>
<p class="dateline"><em>@@DATELINE@@</em></p>
</div></header>
<main id="main" class="wrap">
<div class="front">
<section class="section" aria-labelledby="issues"><h2 class="section-label" id="issues">Issues</h2>
<!-- BEGIN issues: generated from issues.json by scripts/build-index.py. Newest first. -->
@@ISSUES@@
<!-- END issues -->
</section>
<aside class="pick" aria-labelledby="about"><h2 class="section-label" id="about">About</h2>
<p>New issues land on Saturday. Each one is a Bookmark Digest: the posts Vinay saved on X that week, and why they matter.</p>
</aside>
</div>
</main>
<footer class="foot"><div class="wrap"><em>@@TITLE@@ · Bookmark Digest, published weekly.</em></div></footer>
</body></html>
"""


def fail(message: str) -> None:
    print(f"build-index: {message}", file=sys.stderr)
    raise SystemExit(1)


def issue_slug(number: int) -> str:
    return f"issue-{number:02d}"


def render_issue(issue: dict, lead: bool) -> str:
    number = issue["number"]
    slug = issue_slug(number)
    href = f"issues/{slug}.html"
    title = html.escape(issue["title"])
    coverage = html.escape(issue["coverage"])
    klass = "story lead" if lead else "story"
    meta = f'<span class="who">{coverage}</span>'
    if "bookmarks" in issue:
        meta += f'<span class="sep" aria-hidden="true">·</span><span>{int(issue["bookmarks"])} bookmarks</span>'
    dek = ""
    if issue.get("dek"):
        dek = f'\n<p class="dek">{html.escape(issue["dek"])}</p>'
    return (
        f'<article class="{klass}">\n'
        f'<p class="kicker">Issue #{number}</p>\n'
        f'<h3><a href="{href}">{title}</a></h3>\n'
        f'<p class="meta">{meta}</p>'
        f"{dek}\n"
        f"</article>"
    )


def load_issues(data: dict) -> list[dict]:
    raw = data.get("issues")
    if not isinstance(raw, list):
        fail("issues.json needs an 'issues' array")
    seen: set[int] = set()
    issues: list[dict] = []
    for i, issue in enumerate(raw):
        if not isinstance(issue, dict):
            fail(f"issues[{i}] must be an object")
        number = issue.get("number")
        if isinstance(number, bool) or not isinstance(number, int) or number < 1:
            fail(f"issues[{i}].number must be a positive integer")
        if number in seen:
            fail(f"duplicate issue number {number}")
        seen.add(number)
        title = issue.get("title")
        coverage = issue.get("coverage")
        if not isinstance(title, str) or not title.strip():
            fail(f"issues[{i}].title must be a non-empty string")
        if not isinstance(coverage, str) or not coverage.strip():
            fail(f"issues[{i}].coverage must be a non-empty string")
        dek = issue.get("dek", "")
        if not isinstance(dek, str):
            fail(f"issues[{i}].dek must be a string")
        bookmarks = issue.get("bookmarks")
        if bookmarks is not None and (isinstance(bookmarks, bool) or not isinstance(bookmarks, int) or bookmarks < 0):
            fail(f"issues[{i}].bookmarks must be a non-negative integer")
        slug = issue_slug(number)
        html_path = ROOT / "issues" / f"{slug}.html"
        md_path = ROOT / "issues" / f"{slug}.md"
        if not html_path.is_file():
            fail(f"missing {html_path.relative_to(ROOT)} for issue {number}")
        if not md_path.is_file():
            fail(f"missing {md_path.relative_to(ROOT)} for issue {number}")
        issues.append(issue)
    issues.sort(key=lambda item: item["number"], reverse=True)
    return issues


def render(data: dict, issues: list[dict]) -> str:
    for key in ("title", "eyebrow", "tagline"):
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            fail(f"{key} must be a non-empty string")
    if issues:
        body = "\n".join(render_issue(issue, lead=(index == 0)) for index, issue in enumerate(issues))
        dateline = f'Latest · {html.escape(issues[0]["coverage"])}'
    else:
        body = '<p class="dek">No issues yet.</p>'
        dateline = "No issues yet"
    return (
        TEMPLATE.replace("@@TITLE@@", html.escape(data["title"]))
        .replace("@@DESCRIPTION@@", html.escape(data["tagline"]))
        .replace("@@EYEBROW@@", html.escape(data["eyebrow"]))
        .replace("@@TAGLINE@@", html.escape(data["tagline"]))
        .replace("@@DATELINE@@", dateline)
        .replace("@@ISSUES@@", body)
    )


def main() -> None:
    check = "--check" in sys.argv[1:]
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail("issues.json not found")
    except json.JSONDecodeError as exc:
        fail(f"issues.json is not valid JSON: {exc}")
    if not isinstance(data, dict):
        fail("issues.json must be an object")
    page = render(data, load_issues(data))
    if check:
        current = INDEX.read_text(encoding="utf-8") if INDEX.is_file() else ""
        if current != page:
            fail("index.html is out of date. Run: python3 scripts/build-index.py")
        print("index.html is up to date")
        return
    INDEX.write_text(page, encoding="utf-8")
    count = len(data["issues"])
    noun = "issue" if count == 1 else "issues"
    print(f"wrote index.html ({count} {noun})")


if __name__ == "__main__":
    main()
