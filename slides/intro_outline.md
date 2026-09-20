# Intro Slide Outline — Creating Define-XML Solutions Using Python and odmlib

Slide-by-slide outline with speaker notes for the 20-minute opening segment. Target ~15
slides; slides 12–15 run alongside the guided environment setup.

---

### 1. Title

**Creating Define-XML Solutions Using Python and odmlib** — R/Pharma 2026. Presenter intro.

*Notes:* One sentence on the promise: "In three hours you'll read, create, validate, repair,
and extend Define-XML v2.1 — and leave with tools and AI workflows you can use Monday."

### 2. Agenda and how the workshop works

The 8-segment agenda with timings. Repo layout: each block has a folder with
`lecture_notes.md` + an exercise notebook; completed notebooks in `solutions/`.

*Notes:* Set the rhythm expectation: short lecture → 20-minute hands-on exercise → 5-minute
solution review, three times; then three 10-minute demos. Exercises have working cells plus
marked TODOs; lecture notes contain everything needed to complete them.

### 3. What is Define-XML (one-slide refresher)

The machine-readable data definitions for a submission: datasets, variables, codelists,
derivations, value-level metadata, documents. Required by FDA/PMDA for SDTM/SEND/ADaM data.

*Notes:* Calibrate to the room — many R/Pharma attendees know define.xml as "that XML file";
emphasize it's a graph of cross-referenced metadata, which is why tooling matters.

### 4. What is odmlib

An open-source (MIT) Python library implementing the CDISC ODM family as complete,
schema-aware object models. Load → navigate → modify → validate → serialize. On PyPI:
`pip install odmlib`.

*Notes:* Positioning: not an XML helper — a model of the standard. Every element a class,
every attribute typed, references checkable.

### 5. One library, the whole ODM family

Supported standards table: ODM 1.3.2 · ODM 2.0 (draft) · Define-XML 2.0 / **2.1** · ARM 1.0
· Dataset-XML 1.0.1 · CT-XML 1.1.1 · Dataset-JSON 1.1.

*Notes:* Today is Define-XML-focused, but the idioms transfer 1:1 — Block 1's stretch loads
an ARM define with a two-line change. Dataset-JSON support connects to last year's R/Pharma
workshop topic.

### 6. Why not hand-roll the XML?

A slide with a small "hand-rolled" ElementTree snippet vs the odmlib equivalent. Hand-rolled
must manage: 4 namespaces, strict element order, dozens of required attributes, OID
cross-reference integrity — and fails silently.

*Notes:* Key line: "Hand-rolling Define-XML is how subtle, expensive errors get made. odmlib
makes the correct way the easy way."

### 7. Where odmlib is used

Ecosystem/adoption examples: defineutils (Define-XML CLI utilities),
gendefine, odmlib_examples/odmlib_snippets. Community users and internal pipelines.

*Notes:* Personalize with 1–2 real adoption stories. The tools demo (segment 7) shows several
of these live.

### 8. The odmlib development loop

Diagram: **load / build → modify → validate (4 layers) → serialize** — with the four layers
named: XSD schema · OID ref/def · conformance · element order.

*Notes:* This loop is the workshop's spine: Block 1 = load, Block 2 = build/serialize,
Block 3 = validate/repair. Validation-first is the habit to leave with.

### 9. What's new in odmlib 0.2.1

Collect-*all*-errors validation (`collect_errors=True`, `max_errors`) · `to_element()` for
ElementTree interop · ARM 1.0 XSD bundled (+ correct ARM serialization order) · Define-XML
`leaf`/`leafID`/`ArchiveLocationID` reference checks · the odmlib Claude Code skill.

*Notes:* Message: an actively developed project with a real roadmap, not an abandoned parser.

### 10. AI-assisted odmlib development (preview)

The odmlib skill: curated instructions + API reference + runnable examples that load into an
AI coding assistant. Demo in segment 6.

*Notes:* One line to plant the idea: "Generic AI writes plausible CDISC code; the skill makes
it write *correct* odmlib code — and validate it."

### 11. What you'll build today

Concrete outcomes: a metadata report from a 179-variable MSG define.xml (Block 1) · a
schema-valid define.xml from scratch (Block 2) · a repaired broken define, validated clean
(Block 3) · plus extension, AI, and CLI-tools demos.

*Notes:* Reassure on level: intermediate Python is plenty; all CDISC specifics are provided.

### 12. Environment setup — start now

The four commands (clone, venv, `pip install -r requirements.txt`, `jupyter lab`) and the
repo URL. Points at `00_setup/setup_instructions.md`.

*Notes:* Have everyone start installs while the remaining slides play. Mention VS Code /
PyCharm alternatives.

### 13. Verify your setup

`00_setup/verify_setup.ipynb` → Run All → "✅ You are ready for Block 1".

*Notes:* Helpers circulate. Common fixes are in the troubleshooting appendix of the setup
instructions (python3 vs python, Windows activation policy, proxy).

### 14. Meet the data

The MSG example define.xml (11 datasets, 179 variables, 40 codelists) + the deliberately
broken variants used in Block 3 (each hides a different class of error).

*Notes:* Realistic, submission-shaped metadata — not toy files; that's why the numbers
students compute in Block 1 are worth putting on a slide later.

### 15. Ground rules and Q&A buffer

Questions anytime; exercises are self-paced with stretch goals for fast finishers; solutions
folder is not cheating — it's the safety net. Segue into Block 1 lecture.

*Notes:* Flex slide — absorb setup overruns here; cut if on time.
