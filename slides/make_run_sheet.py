#!/usr/bin/env python3
"""Build printable run sheets from the Marp decks.

Each deck's speaker notes live in HTML comments; this pairs them with their slide
number and title and writes a self-contained, print-optimised HTML page. Print it
(Ctrl+P) or open it on a second device while you present the PDF.

Usage:  python3 slides/make_run_sheet.py
"""

from __future__ import annotations

import html
import pathlib
import re

SLIDES = pathlib.Path(__file__).resolve().parent
OUT = SLIDES / "notes"

# Timing shown in each run sheet header.
#
# `handoff_before` is the slide number that the live notebook demo runs *before* —
# i.e. the last slide is the "watch out / your turn" hand-off, so the notebook runs
# immediately ahead of it. Adjust if you'd rather demo earlier in a block.
DECKS = [
    {
        "file": "odmlib_ws_intro.md",
        "title": "Introduction and Environment Setup",
        "timing": "20 min · segment 1 of 8",
        "handoff_before": None,
        "handoff_text": None,
    },
    {
        "file": "block1_read_explore.md",
        "title": "Block 1 — Read, Explore, and Report",
        "timing": "4 min slides · 9 min notebook · 2 min hand-off",
        "handoff_before": 5,
        "handoff_text": "01_read_explore/lecture_demo.ipynb",
    },
    {
        "file": "block2_create_define.md",
        "title": "Block 2 — Generate a Minimal Define-XML v2.1",
        "timing": "4 min slides · 9 min notebook · 2 min hand-off",
        "handoff_before": 6,
        "handoff_text": "02_create_define/lecture_demo.ipynb",
    },
    {
        "file": "block3_validate_check.md",
        "title": "Block 3 — Validate and Check",
        "timing": "4 min slides · 9 min notebook · 2 min hand-off",
        "handoff_before": 6,
        "handoff_text": "03_validate_check/lecture_demo.ipynb",
    },
    {
        "file": "odmlib_ws_conclusion.md",
        "title": "Q&A and Conclusion",
        "timing": "10 min · segment 8 of 8",
        "handoff_before": None,
        "handoff_text": None,
    },
]

CSS = """
:root { --ink:#31404b; --muted:#6b7b87; --rule:#d8dee3; --accent:#c26a3a; --bg:#fff; }
* { box-sizing:border-box; }
body { margin:0; padding:28px 34px; background:var(--bg); color:var(--ink);
       font-family:'Lato','Noto Sans',system-ui,sans-serif; font-size:11.5pt; line-height:1.45; }
header { border-bottom:3px solid var(--ink); padding-bottom:10px; margin-bottom:18px; }
h1 { font-size:17pt; margin:0 0 4px; font-weight:900; letter-spacing:-.01em; }
.timing { color:var(--muted); font-size:10.5pt; font-weight:700; }
.deck { color:var(--muted); font-size:9.5pt; font-family:'DejaVu Sans Mono',monospace; }
.slide { display:grid; grid-template-columns:52px 1fr; gap:0 14px;
         padding:10px 0; border-bottom:1px solid var(--rule); break-inside:avoid; }
.num { font-family:'DejaVu Sans Mono',monospace; font-size:10pt; font-weight:700;
       color:var(--muted); padding-top:2px; white-space:nowrap; }
.title { font-weight:900; font-size:12pt; margin-bottom:3px; }
.note { white-space:pre-wrap; color:#3d4c57; }
.note code, .title code { font-family:'DejaVu Sans Mono',monospace; font-size:.92em;
       background:#eef1f3; padding:0 3px; border-radius:2px; }
.nonote { color:var(--muted); font-style:italic; }
.handoff { grid-column:1 / -1; margin:8px 0 2px; padding:7px 11px; border-radius:3px;
           background:#fbf0e8; border-left:4px solid var(--accent);
           font-weight:900; font-size:11pt; color:#8a4520; break-inside:avoid; }
.handoff code { background:rgba(255,255,255,.65); }
footer { margin-top:20px; padding-top:9px; border-top:1px solid var(--rule);
         color:var(--muted); font-size:9.5pt; display:flex; justify-content:space-between; }
@media print {
  body { padding:0; font-size:10.5pt; }
  @page { margin:14mm 13mm; }
  header { position:running(head); }
}
"""


def parse_deck(path: pathlib.Path) -> list[dict]:
    """Return [{n, title, note}] for each slide in a Marp deck."""
    raw = path.read_text(encoding="utf-8")

    # Drop the YAML front matter, then split on slide separators.
    if raw.startswith("---"):
        raw = raw.split("\n---\n", 1)[1] if "\n---\n" in raw else raw
    chunks = raw.split("\n---\n")

    slides = []
    for i, chunk in enumerate(chunks, start=1):
        # Title: first ATX h1. Strip Marp directive comments first so they can't match.
        body = re.sub(r"<!--\s*_[a-z]+:.*?-->", "", chunk, flags=re.S)
        m = re.search(r"^#\s+(.+?)\s*$", body, flags=re.M)
        title = m.group(1) if m else "(no title)"

        # Speaker note: the multi-line HTML comment that is not a Marp directive.
        note = ""
        for c in re.findall(r"<!--(.*?)-->", chunk, flags=re.S):
            stripped = c.strip()
            if stripped.startswith("_") or "\n" not in stripped:
                continue  # Marp directive (_class:, _footer:, …), not a note
            note = stripped
            break

        slides.append({"n": i, "title": title, "note": note})
    return slides


def md_inline(text: str) -> str:
    """Escape, then honour `code` and **bold** so notes read the way they were written."""
    out = html.escape(text)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    return out


def render(deck: dict, slides: list[dict]) -> str:
    rows = []
    for s in slides:
        if deck["handoff_before"] == s["n"]:
            rows.append(
                f'<div class="handoff">▶ SWITCH TO THE NOTEBOOK — '
                f'<code>{html.escape(deck["handoff_text"])}</code> — then return for the last slide</div>'
            )
        note = (
            f'<div class="note">{md_inline(s["note"])}</div>'
            if s["note"]
            else '<div class="note nonote">no speaker note</div>'
        )
        rows.append(
            '<div class="slide">'
            f'<div class="num">{s["n"]}/{len(slides)}</div>'
            f'<div><div class="title">{md_inline(s["title"])}</div>{note}</div>'
            "</div>"
        )

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Run sheet — {html.escape(deck["title"])}</title>
<style>{CSS}</style></head>
<body>
<header>
  <h1>{html.escape(deck["title"])}</h1>
  <div class="timing">{html.escape(deck["timing"])}</div>
  <div class="deck">slides/{html.escape(deck["file"])} · {len(slides)} slides</div>
</header>
{"".join(rows)}
<footer><span>R/Pharma 2026 · Creating Define-XML Solutions Using Python and odmlib</span>
<span>Run sheet — not for sharing on screen</span></footer>
</body></html>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for deck in DECKS:
        src = SLIDES / deck["file"]
        if not src.exists():
            raise SystemExit(f"missing deck: {src}")
        slides = parse_deck(src)
        dest = OUT / f"{src.stem}_run_sheet.html"
        dest.write_text(render(deck, slides), encoding="utf-8")
        missing = sum(1 for s in slides if not s["note"])
        flag = f"  ({missing} without notes)" if missing else ""
        print(f"  {dest.relative_to(SLIDES.parent)}  —  {len(slides)} slides{flag}")


if __name__ == "__main__":
    main()
