# Demo — defineutils and Other Command-Line Tools

Everything you built by hand in Blocks 1–3 — metrics, schema validation, ref/def checking —
exists productized as command-line tools. defineutils is a set of Define-XML utilities built
on odmlib: install with pip, run with `python -m`, wire into CI with meaningful exit codes.

This is the payoff message of the workshop: odmlib is not just a library you script against;
it's the engine under a growing ecosystem of tools, and after Blocks 1–3 you can read — and
build — tools like these yourself.

## The five defineutils commands

| Command | What it does |
|---------|--------------|
| `python -m defineutils.metrics -d define.xml` | Describe a define.xml: study info, standards, element counts, per-dataset variable table |
| `python -m defineutils.validate -d define.xml` | XSD schema validation — reports *every* error, grouped into distinct findings with line numbers |
| `python -m defineutils.definerefs -d define.xml` | OID reference/definition integrity: dangling refs, duplicate OIDs, orphan definitions, leaf/ArchiveLocation checks |
| `python -m defineutils.definehtml -d define.xml -o define.html` | Render the browsable HTML view using the standard Define-XML stylesheet |
| `python -m defineutils.definepp -d define.xml -o pretty.xml` | Byte-careful pretty-print: re-indents while preserving comments, namespaces, and content |

Useful flags across the commands: `-o` to write a report file, `--json` for machine-readable
output, `-L 0` to list *all* error locations (default caps the list), `--errors-only`
(definerefs), `--permissive` for best-effort runs on broken files, `-s` to supply an
alternate schema (validate).

**CI-friendly exit codes:** `validate` and `definerefs` exit 0 when clean, 1 with findings,
2 if the check could not run — so a define.xml quality gate in CI is a two-line job.

Sound familiar? `metrics` is Block 1's exercise, `validate` is Block 3 layer 1, `definerefs`
is Block 3 layer 2 — each wrapped in argparse with reporting. That's the odmlib development
experience: the distance from "notebook exercise" to "useful tool" is short.

## The wider odmlib ecosystem

All built on the same library and idioms you just learned:

- **gendefine** — generate Define-XML v2.1 from metadata spreadsheets via configurable JSON
  mappings. <https://github.com/swhume/gendefine>
- **odmlib_examples / odmlib_snippets** — runnable example programs and reference snippets.
  <https://github.com/swhume/odmlib_examples>

## Demo notebook

`defineutils_demo.ipynb` runs all five commands against the workshop data — the MSG example,
the minimal DM define from Block 2, and the broken files from Block 3 — from shell cells you
can rerun anytime.
