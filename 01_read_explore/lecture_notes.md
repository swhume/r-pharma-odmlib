# Block 1 — Read, Explore, and Report on a Define-XML v2.1

Define-XML is the CDISC standard for describing the datasets, variables, codelists, and
derivations in a study — the machine-readable "data definitions" document that accompanies a
regulatory submission. A define.xml is dense, deeply nested XML with hundreds of
cross-references. Working with it through a generic XML parser means juggling namespaces,
XPath, and OID lookups by hand.

odmlib takes a different approach: it loads the document into a complete Python object model
that mirrors the Define-XML v2.1 specification. Every element becomes an object, every
attribute a typed property, and every list of children a Python list. You explore a define.xml
the way you explore any Python data structure.

In this block you will load the CDISC SDTM Metadata Submission Guidelines (MSG) example
define.xml — a realistic, submission-shaped document with 11 datasets and ~180 variables — and
mine it for information.

## 1. Loading a Define-XML v2.1 file

Two idioms. The explicit loader:

```python
import odmlib.define_loader as DL
import odmlib.loader as LD

loader = LD.ODMLoader(DL.XMLDefineLoader(model_package="define_2_1"))
loader.open_odm_document("../data/defineV21-SDTM.xml")

odm = loader.root()                  # the ODM root object
mdv = odm.Study.MetaDataVersion      # where nearly everything lives
```

And the context-manager shortcut, which defaults to Define-XML v2.1:

```python
from odmlib.context import open_define

with open_define("../data/defineV21-SDTM.xml") as define:
    mdv = define.Study.MetaDataVersion
```

> **NOTE 1: Always pass the model name - `model_package="define_2_1"`.** 
>
> **NOTE 2: `Study` and `MetaDataVersion` are single objects in Define-XML.** A define.xml
> describes one study with one metadata version, so you write `odm.Study.MetaDataVersion` —
> no indexing. (In ODM 1.3.2 these are lists, because an ODM file can carry many studies.)
>
> **NOTE 3: every call to `loader.root()` builds a fresh object tree.** Call it once,
> keep the reference, and navigate from it. The same goes for convenience accessors like
> `loader.MetaDataVersion()` — fine for a quick read, but if you plan to *modify* the
> document, work from a single `root()` object so your changes are all in one tree.

## 2. Navigating the object model

The `MetaDataVersion` object holds the metadata collections as plain Python lists:

```python
mdv.ItemGroupDef        # datasets
mdv.ItemDef             # variables
mdv.CodeList            # controlled terminology
mdv.MethodDef           # derivation methods
mdv.ValueListDef        # value-level metadata
mdv.WhereClauseDef      # value-level conditions
mdv.CommentDef          # comments
mdv.leaf                # external documents (dataset files, aCRF, reviewer guide)
mdv.Standards.Standard  # the standards this define declares
```

Attributes read like properties; element text lives in `_content` (and `str()` of a text
element gives you the text):

```python
for igd in mdv.ItemGroupDef:
    print(igd.OID, igd.Name, igd.Structure)      # def:Structure is just .Structure

first = mdv.ItemDef[0]
print(first.Description.TranslatedText[0]._content)   # or str(...TranslatedText[0])
```

Namespaces (`def:`, `xlink:`) disappear at the Python level — the model already knows which
attribute belongs to which namespace and puts them back when you serialize.

## 3. Finding things

Rather than hand-writing search loops, use `find()` and `find_all()` — both search the
element's descendants for objects of a given class with a matching attribute value:

```python
age = mdv.find("ItemDef", "OID", "IT.DM.AGE")          # first match or None
vs_items = mdv.find_all("ItemDef", "Name", "VSTESTCD") # every match, as a list
```

Cross-references resolve the same way. An `ItemRef` inside a dataset points at an `ItemDef`
by OID:

```python
vs = mdv.find("ItemGroupDef", "OID", "IG.VS")
for ref in sorted(vs.ItemRef, key=lambda r: int(r.OrderNumber)):
    item = mdv.find("ItemDef", "OID", ref.ItemOID)
    print(item.Name, item.DataType, ref.Mandatory)
```

For reverse lookup — "who carries this OID?" — build the OID index once and query it:

```python
idx = odm.build_oid_index()
idx.find_all("IT.DM.AGE")     # every object defining or referencing that OID
```

A variable's codelist is one more hop through a reference:

```python
sex = mdv.find("ItemDef", "OID", "IT.DM.SEX")
cl = mdv.find("CodeList", "OID", sex.CodeListRef.CodeListOID)
for term in cl.CodeListItem:
    print(term.CodedValue, "=", term.Decode.TranslatedText[0]._content)
# F = Female
# M = Male ...
```

NOTE: Some codelists use `EnumeratedItem` instead of `CodeListItem` — enumerations have coded
values but no decodes. Check both.

## 4. Reporting: from objects to metrics

Because everything is lists of objects, document metrics are one-liners:

```python
metrics = {
    "datasets":       len(mdv.ItemGroupDef),
    "variables":      len(mdv.ItemDef),
    "codelists":      len(mdv.CodeList),
    "methods":        len(mdv.MethodDef),
    "value lists":    len(mdv.ValueListDef),
    "where clauses":  len(mdv.WhereClauseDef),
    "comments":       len(mdv.CommentDef),
    "documents":      len(mdv.leaf),
}
for name, count in metrics.items():
    print(f"{name:>14}: {count}")
```

A per-dataset variable listing is a short loop over `ItemRef` with an `ItemDef` lookup — you
will build one in the exercise.

## 5. Beyond Define-XML

The pattern you just learned — loader → root object → navigate → `find()` — is the same for
every standard odmlib supports. Two examples:

**ODM 1.3.2** (operational study metadata and data):

```python
import odmlib.odm_loader as OL
loader = LD.ODMLoader(OL.XMLODMLoader())
loader.open_odm_document("study.xml")
odm = loader.root()
mdv = odm.Study[0].MetaDataVersion[0]     # lists here! ODM can hold many studies
```

**Analysis Results Metadata (ARM)** — an extension of Define-XML v2.1 that documents analysis
displays and results for ADaM. Same loader pattern, richer model:

```python
import odmlib.arm_loader as AL
loader = LD.ODMLoader(AL.XMLArmLoader())
loader.open_odm_document("../data/definev21-adam.xml")
mdv = loader.root().Study.MetaDataVersion
for rd in mdv.AnalysisResultDisplays.ResultDisplay:
    print(rd.OID, "-", str(rd.Description.TranslatedText[0]))
```

The exercise's stretch goal has you run exactly this. odmlib also covers Define-XML v2.0,
Dataset-XML, CT-XML, ODM 2.0 (draft), and Dataset-JSON v1.1 with the same object-model
approach.

## Things to watch out for

- Forgetting `model_package="define_2_1"` on `XMLDefineLoader` (v2.0 is the default model).
- Indexing `Study[0]` / `MetaDataVersion[0]` in Define-XML — they are single objects here;
  lists only in ODM 1.3.2.
- Calling `loader.root()` repeatedly and wondering why edits "disappear" — each call builds a
  fresh tree; keep one reference.
- Reading `.text` for element content — odmlib uses `_content` (or `str(obj)`).
- Assuming every codelist has `CodeListItem` — enumerated codelists use `EnumeratedItem`.

## Exercise

Open `read_explore_exercise.ipynb`. The working cells at the top load the MSG define.xml and
print an overview; then four TODOs have you find a variable, list a dataset's variables,
decode a codelist, and produce a metrics summary — everything shown above. Budget ~20
minutes. A completed version is in `solutions/read_explore_solution.ipynb`.
