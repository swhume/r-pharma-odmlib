# Demo — Extending the Define-XML Model

Vendor extensions are a designed-in part of ODM: sponsors and tool vendors routinely carry
extra attributes and elements in their own namespace alongside the standard content. odmlib's
model classes are ordinary Python classes, so extension is ordinary subclassing — this is not
a bolted-on feature but exactly how odmlib builds its own models: `define_2_1` extends
`odm_1_3_2`, and `arm_1_0` extends `define_2_1`. Your extensions use the same machinery as
those production models.

This 10-minute demo (`extend_model_demo.ipynb`) walks the full lifecycle: extend, write,
round-trip, and the honest story on schema validation.

## 1. A vendor attribute in three lines

Register the vendor namespace, then subclass with `merge_fields=True`, which inherits every
field from the base class — no redeclaring 20 attributes:

```python
import odmlib.ns_registry as NS
import odmlib.typed as T
import odmlib.define_2_1.model as DEF

NS.NamespaceRegistry(prefix="vnd", uri="https://example.org/vnd/v1.0")

class ItemDef(DEF.ItemDef, merge_fields=True):
    ReviewStatus = T.String(namespace="vnd")
```

Two rules:

- **Name the subclass after the element.** The XML tag comes from the class name — a class
  called `TrackedItemDef` would serialize as `<TrackedItemDef>`. Shadowing the stock name in
  your module is the point.
- **Never register an extension namespace as the default** (`is_default=True`) — the default
  namespace belongs to ODM.

Instances work like any ItemDef, plus the new attribute:

```python
item = ItemDef(OID="IT.DM.RACE", Name="RACE", DataType="text", Length=20,
               ReviewStatus="Draft")
```

Serialized, it comes out exactly right: `vnd:ReviewStatus="Draft"` with
`xmlns:vnd="https://example.org/vnd/v1.0"` declared.

## 2. Round-tripping extended documents

Loading an extended file with the *stock* model fails — strict mode rejects the unknown
attribute (by design: strictness is what catches typos). Two ways in:

**A local model package** — the production answer. A module that imports the stock model and
overrides the extended classes (see `custom_define/model.py`, ~10 lines). The loader accepts
it via `local_model=True`:

```python
loader = LD.ODMLoader(DL.XMLDefineLoader(model_package="custom_define", local_model=True))
loader.open_odm_document("output/define_dm_extended.xml")
# ...ReviewStatus is a first-class, typed attribute again
```

**Permissive mode** — the pragmatic answer for files you merely consume:

```python
with odmlib.permissive():
    odm = load_define("output/define_dm_extended.xml")   # extension attrs tolerated
```

## 3. The honest story on validation

- **Stock XSD:** the Define-XML v2.1 schema pins the attribute set of most elements, so a
  vendor attribute makes the file fail stock schema validation. That is a property of the
  standard, not of odmlib. Submission-grade extensions ship an *extension schema* (the
  standard's `define-extension.xsd` exists exactly for this), and odmlib plugs it straight
  in: `ODMSchemaValidator(xsd_file="your_extended_schema.xsd")`.
- **Conformance checker:** validates against the stock model, so it flags your extension as
  an unknown field — expected; scope it accordingly.
- **OID checks and ordering:** unaffected; they work on extended documents as-is.
- **The no-schema-change alternative:** for small annotations, consider the standard's own
  `Alias` element (`Context` + `Name`) — carried by most Define-XML elements, no extension
  namespace or schema needed, valid everywhere.

## 4. Going further

- A complete hand-written extension model: `tests/model_extended.py` in the odmlib repo
  (adds a constrained `Alias/@Standard` with `T.ExtendedValidValues`).
- The production-scale examples inside odmlib itself: `odmlib/define_2_1/model.py` (extends
  ODM 1.3.2 with the whole `def:` namespace) and `odmlib/arm_1_0/model.py` (extends
  Define-XML v2.1 with `arm:`).
- The full descriptor toolbox in `odmlib/typed.py`: `T.String`, `T.OID`, `T.OIDRef`,
  `T.ValueSetString`, `T.ExtendedValidValues`, `T.ODMObject`, `T.ODMListObject`, and more.
