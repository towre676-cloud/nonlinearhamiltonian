# Mathematics retrospective table exports

These tables flatten the integrated mathematics atlas through 21 October 2026. They contain all 1,051 main treatments and all 14 supplementary 2023 syntheses. They preserve source mathematics and reviewed atlas classifications without claiming exhaustive recovery of original conversations or historical authorship of the newly developed proofs.

The canonical treatment table is `treatments.csv`, with exactly 1,065 data rows and one header row. The four yearly tables are disjoint subsets. `references.csv` and `source_family_links.csv` normalize repeated fields. `families.csv` contains all 71 developed atlas families. `domains.csv` and `capabilities.csv` provide the code dictionaries. Coverage tables count primary-domain assignments once per treatment. Secondary domains and family references overlap and must not be added to obtain a treatment total.

All CSVs use UTF-8, comma separation, CRLF record endings and double-quoted fields with doubled internal quotes. Embedded newlines are preserved inside quoted cells. JSON arrays and objects remain JSON text within their cells. Source dates are ISO strings where recorded; missing dates are empty, with `date_status=unavailable`. The supplied primary label `Annual synthesis` is preserved for the 14 supplements; they are not assigned invented domain or capability codes.

The source hash protects the complete retained source object even though this tabular view omits retrieval receipts, private storage links and chat-source excerpts. Original-question strings are retained only where the original-question field exists. Revised questions are labeled separately. Potential spreadsheet formula-leading text is escaped with one leading apostrophe; any such occurrences are listed in `export_checks.json`. Remove that apostrophe only when treating the field as plain text. No formulas or macros are authored. The full source JSON in the atlas remains the authority for lossless payload recovery.

## Treatment data dictionary

| Column | Meaning |
| --- | --- |
| uid | Stable globally unique atlas treatment key YEAR:SOURCE_ID. |
| kind | main or supplementary. Supplementary records are the 14 retained 2023 annual syntheses. |
| year | Retained source year, not a claim about the authorship date of the revised proof. |
| date | Recorded source date exactly as retained; empty when unavailable. No dates are inferred. |
| date_status | recorded or unavailable. |
| source_id | Identifier within the annual source, e.g. M001, Y24-07-002, S001. |
| primary_domain | Final reviewed atlas primary domain; Annual synthesis is preserved for supplementary records. |
| primary_domain_title | Human-readable taxonomy title, or the retained supplementary label. |
| secondary_domains | JSON array of final secondary domain IDs. |
| capabilities | JSON array of capability IDs; see capabilities.csv. Empty means no retained assignment. |
| family_ids | JSON array of final assigned family IDs on the treatment wrapper. |
| referencing_family_ids | JSON array of all atlas families citing this source, including cross-domain references. |
| title | Retained revised-treatment title. |
| revised_question | Retained revised question. It is not a reconstructed verbatim historical prompt. |
| revised_question_source | Object path from which the retained question was read. |
| original_question | Retained source.original.original_question only, when present. Blank means no original-question string was retained; it must not be filled by the revised question. |
| status | Retained treatment development or verification status; not newly inferred. |
| summary | Retained treatment summary. |
| definitions_json | JSON array of definitions, preserving exact text. |
| theorem_name | Retained result name, if supplied. |
| theorem_statement | Retained theorem/result statement with its hypotheses. |
| theorem_proof | Retained proof or derivation text. |
| worked_example_json | JSON object containing the retained worked example. |
| limits | Retained mathematical and evidential limitations. |
| extension | Retained extension or next question, if supplied. |
| linked_source_uids | JSON array of retained source links; bare IDs are qualified by the record year. |
| references_json | JSON array of retained mathematical references with labels and URLs. |
| source_payload_sha256 | SHA-256 of the unchanged source object serialized by Python json.dumps(source,sort_keys=True,separators=(comma,colon),ensure_ascii=False), UTF-8 encoded. Computed before CSV safety escaping. |

## Related tables

`references.csv`: one retained reference per treatment and reference number. `source_family_links.csv`: one unique treatment/family pair, with booleans distinguishing assigned membership from citation by a family. `source_links.csv`: retained annual-synthesis links only, qualified by year. `year_coverage.csv`: main, supplementary, total and date-availability counts by year. `domain_year_coverage.csv`: the same main/supplementary population by primary domain and year. `families.csv`: family definitions, theorems, examples, source progression, bridges and actual interactive contracts. Empty values express absence, not a negative mathematical conclusion.
