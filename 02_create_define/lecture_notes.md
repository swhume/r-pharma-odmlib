# Block 2 — Generate a Minimal Define-XML v2.1

In Block 1 you read someone else's define.xml. Now you will create one from scratch — a
minimal but complete and schema-valid Define-XML v2.1 describing a single Demographics (DM)
dataset.

This is where odmlib earns its keep. Hand-writing Define-XML means managing four namespaces,
strict element ordering, dozens of required attributes, and cross-references — and one typo
produces a file that silently fails downstream. With odmlib you build plain Python objects;
namespaces, ordering, and escaping are handled for you, and required attributes are enforced
the moment you construct an object.

## 1. Construction basics

Import the Define-XML v2.1 model and build objects bottom-up with keyword arguments:

```python
import odmlib.define_2_1.model as DEF

item = DEF.ItemDef(OID="IT.DM.AGE", Name="AGE", DataType="integer", Length=3)
```

The rules to know:

- **Required attributes are enforced at construction.** Leave out `Name` and you get an
  immediate `OdmlibRequiredAttributeError` naming the missing attribute — not a broken file
  three steps later. Unknown keyword arguments are rejected too, with a list of valid ones.
- **Element text is the `_content` keyword:** `DEF.TranslatedText(_content="Age", lang="en")`.
- **Single-object children are assigned; list children are appended** (or assigned a whole
  list):

  ```python
  item.Description = DEF.Description()                       # single child: assign
  item.Description.TranslatedText.append(                    # list child: append
      DEF.TranslatedText(_content="Age", lang="en"))
  ```
- **Namespace prefixes are invisible.** `def:Structure`, `xlink:href` — you just write
  `Structure=...`, `href=...`; the model puts the right prefix on the right attribute when
  serializing.
- **Required child *elements* are not checked at construction** — a dataset missing its
  `def:leaf` only surfaces when you validate (Block 3) or schema-validate. Construction
  checks attributes; validation checks structure.

## 2. The worked example — a one-dataset define.xml

Build order follows the document structure, top down. First the root and study:

```python
odm = DEF.ODM(
    FileOID="DEF.RPH2026.DM",
    FileType="Snapshot",
    CreationDateTime="2026-08-19T12:00:00",
    ODMVersion="1.3.2",
    Context="Submission",                 # def:Context - required in Define-XML v2.1
    Originator="R/Pharma 2026 Workshop",
    SourceSystem="odmlib",
)

study = DEF.Study(OID="ST.RPH2026")
study.GlobalVariables = DEF.GlobalVariables(
    StudyName=DEF.StudyName(_content="RPH2026"),
    StudyDescription=DEF.StudyDescription(_content="R/Pharma 2026 odmlib workshop study"),
    ProtocolName=DEF.ProtocolName(_content="RPH-2026-001"),
)
```

The `MetaDataVersion` with its required `def:DefineVersion`, and the `def:Standards` section
every v2.1 define must declare:

```python
mdv = DEF.MetaDataVersion(OID="MDV.RPH2026.1", Name="RPH2026 Data Definitions",
                          Description="Demographics metadata for the workshop",
                          DefineVersion="2.1.0")

standards = DEF.Standards()
standards.Standard.append(
    DEF.Standard(OID="STD.1", Name="SDTMIG", Type="IG", Version="3.4", Status="Final"))
mdv.Standards = standards
```

The DM dataset — an `ItemGroupDef` with its v2.1 attributes, a description, variable
references, a class, and a `def:leaf` pointing at the dataset file:

```python
igd = DEF.ItemGroupDef(
    OID="IG.DM", Name="DM", Repeating="No", IsReferenceData="No",
    SASDatasetName="DM", Domain="DM", Purpose="Tabulation",
    Structure="One record per subject",
    ArchiveLocationID="LF.DM",            # must match the leaf ID below
    StandardOID="STD.1",                  # ties the dataset to a declared Standard
)
igd.Description = DEF.Description()
igd.Description.TranslatedText.append(DEF.TranslatedText(_content="Demographics", lang="en"))

igd.ItemRef.append(DEF.ItemRef(ItemOID="IT.DM.STUDYID", Mandatory="Yes", OrderNumber=1, KeySequence=1))
igd.ItemRef.append(DEF.ItemRef(ItemOID="IT.DM.USUBJID", Mandatory="Yes", OrderNumber=2, KeySequence=2))
igd.ItemRef.append(DEF.ItemRef(ItemOID="IT.DM.AGE", Mandatory="No", OrderNumber=3))
igd.ItemRef.append(DEF.ItemRef(ItemOID="IT.DM.SEX", Mandatory="Yes", OrderNumber=4))

igd.Class = DEF.Class(Name="SPECIAL PURPOSE")
igd.leaf = DEF.leaf(ID="LF.DM", href="dm.xpt", title=DEF.title(_content="dm.xpt"))
```

> **Build children in schema order.** Notice the sequence: `Description`, then `ItemRef`s,
> then `Class`, then `leaf` — the order the Define-XML schema expects. odmlib serializes
> files correctly regardless, but `validate()` flags out-of-order construction, and
> `reorder_object()` fixes it if you add elements late (you'll meet both in the stretch
> goal and in Block 3).

The variables. A helper keeps the repetition down — and bakes in the right child order
(`Description`, `CodeListRef`, `Origin`):

```python
def make_item(oid, name, dtype, length, desc, codelist=None):
    item = DEF.ItemDef(OID=oid, Name=name, DataType=dtype, Length=length, SASFieldName=name)
    item.Description = DEF.Description()
    item.Description.TranslatedText.append(DEF.TranslatedText(_content=desc, lang="en"))
    if codelist:
        item.CodeListRef = DEF.CodeListRef(CodeListOID=codelist)
    item.Origin.append(DEF.Origin(Type="Collected"))
    return item

mdv.ItemDef.append(make_item("IT.DM.STUDYID", "STUDYID", "text", 12, "Study Identifier"))
mdv.ItemDef.append(make_item("IT.DM.USUBJID", "USUBJID", "text", 25, "Unique Subject Identifier"))
mdv.ItemDef.append(make_item("IT.DM.AGE", "AGE", "integer", 3, "Age"))
mdv.ItemDef.append(make_item("IT.DM.SEX", "SEX", "text", 1, "Sex", codelist="CL.SEX"))
```

A codelist for SEX, wired up by the `CodeListRef` above:

```python
cl = DEF.CodeList(OID="CL.SEX", Name="Sex", DataType="text")
for coded, decode in (("F", "Female"), ("M", "Male")):
    term = DEF.CodeListItem(CodedValue=coded)
    term.Decode = DEF.Decode()
    term.Decode.TranslatedText.append(DEF.TranslatedText(_content=decode, lang="en"))
    cl.CodeListItem.append(term)
mdv.CodeList.append(cl)
```

Assemble and write. `Study` and `MetaDataVersion` are **single objects** in Define-XML —
assignment, not append:

```python
mdv.ItemGroupDef.append(igd)
study.MetaDataVersion = mdv      # assignment - single object
odm.Study = study                # assignment - single object

odm.write_xml("output/define_dm.xml")
```

Open the file: four namespaces declared, every element in schema order, all attributes
prefixed correctly — none of which you had to think about.

## 3. Serialization options

| Call | Use it for |
|------|-----------|
| `odm.write_xml(path)` | Writing the document to a file (with XML declaration) |
| `elem.to_xml_string()` | A self-contained XML string of any element — great for debugging and diffs |
| `elem.to_element()` | A real `xml.etree.ElementTree.Element` for interop with other XML tooling (new in 0.2.1) |
| `odm.write_json(path)` / `to_dict()` | Define-XML content as JSON / dicts |

## 4. Viewing the result

The XML itself is readable, but for a human-friendly view, defineutils (demo segment 7) turns
it into the familiar browsable HTML in one command:

```bash
python -m defineutils.definehtml -d output/define_dm.xml -o output/define_dm.html
```

## 5. Beyond Define-XML

The construction pattern is identical across the ODM family. An ARM `AnalysisResultDisplays`
section, an ODM 1.3.2 study, a Dataset-JSON document — all are "construct with kwargs, append
to lists, assign single children, `write_xml()` (or `write_json()`)". Learn it once.

## Things to watch out for

- `study.MetaDataVersion.append(...)` — no: in Define-XML it's a single object; assign it.
- Forgetting `Context` on `DEF.ODM(...)` — `def:Context` is required in v2.1 (its absence is
  the deliberate error in one of Block 3's broken files).
- `ArchiveLocationID` must match a `leaf` `ID` — a mismatch is a ref/def error that Block 3's
  OID checker catches.
- Adding children out of schema order — harmless to `write_xml()`, but `validate()` will tell
  you; `reorder_object()` on the flagged element fixes it.
- Building XML strings by hand for "just one small element" — `to_xml_string()` exists;
  hand-rolled markup is how namespace bugs get in.

## Exercise

Open `create_define_exercise.ipynb`. The root, study, `MetaDataVersion`, and `Standards` are
given; four TODOs have you build the dataset, its variables and codelist, and assemble and
write the file. The stretch goal adds value-level metadata (`ValueListDef` +
`WhereClauseDef`). Budget ~20 minutes. Completed version:
`solutions/create_define_solution.ipynb`.
