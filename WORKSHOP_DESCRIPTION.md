# Creating Define-XML Solutions Using Python and odmlib

*R/Pharma 2026 workshop — program description (~205 words)*

This hands-on workshop teaches you to work with Define-XML v2.1 in Python using
odmlib, the open-source library that models the entire CDISC ODM family as schema-aware
Python objects.

Working in Jupyter notebooks, you will complete three guided exercise blocks: read a
realistic, submission-scale define.xml to find content and generate metrics; create a
complete, schema-valid Define-XML v2.1 document from scratch; and run odmlib's four
validation layers - XSD schema, OID reference/definition integrity, conformance, and element
order - to diagnose and repair broken files. Short demos follow: extending the Define-XML
model with namespaces, flattening Define-XML into datasets, AI-assisted odmlib development 
using the odmlib skill with Claude Code, and the defineutils command-line tools built on odmlib. 
Although the workshop focuses on Define-XML and odmlib has been most widely implemented 
in Define-XML solutions, the same idioms apply across ODM, Analysis Results Metadata
(ARM), and Dataset-JSON.

All content - lecture notes, exercises, solutions, and sample data - ships in a public GitHub
repository that you clone at the start and keep afterward. Intermediate Python experience is
expected; no prior odmlib or deep CDISC knowledge is required.

## Speaker bio (~130 words)

Sam Hume runs Hume Data Labs, an independent practice building open-source
software that makes clinical research and healthcare data standards executable. Sam is the
creator and maintainer of odmlib, the open-source Python library for CDISC ODM and the
ODM-based standards, including Define-XML, Dataset-JSON, and Analysis Results Metadata. 
Previously CDISC's VP of Data Science for more than a decade, Sam now works with CDISC as a 
Principal Consultant, co-leading the 360i Data Definition Engine, Data Definition Specification 
model, and Data Exchange Standards teams, and is an active PHUSE contributor. With 30+ years 
in senior technology roles across the biopharmaceutical industry. Sam's work is guided by a simple 
idea: standards earn their keep when they're executable, not when they sit as static documents.
