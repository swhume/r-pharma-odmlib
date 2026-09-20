# Live Demo Prompts — the odmlib Skill in Claude Code

Scripted prompts for the 10-minute demo. Run Claude Code in a scratch directory containing a
copy of `data/define_dm_example.xml` (and with the odmlib skill installed — see
`lecture_notes.md`). The point of each prompt is noted, plus what to highlight in the
assistant's behavior.

---

## Prompt 1 — the skill triggers without naming odmlib

> Read define_dm_example.xml and print a summary of each dataset: name, structure, and its
> variables with their data types.

**Watch for:** odmlib is never mentioned in the prompt. The skill triggers on the domain
(a define.xml). The generated code uses `XMLDefineLoader(model_package="define_2_1")` — the
non-default model package a from-memory model routinely gets wrong — and navigates
`odm.Study.MetaDataVersion` without `[0]`.

## Prompt 2 — modify and validate

> Add a RACE variable to the DM dataset in define_dm_example.xml: text, length 20, collected,
> with the CDISC RACE codelist values White, Black or African American, Asian, and Other.
> Write the result to define_dm_race.xml.

**Watch for:** the skill's working loop in action — the assistant builds the `ItemDef`,
`ItemRef`, and `CodeList` as objects, then **validates before writing** (fresh
`create_oid_checker("define_2_1")`, `validate(collect_errors=True, ...)`) without being asked,
and XSD-validates the output file. Open the written file: correct namespaces, schema order,
resolved references.

## Prompt 3 — an analysis task

> Which variables in define_dm_example.xml have no Origin? Write a short script that reports
> them.

**Watch for:** `find()`-style navigation instead of hand-written XML parsing; a runnable
script as the deliverable.

## Prompt 4 (if time) — the repair loop

> This define.xml fails its reference checks. Find and fix the problems, and show me the
> validation output proving it's clean. Use define_broken_refs.xml.

(Copy `data/define_broken_refs.xml` into the scratch directory first.) **Watch for:** the
Block 3 workflow, reproduced by the assistant: `verify_oids` → fix the dangling ref → *then*
`unreferenced_oids` for the orphan → re-validate to an empty error list → write.

---

## The contrast (30 seconds, slides or terminal)

The same Prompt 2 asked of a model **without** the skill typically yields hand-rolled
`xml.etree.ElementTree` with string-built namespaces, no ordering discipline, and no
validation — code that produces a file which *looks* like Define-XML and fails at the first
real check. The skill is the difference between plausible and correct.

## Talking points while code generates

- The skill is ~480 lines of Markdown plus references and examples — no fine-tuning, no
  retrieval infrastructure; a text file that any team can write for their own library.
- It ships *with* odmlib, so its API reference tracks the installed version (it targets
  0.2.1+ and documents the 0.2.0 → 0.2.1 differences).
- Everything the assistant just did — the load idiom, the validation layers, the repair
  order — is exactly what you did by hand in Blocks 1–3. The skill encodes this workshop.
