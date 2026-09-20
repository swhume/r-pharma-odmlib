---
marp: true
theme: gaia
paginate: true
footer: 'R/Pharma 2026 · Creating Define-XML Solutions Using Python and odmlib'
---

<!-- _class: lead -->
<!-- _paginate: false -->
<!-- _footer: '' -->

# Block 2
## Generate a Minimal Define-XML v2.1

**15 min lecture · 20 min exercise · 5 min review**

<!--
Segment 3 of 8. Block 1 read someone else's define.xml; now we write one from
scratch - a complete, schema-valid v2.1 describing a single DM dataset. This is
the "build + serialize" third of the development loop.
-->

---

# Why not hand-roll it?

<style scoped>
ul { font-size: 0.85em; }
blockquote { font-size: 0.78em; }
p { font-size: 0.85em; }
</style>

Writing Define-XML by hand means you personally own:

- **Four namespaces** — `def:`, `xlink:`, `xsi:`, and the ODM default
- **Strict element order** — children in the sequence the schema demands
- **Dozens of required attributes** — per element, per version
- **Cross-references** — every OID pointing at something real

One typo ships a file that fails **silently**, weeks later, at a gateway.

> odmlib moves all four into the model.
> Hand-rolled failures are silent; **odmlib failures are loud**.

<!--
Callback to the intro deck's ElementTree-vs-odmlib slide. The framing for the next
15 minutes: everything on this list is something you are about to NOT do.
-->

---

# What you're building

<style scoped>
pre { font-size: 0.72em; }
</style>

```text
ODM  (FileOID, FileType, CreationDateTime, ODMVersion, def:Context)
└ Study  (OID)                                          ← assign
  ├ GlobalVariables  (StudyName, StudyDescription, ProtocolName)
  └ MetaDataVersion  (OID, Name, def:DefineVersion)     ← assign
    ├ def:Standards → Standard  (SDTMIG 3.4)
    ├ ItemGroupDef  "DM"                        [list]
    │   ├ Description   ┐
    │   ├ ItemRef × 4   │ schema order matters
    │   ├ def:Class     │
    │   └ def:leaf ─────┘  ID ⟷ ArchiveLocationID
    ├ ItemDef × 4  (Description, CodeListRef, Origin)   [list]
    └ CodeList  "CL.SEX" → CodeListItem F / M           [list]
```

<!--
Keep this up while I live-code - it is the map for the next nine minutes. Two
things to point at: the brace showing ItemGroupDef's children go in schema order,
and the leaf ID matching ArchiveLocationID, which is the cross-reference Block 3's
OID checker will verify.
-->

---

# Five construction rules

<style scoped>
ol { font-size: 0.7em; line-height: 1.3; }
ol code { font-size: 0.9em; }
</style>

1. **Required attributes are enforced at `__init__`** — omit `Name` and you get
   `OdmlibRequiredAttributeError` *now*, not a broken file three steps later
2. **Element text is `_content=`** — `DEF.TranslatedText(_content="Age", lang="en")`
3. **Single children are assigned, list children are appended**
   `item.Description = DEF.Description()` vs `igd.ItemRef.append(...)`
4. **Namespace prefixes are invisible** — write `Structure=`, `href=`;
   the model puts `def:` / `xlink:` back on serialization
5. **Required child *elements* are not checked at construction** — a dataset
   missing its `def:leaf` surfaces at *validation* (Block 3)

<!--
Rule 3 is the one people trip on and rule 5 is the one that surprises people.
Construction checks attributes; validation checks structure. That split is
deliberate - it's why Block 3 exists.
-->

---

# Getting it back out

<style scoped>
table { font-size: 0.74em; }
pre { font-size: 0.68em; }
p { font-size: 0.82em; }
</style>

| Call | Use it for |
|---|---|
| `odm.write_xml(path)` | The document to a file, with XML declaration |
| `elem.to_xml_string()` | Any element as a string — debugging and diffs |
| `elem.to_element()` | A real `ElementTree.Element` — interop *(new in 0.2.1)* |
| `odm.write_json(path)` / `to_dict()` | Define-XML content as JSON / dicts |

Human-readable view, one command *(demo in segment 7)*:

```bash
python -m defineutils.definehtml -d output/define_dm.xml -o define_dm.html
```

<!--
to_xml_string() on a single element is the debugging tool people don't discover
on their own - reach for it instead of print()ing an object.
-->

---

# Watch out for these

<style scoped>
ul { font-size: 0.74em; line-height: 1.32; }
ul code { font-size: 0.88em; }
h3 { font-size: 0.82em; }
</style>

- **`study.MetaDataVersion.append(...)`** — no: single object, **assign** it
- Forgetting **`Context`** on `DEF.ODM(...)` — `def:Context` is required in v2.1
  *(and is the deliberate error in one of Block 3's broken files)*
- **`ArchiveLocationID` must match a `leaf` `ID`** — a mismatch is a ref/def
  error the OID checker catches
- Adding children **out of schema order** — harmless to `write_xml()`, but
  `validate()` flags it; `reorder_object()` repairs it
- Hand-building an XML string for "just one small element" —
  **`to_xml_string()` exists**; hand-rolled markup is how namespace bugs get in

### Your turn → `create_define_exercise.ipynb` — 4 TODOs, ~20 min

<!--
Root, Study, MetaDataVersion and Standards are given to you - you build the
dataset, the variables, the codelist, then assemble and write. Stretch adds
value-level metadata. The containment diagram slide is the map; keep the lecture
notes open beside the notebook.
-->
