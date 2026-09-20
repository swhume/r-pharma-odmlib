# Block 3 — Validate and Check a Define-XML v2.1

A define.xml that "looks right" can still be broken in ways that surface weeks later — at a
regulatory gateway, in a downstream tool, or in a reviewer's browser. Validation-first
development catches these problems at the moment they're introduced. odmlib gives you four
independent validation layers, each catching a class of problems the others can't:

| Layer | Catches | One-liner |
|-------|---------|-----------|
| 1. XSD schema | Structural violations: missing required attributes/elements, bad enumeration values, wrong element placement | `ODMSchemaValidator(...).validate_file(path)` |
| 2. OID ref/def | Dangling references, duplicate OIDs, orphan definitions | `odm.verify_oids(checker)` |
| 3. Conformance | Model-rule violations on the object tree (value sets, required fields) — works *before* you serialize | `odm.verify_conformance(MetadataSchema())` |
| 4. Element order | Children assigned out of schema order (matters for dict/JSON output and hygiene) | `odm.verify_order()` |

And one call that runs layers 2–4 together and collects **every** finding:
`odm.validate(collect_errors=True, ...)`.

## 1. XSD schema validation

The official Define-XML v2.1 schema ships inside odmlib — nothing to download, no paths to
configure:

```python
from odmlib.odm_parser import ODMSchemaValidator

validator = ODMSchemaValidator(standard="define", version="2.1")
validator.validate_file("output/define_dm.xml")     # silent on success, raises on failure
```

Both arguments are required — there is no default. Supported pairs include
`("odm", "1.3.2")`, `("define", "2.0")`, `("define", "2.1")`, and for ARM inside a v2.1
define, `("arm", "1.0-define2.1")`. A custom or extended schema plugs in with
`ODMSchemaValidator(xsd_file="path/to/schema.xsd")`.

For a *report* rather than an exception, enumerate the findings:

```python
for err in validator.xsd.iter_errors("bad_define.xml"):
    print(err.reason, "at", err.path)
```

## 2. OID reference/definition integrity

Everything in Define-XML is wired together by OID references — `ItemRef → ItemDef`,
`CodeListRef → CodeList`, `MethodOID → MethodDef`, `ArchiveLocationID → leaf`. XSD cannot
check these (to the schema, an OID is just a string). The OID checker can:

```python
from odmlib import create_oid_checker

checker = create_oid_checker("define_2_1")
odm.verify_oids(checker)          # raises OdmlibOIDError on dangling refs / duplicate OIDs
```

Orphans — definitions nothing references — are reported separately, because they're usually
lint rather than an error:

```python
orphans = odm.unreferenced_oids(create_oid_checker("define_2_1"))
# {} when clean; else {orphan OID: the ref attribute that would use it}
```

Two things to know:

- **Checkers are stateful and single-use.** They accumulate OIDs as they walk a document —
  create a fresh one per document (or call `checker.reset()`).
- **`unreferenced_oids()` verifies references first** — on a document that still has dangling
  refs it raises rather than reporting orphans. Fix the refs, then hunt orphans. That
  ordering *is* the repair workflow.

New in 0.2.1, the checker also validates Define-XML's document links: `leaf` IDs against
`def:ArchiveLocationID` and `DocumentRef/@leafID`.

## 3. Conformance checking

The conformance checker applies model rules (required fields, controlled value sets) to the
**object tree** — so it works on documents you built in memory and haven't serialized yet,
and on files loaded permissively:

```python
from odmlib.define_2_1.rules.metadata_schema import MetadataSchema

odm.verify_conformance(MetadataSchema())    # raises OdmlibConformanceError with details
```

## 4. Element order

```python
odm.verify_order()       # recursive - checks the whole tree, names the misordered element
element.reorder_object() # fixes that element in place (not recursive - fix what's flagged)
```

As you saw in Block 2: `write_xml()` always serializes in schema order anyway; the order
check keeps your object tree consistent for `validate()`, `to_dict()`, and `to_json()`.

## 5. The combined call — your default

```python
errors = odm.validate(
    collect_errors=True,
    oid_checker=create_oid_checker("define_2_1"),
    conformance_checker=MetadataSchema(),
)
if not errors:
    print("clean")
for err in errors:
    print(type(err).__name__, "-", err)
```

`collect_errors=True` returns a list with **every** finding across order, OID, and
conformance checks (as of 0.2.1 — earlier versions stopped after a few). An empty list means
clean. Filter by exception type (`OdmlibOIDError`, `OdmlibConformanceError`,
`OdmlibElementOrderError`) to group a report; `max_errors=N` caps a runaway list. Without
`collect_errors`, `validate()` is fail-fast — right for pipelines, where the exception *is*
the answer.

Note what the combined call does **not** include: XSD. Schema validation works on the
serialized file, the object checks work on the tree — you'll see in the exercise why you
want both.

## 6. Permissive mode: loading broken files on purpose

Strict loading rejects a file with, say, a missing required attribute — correct behavior,
unhelpful when your task is *repairing* that file. Permissive mode gets the file into
objects; validation then tells you everything wrong; you fix and re-validate:

```python
import odmlib

with odmlib.permissive():
    loader = LD.ODMLoader(DL.XMLDefineLoader(model_package="define_2_1"))
    loader.open_odm_document("nonconformant.xml")
    odm = loader.root()

errors = odm.validate(collect_errors=True, ...)   # what needs fixing
# ... fix the objects ...
errors = odm.validate(collect_errors=True, ...)   # until this is empty
```

Load permissively → collect errors → fix objects → re-validate to clean → write. That loop is
the heart of odmlib-based repair tools.

## 7. Beyond Define-XML

The same four layers with the same calls cover the whole family — swap the model package and
schema pair: `create_oid_checker("odm_1_3_2")` with `("odm", "1.3.2")` for ODM,
`create_oid_checker("arm_1_0")` with `("arm", "1.0-define2.1")` for ARM (whose XSD is bundled
as of 0.2.1).

## Things to watch out for

- Reusing an OID checker across documents — it's stateful; make a fresh one each time.
- Calling `unreferenced_oids()` on a document that still has dangling refs — it raises; fix
  refs first.
- Expecting `validate()` to schema-validate — XSD is a separate, file-level layer; run both.
- Fixing objects from `loader.MetaDataVersion()` while validating `loader.root()` — each call
  builds a fresh tree; keep one `root()` reference and navigate from it.
- Reading only the first error — use `collect_errors=True` and fix in bulk.

## Exercise

Open `validate_check_exercise.ipynb`. Working cells run all four layers against a known-clean
file; then the TODOs have you diagnose a schema-invalid file, repair a define with reference
errors until it validates clean, and discover why the object checks and XSD are both
necessary. The stretch repairs a non-conformant file via permissive mode. Budget ~20 minutes.
Completed version: `solutions/validate_check_solution.ipynb`.
