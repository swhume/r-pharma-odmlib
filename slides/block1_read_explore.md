---
marp: true
theme: gaia
paginate: true
footer: 'R/Pharma 2026 · Creating Define-XML Solutions Using Python and odmlib'
---

<!-- _class: lead -->
<!-- _paginate: false -->
<!-- _footer: '' -->

# Block 1
## Read, Explore, and Report on a Define-XML v2.1

**15 min lecture · 20 min exercise · 5 min review**

<!--
Where we are: segment 2 of 8. This is the "load" third of the odmlib development
loop from the intro. Four minutes of slides, then I drive a live notebook, then
you take the exercise. Everything I run is in 01_read_explore/lecture_demo.ipynb -
you have it, you can follow along or just watch.
-->

---

# The one idea

<style scoped>
pre { font-size: 0.7em; }
</style>

```text
  define.xml                     odmlib objects
  ──────────                     ──────────────
  <ODM>                          odm
   └ <Study>                      └ .Study             ← single object
      └ <MetaDataVersion>          └ .MetaDataVersion  ← single object
         ├ <ItemGroupDef>             ├ .ItemGroupDef   [list]
         │   └ <ItemRef ──┐           │    └ .ItemRef   [list]
         ├ <ItemDef> ◄────┘           ├ .ItemDef        [list]
         └ <CodeList>                 └ .CodeList       [list]
```

Not a parse tree — a **typed object model of the v2.1 spec**.
Namespaces, XPath, and OID bookkeeping stop being your problem.

<!--
This is the slide that matters. Everything else in the block follows from it.
The arrow is the point: ItemRef carries an OID string that names an ItemDef -
Define-XML is a graph, and in a moment you'll see find() traverse that edge in
one line instead of a nested loop.
-->

---

# Three idioms — that's the whole block

<style scoped>
pre { font-size: 0.74em; }
p { font-size: 0.85em; }
p code { font-size: 0.9em; }
</style>

```python
# 1. load
loader = LD.ODMLoader(DL.XMLDefineLoader(model_package="define_2_1"))
loader.open_odm_document(path)
mdv = loader.root().Study.MetaDataVersion

# 2. navigate — collections are plain Python lists
mdv.ItemGroupDef · mdv.ItemDef · mdv.CodeList · mdv.MethodDef

# 3. find — searches descendants by class + attribute
mdv.find("ItemDef", "OID", "IT.DM.AGE")      # first match or None
mdv.find_all("ItemDef", "Name", "VSTESTCD")  # every match, a list
```

Element text is **`_content`** — `age.Description.TranslatedText[0]._content`

<!--
Signatures only - the worked examples are in the lecture notes and I'm about to
run all of this live. Two things to flag now because they cause most of the
exercise stumbles: model_package is required (v2.0 is the default), and text
lives in _content, not .text.
-->

---

# Beyond Define-XML

<style scoped>
p { font-size: 0.85em; }
table { font-size: 0.78em; }
</style>

The same four lines, a different standard — swap the loader:

| Standard | Loader | Note |
|---|---|---|
| Define-XML 2.0 / 2.1 | `XMLDefineLoader` | today |
| ODM 1.3.2 | `XMLODMLoader` | `Study[0]`, `MetaDataVersion[0]` — **lists** |
| ARM 1.0 | `XMLArmLoader` | `mdv.AnalysisResultDisplays` |
| Dataset-JSON 1.1 | `DatasetJSON.read_json()` | JSON — no XML loader needed |

Learn the idioms once. **Block 1's stretch goal is the ARM row.**

<!--
Breadth message - I'm not demoing this, the stretch goal does it for you in two
lines. The ODM row is the one gotcha worth remembering: an ODM file can carry many
studies, so those are lists there and single objects here.
-->

---

# Watch out for these

<style scoped>
ul { font-size: 0.74em; line-height: 1.32; }
ul code { font-size: 0.88em; }
h3 { font-size: 0.82em; }
</style>

- Forgetting **`model_package="define_2_1"`** — v2.0 is the default
- Indexing **`Study[0]`** in Define-XML — single objects here, lists in ODM 1.3.2
- Calling **`loader.root()` repeatedly** — each call builds a *fresh* tree,
  so edits seem to vanish. Call once, keep the reference
- Reading **`.text`** for element content — odmlib uses `_content`
- Assuming every codelist has `CodeListItem` — enumerations use
  **`EnumeratedItem`** (coded values, no decodes). Check both

### Your turn → `read_explore_exercise.ipynb` — 4 TODOs, ~20 min

<!--
Read these out - they are the five things that will cost someone five minutes
otherwise. The last one bites in TODO 3 specifically.
Hand-off: full detail is in 01_read_explore/lecture_notes.md, open it beside the
notebook. Solutions folder is the safety net, not cheating. Back in 20 minutes.
-->
