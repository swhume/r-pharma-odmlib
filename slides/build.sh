#!/usr/bin/env bash
#
# Build the presentation artifacts for the R/Pharma 2026 workshop.
#
#   slides/pdf/*.pdf                    what you present (fonts embedded, no chrome)
#   slides/notes/*_run_sheet.html       what you print / read on a second device
#
# Needs Node (for npx) and a network connection: the gaia theme fetches Lato and
# Roboto Mono at export time, and they get embedded into the PDF. Presenting needs
# neither. Run this the day before, not five minutes before.
#
# Usage:  ./slides/build.sh  [deck-name ...]     (default: all four decks)

set -euo pipefail

cd "$(dirname "$0")/.."

MARP=(npx --yes @marp-team/marp-cli@latest)
DECKS=("${@:-}")
if [ -z "${DECKS[0]:-}" ]; then
    DECKS=(odmlib_ws_intro block1_read_explore block2_create_define block3_validate_check)
fi

# npx usually isn't on PATH in a non-interactive shell when Node came from nvm.
if ! command -v npx >/dev/null 2>&1 && [ -s "$HOME/.nvm/nvm.sh" ]; then
    # shellcheck disable=SC1091
    . "$HOME/.nvm/nvm.sh" >/dev/null 2>&1 || true
fi
command -v npx >/dev/null 2>&1 || {
    echo "error: npx not found. Install Node, or load nvm first:" >&2
    echo "       source \"\$HOME/.nvm/nvm.sh\" && nvm use --lts" >&2
    exit 1
}

mkdir -p slides/pdf

echo "Building PDFs..."
for deck in "${DECKS[@]}"; do
    src="slides/${deck}.md"
    [ -f "$src" ] || { echo "error: no such deck: $src" >&2; exit 1; }

    # --pdf-outlines adds per-slide bookmarks (handy for jumping during Q&A).
    # Deliberately NOT --pdf-notes: that embeds the notes as annotations, which
    # draws a note icon in the page corner that would show on the recording.
    "${MARP[@]}" --pdf --pdf-outlines "$src" -o "slides/pdf/${deck}.pdf" >/dev/null
    printf '  slides/pdf/%-30s %s\n' "${deck}.pdf" "$(du -h "slides/pdf/${deck}.pdf" | cut -f1)"
done

echo "Building run sheets..."
python3 slides/make_run_sheet.py

echo
echo "Done. Present from slides/pdf/ in your viewer's presentation mode"
echo "(Evince F5 · Okular Ctrl+Shift+P). Run sheets are in slides/notes/."
