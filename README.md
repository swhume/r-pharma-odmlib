# Creating Define-XML Solutions Using Python and odmlib

Hands-on workshop — **R/Pharma 2026**

Learn to read, create, validate, repair, and extend CDISC Define-XML v2.1 documents in Python
using [odmlib](https://github.com/swhume/odmlib) — plus how to pair odmlib with generative AI
and the command-line tools built on it. Three hours, Jupyter-based, intermediate Python
assumed (no prior odmlib experience needed).

## Quick start

```bash
git clone https://github.com/swhume/r-pharma-odmlib.git
cd r-pharma-odmlib
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

Then open `00_setup/verify_setup.ipynb` and run all cells. Full instructions (including VS
Code/PyCharm alternatives and troubleshooting): [`00_setup/setup_instructions.md`](00_setup/setup_instructions.md).

## Agenda

| # | Segment | Time |
|---|---------|------|
| 1 | Introduction and environment setup | 20 min |
| 2 | **Block 1** — Read, explore, and report on a Define-XML v2.1 | 40 min |
| 3 | **Block 2** — Generate a minimal Define-XML v2.1 | 40 min |
| 4 | **Block 3** — Schema validation, ref/def checks, and conformance | 40 min |
| 5 | Demo — Extending the Define-XML model | 10 min |
| 6 | Demo — The odmlib skill with generative AI | 10 min |
| 7 | Demo — defineutils and other command-line tools | 10 min |
| 8 | Q&A and conclusion | 10 min |

Each block: a short lecture, a ~20-minute hands-on exercise, and a solution review.

## How to use this repository

- Each numbered folder is one workshop segment, containing **`lecture_notes.md`** (background
  and worked examples — everything needed for the exercise) and a **notebook**.
- Exercise notebooks (blocks 1–3) mix working cells with `# YOUR CODE HERE` TODOs sized for
  ~20 minutes, plus an optional stretch goal.
- **`solutions/`** holds completed, executed versions of the three exercise notebooks.
- Demo notebooks (segments 5 and 7) are fully runnable — replay them anytime.
- **`data/`** contains the sample define.xml files (see [`data/README.md`](data/README.md)),
  including deliberately broken ones for the validation block.

```
00_setup/               setup instructions + environment check
01_read_explore/        Block 1: load, navigate, find, report
02_create_define/       Block 2: build a define.xml from scratch
03_validate_check/      Block 3: four validation layers + repair workflow
04_extend_model/        Demo: vendor extensions of the Define-XML model
05_odmlib_skill/        Demo: AI-assisted odmlib development
06_defineutils_tools/   Demo: the odmlib-based CLI tool ecosystem
solutions/              completed exercise notebooks
data/                   sample Define-XML v2.1 files
slides/                 intro slide outline
```

## Requirements

- Python 3.10+ (3.12 recommended)
- [odmlib](https://pypi.org/project/odmlib/) ≥ 0.2.1,
  [defineutils](https://github.com/swhume/defineutils), JupyterLab — all installed by
  `pip install -r requirements.txt`

## Links

- odmlib: <https://github.com/swhume/odmlib> · docs: <https://swhume.github.io/odmlib>
- defineutils: <https://github.com/swhume/defineutils>
- odmlib examples: <https://github.com/swhume/odmlib_examples>
- CDISC Define-XML v2.1: <https://www.cdisc.org/standards/data-exchange/define-xml>

## License

MIT — see [LICENSE](LICENSE). Sample data provenance is documented in
[`data/README.md`](data/README.md).
