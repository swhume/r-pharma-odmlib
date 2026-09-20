# Workshop Data Files

Sample Define-XML v2.1 files used by the exercises and demos.

| File | Used in | Description |
|------|---------|-------------|
| `defineV21-SDTM.xml` | Blocks 1 & 3, demos | The primary teaching file: the CDISC SDTM Metadata Submission Guidelines (MSG) example define.xml — 11 datasets, 179 variables. Valid against all checks. |
| `defineV21-SDTM-test.xml` | Setup verification | A tiny Define-XML v2.1 fragment for a fast load test. |
| `defineV21-SDTM-invalid.xml` | Block 3, tools demo | Schema-invalid: the required `def:Context` attribute is missing from the `ODM` element. |
| `defineV21-SDTM-invalid-class.xml` | Block 3 | Contains a `def:Class` with an invalid `Name` — caught by XSD enumeration, invisible to the object-level checks. |
| `define_broken_refs.xml` | Block 3, tools demo | A small define (generated with odmlib for this workshop) with a dangling `ItemRef/@ItemOID` and an orphan `ItemDef` — the repair exercise. Schema-valid on purpose. |
| `nonconformant_define21.xml` | Block 3 stretch | Won't load in strict mode (missing required `Repeating`; bogus Origin `Type`) — the permissive-mode repair exercise. |
| `definev21-adam.xml` | Block 1 stretch | An ADaM define.xml with Analysis Results Metadata (ARM v1.0) — the "same pattern, different standard" example. |
| `define_dm_example.xml` | Demos 4 & 6 | The completed minimal DM define that Block 2 builds — a known-good reference. |

## Provenance and licensing

The `defineV21-*` and `definev21-adam` files derive from the example define.xml published in
the CDISC SDTM Metadata Submission Guidelines and are distributed with the
[odmlib](https://github.com/swhume/odmlib) test suite (MIT license); the invalid variants
introduce deliberate errors for teaching. `define_broken_refs.xml` and
`define_dm_example.xml` were generated with odmlib for this workshop. All content is
synthetic example study metadata — no real study data.
