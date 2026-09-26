---
marp: true
theme: gaia
paginate: true
footer: 'R/Pharma 2026 · Creating Define-XML Solutions Using Python and odmlib'
---

<!-- _class: lead -->
<!-- _paginate: false -->
<!-- _footer: '' -->

# Block 3
## Schema Validation, Ref/Def Checks, Conformance

**15 min lecture · 20 min exercise · 5 min review**

<!--
Segment 4 of 8, and the payoff for the whole workshop. A define.xml that "looks
right" can be broken in ways that surface weeks later - at a gateway, in a
downstream tool, in a reviewer's browser. Validation-first catches them at the
moment they're introduced.
-->

---

# Four layers, four failure classes

<style scoped>
table { font-size: 0.62em; }
td:first-child { white-space: nowrap; }
</style>

| Layer | Catches | One-liner |
|---|---|---|
| **1. XSD schema** | Structural violations: missing required attributes or elements, bad enumeration values, wrong placement | `ODMSchemaValidator(...)`<br>`.validate_file(path)` |
| **2. OID ref/def** | Dangling references, duplicate OIDs, orphan definitions | `odm.verify_oids(checker)` |
| **3. Conformance** | Model-rule violations on the object tree — works *before* you serialize | `odm.verify_conformance(`<br>`MetadataSchema())` |
| **4. Element order** | Children assigned out of schema order — matters for dict/JSON output | `odm.verify_order()` |

**None of them subsumes another.** That's the lesson of this block.

<!--
Spend real time here - this is the most valuable slide in the workshop. Layer by
layer, say what each one sees that the others are blind to. To XSD an OID is just
a string, so it cannot check layer 2. Layer 3 works on objects you haven't
serialized yet, which XSD structurally cannot do. In the exercise you meet one
file that passes the object checks and fails only XSD, and another that does
exactly the reverse.
-->

---

# Your default call

<style scoped>
pre { font-size: 0.74em; }
p { font-size: 0.82em; }
p code { font-size: 0.9em; }
</style>

```python
errors = odm.validate(
    collect_errors=True,
    oid_checker=create_oid_checker("define_2_1"),
    conformance_checker=MetadataSchema(),
)
for err in errors:
    print(type(err).__name__, "-", err)
```

Runs layers **2 – 4** and collects **every** finding *(new in 0.2.1)*.
Empty list means clean. `max_errors=N` caps a runaway list.

Without `collect_errors` it's fail-fast — right for pipelines,
where the exception *is* the answer.

<!--
Filter by exception type - OdmlibOIDError, OdmlibConformanceError,
OdmlibElementOrderError - to group a report. Before 0.2.1 this stopped after a
few errors, so you fixed one, re-ran, found the next. Now you fix in bulk.
-->

---

# What `validate()` misses: XSD

<style scoped>
ul { font-size: 0.82em; }
p { font-size: 0.85em; }
pre { font-size: 0.72em; }
</style>

```text
   XSD            works on the serialized FILE
   layers 2-4     work on the object TREE
```

Deliberate, not an oversight — the object checks run on documents
you built in memory and **haven't written yet**.

You need **both**, and the exercise proves it:

- `define_broken_refs.xml` → passes XSD, **fails** layer 2
- `defineV21-SDTM-invalid-class.xml` → passes 2–4, **fails** XSD

<!--
This is the single most common misconception about odmlib validation - people run
validate(), see an empty list, and assume schema-valid. Say it plainly: validate()
plus validate_file(), every time.
-->

---

# The repair loop

<style scoped>
pre { font-size: 0.72em; }
</style>

```text
  with odmlib.permissive():        ← get a broken file into objects at all
      odm = load(path)
            │
            ▼
  odm.validate(collect_errors=True, ...)   ← everything wrong, one pass
            │
            ▼
  fix the objects                  ← ordinary attribute assignment
            │
            ▼
  re-validate  ──► empty?  ──► odm.write_xml(path)
```

Strict loading *rejects* a malformed file — correct, but useless
when your job is repairing it. **This loop is the heart of every
odmlib-based repair tool.**

<!--
Note the order inside the loop: fix dangling references BEFORE hunting orphans,
because unreferenced_oids() verifies references first and raises while any remain.
That ordering is the workflow, not a quirk. In ~20 lines the exercise builds the
essence of a Define-XML repair tool.
-->

---

# Watch out for these

<style scoped>
ul { font-size: 0.74em; line-height: 1.32; }
ul code { font-size: 0.88em; }
h3 { font-size: 0.82em; }
</style>

- **Reusing an OID checker across documents** — they're stateful and
  single-use. Fresh one each time, or `checker.reset()`
- Calling **`unreferenced_oids()` while dangling refs remain** — it raises.
  Fix refs first, then hunt orphans
- Expecting **`validate()` to schema-validate** — separate layer, run both
- Fixing objects from `loader.MetaDataVersion()` while validating
  `loader.root()` — **different trees**. Keep one `root()` reference
- Reading only the first error — use **`collect_errors=True`** and fix in bulk

### Your turn → `validate_check_exercise.ipynb` — 4 TODOs, ~20 min

<!--
Working cells run all four layers on a known-clean file; then you diagnose a
schema-invalid file, repair one with reference errors until it validates clean,
and discover why both XSD and the object checks are necessary. Stretch does a
permissive-mode repair. Back in 20 minutes.
-->
