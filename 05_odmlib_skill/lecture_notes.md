# Demo — The odmlib Skill with Generative AI

Generative AI writes plausible code. For a niche, precision-critical domain like CDISC
standards, plausible isn't enough: a model working from memory will hand-roll XML, guess at
API names, index `Study[0]` in a Define-XML file, or skip validation entirely — and the
result *looks* fine until a reviewer or a gateway rejects it.

A **skill** fixes this. A skill is a package of curated instructions and reference material
that an AI coding assistant (this demo uses Claude Code) loads automatically when a task
matches its domain. The odmlib skill ships with odmlib itself and teaches the assistant the
library's correct idioms, its gotchas, and — crucially — a validation-first working loop.

## What's in the odmlib skill

```
odmlib/.claude/skills/odmlib/
├── SKILL.md                  the core instructions (~480 lines)
├── references/
│   ├── api-reference.md      exact public API names and signatures
│   ├── models.md             model packages, ODM 1.3.2 vs 2.0, namespaces
│   ├── validation.md         the four layers, error collection, permissive mode
│   └── dataset-json.md       Dataset-JSON 1.1 + conversion helpers
└── examples/                 8 runnable scripts (create, load, validate, repair,
                              round-trip Define-XML, Dataset-JSON, OID reporting)
```

Highlights of `SKILL.md` — you'll recognize this workshop in it:

- **The core principle: don't hand-build the markup.** The skill's first instruction.
- **The things to watch for list**: `_content` for element text, singular `Study`/`MetaDataVersion` in
  Define-XML, the loader's `define_2_0` default, fresh OID checkers per document,
  `except OdmlibError` — the same gotchas from Blocks 1–3.
- **A working loop**: identify the standard → build with odmlib → validate until clean with
  a fresh OID checker → serialize → XSD-validate for submissions. The assistant doesn't
  just write code; it validates what it writes.

The bundled examples are safe to run from anywhere — they write to `./odmlib_skill_output/`
in the current directory, never into the skill itself.

## What the demo shows

Live, in Claude Code, using the prompts in `demo_prompts.md`:

1. A Define-XML task phrased naturally — *without* naming odmlib. The skill triggers on the
   domain (define.xml, study metadata), and the generated code uses the right library and
   the right idioms.
2. The generated code follows the same patterns you just learned: explicit
   `model_package="define_2_1"`, one `root()` reference, `validate(collect_errors=True, ...)`
   with a fresh checker — and it runs the validation without being asked.
3. The contrast: what a model without the skill typically produces (hand-rolled
   `xml.etree` and string templates, no validation).

## Install the skill yourself

The skill lives in the odmlib repository and is included in the odmlib distribution. For
Claude Code:

```bash
# clone odmlib, then make the skill visible to Claude Code - either per-project:
mkdir -p .claude/skills
cp -r path/to/odmlib/.claude/skills/odmlib .claude/skills/

# or globally for your user:
mkdir -p ~/.claude/skills
cp -r path/to/odmlib/.claude/skills/odmlib ~/.claude/skills/
```

There is also a packaged single-file bundle (`odmlib.skill`) alongside the skill directory in
the odmlib repo. Skills are plain Markdown + example files — open `SKILL.md` and read it; it
doubles as a compact odmlib best-practices guide, and the format is easy to imitate for your
own in-house libraries.

## Related: AI beyond the skill

The skill teaches an assistant to *write odmlib code*. The **define-mcp-server** project
(see the tools demo) goes further: it exposes Define-XML operations directly to AI agents via
the Model Context Protocol — an agent can query and manipulate a define.xml without writing
code at all. Skill + MCP server sketch the two ends of AI-assisted standards work.
