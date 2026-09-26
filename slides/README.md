# Slides

Marp decks (`marp: true`, `theme: gaia`). One deck per lecture segment:

| File | Segment | Slides |
|------|---------|--------|
| `odmlib_ws_intro.md` | 1 — Introduction and environment setup (20 min) | 16 |
| `block1_read_explore.md` | 2 — Block 1 lecture (15 min) | 5 |
| `block2_create_define.md` | 3 — Block 2 lecture (15 min) | 6 |
| `block3_validate_check.md` | 4 — Block 3 lecture (15 min) | 6 |
| `odmlib_ws_conclusion.md` | 8 — Q&A and conclusion (10 min) | 5 |

Each block lecture is **~4 min slides + ~9 min live notebook + ~2 min hand-off**.
The live notebook for each block is `<block_folder>/lecture_demo.ipynb`; the
slides carry the concepts, tables and gotchas, the notebook carries the code.

`lecture_notes.md` in each block folder stays the written reference — read it
during the exercise, not from the podium.

## Building

```bash
./slides/build.sh                      # all decks
./slides/build.sh block1_read_explore  # just one
```

Produces:

- **`slides/pdf/*.pdf`** — what you present
- **`slides/notes/*_run_sheet.html`** — what you print or read on a second device

Needs Node (the script loads nvm automatically if it's installed) and a network
connection: the gaia theme fetches Lato and Roboto Mono at export time and they
get embedded into the PDF. Presenting needs neither. **Run the build the day
before, not five minutes before.**

Marp is not a Python package and is deliberately not in `requirements.txt` —
students never need it. For editing, the
[Marp VS Code extension](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
gives a live preview.

## Presenting

**Present from the PDF, not the browser.** The PDF has fonts embedded and carries
no browser chrome, tabs, URL bar, extension popups or Marp on-screen controller —
nothing but the slide reaches the recording.

- Open in a real presentation mode: **Evince `F5`**, **Okular `Ctrl+Shift+P`**, or
  `zathura`. Check arrow-key navigation and that the cursor auto-hides.
- **Share the whole of Display 1 in Zoom — not a single window.** The PDF and
  JupyterLab both live there, so alt-tabbing between deck and notebook never
  blacks out the audience. Single-window sharing is the classic failure mode for
  a live-coded virtual workshop.
- **Display 2 is never shared** — run sheet, Zoom chat, participant list, timer.
- Pre-flight Display 1: Do Not Disturb on, dock/taskbar hidden, other windows
  closed or moved to Display 2, JupyterLab font size raised and light theme set.

`--pdf-notes` is deliberately **not** used in the build: it embeds the speaker
notes as PDF annotations, which draws a note icon in the page corner that would
show on the recording. The run sheets carry the notes instead.

### If you'd rather use the browser

`npx @marp-team/marp-cli@latest slides/<deck>.md -o /tmp/<deck>.html`, then `f`
for fullscreen and `p` for presenter view. Viable, just second choice. Its fonts
come from `fonts.bunny.net` at page load; Lato is installed locally but Roboto
Mono is not, so offline the code blocks fall back to DejaVu Sans Mono. That
fallback was rendered and checked — it is cosmetic, and no slide clips.

## Editing notes

- Speaker notes are HTML comments (`<!-- ... -->`) — they are stripped from the
  slides and collected into the run sheets.
- Gaia overflows silently: content that doesn't fit is **clipped**, not shrunk.
  After editing, re-render to PNG and *look* at the slide — several of these need
  a `<style scoped>` block to fit. Keep at most one such block per slide.

  ```bash
  npx @marp-team/marp-cli@latest --images png slides/block1_read_explore.md
  ```

- The notebook hand-off point printed in each run sheet is set by
  `handoff_before` in `make_run_sheet.py`. It currently assumes the demo runs
  just before the final "watch out / your turn" slide.

## Virtual delivery

This deck set assumes a virtual workshop: questions go to the chat, setup triage
happens in the chat with a breakout room for anyone still stuck, and there is no
"wave if you're lost".
