# Changelog

All notable changes to this repository's own files (docs, templates, the
label manifest, and governance tooling) are documented here. Issue numbers
refer to this repo's issues.

## [Unreleased]

### Added: staged production-scoring overlay `v9.3.1-rc.12` (contract and corporate label rounds)

- `mailroom_cache/v9.3.0/pre-release/v9.3.1-rc.12/` is a new cut. It is built from the sandbox's v9.3 label-repaired release at builder and labels commit `84360786` (local-mailroom-sandbox #474).
  - **New labels:** two near-gold rounds, each document read by two independent passes, with every dispute settled by a source-reading review and no `heldout` document labelled. Phase 1 fills the open contract target fields that the production slices 100, 250 and 500 score. Phase 2 fills the open corporate gate fields on 100 calibration documents. Contract labels grow from 6,802 to 7,121, corporate from 2,111 to 2,679, and correspondence from 8,956 to 8,957.
  - **Held-back cells released:** 74 contract cells and 1 corporate cell that rc.11 held as `disputed_unresolved` now carry a reviewed near-gold value. `label_cells_disputed_unresolved` goes from 197 to 125.
  - **Protected truth:** compared with rc.11, no cell was removed, and 888 cells were added. One value changed, on purpose: the reviewed `jurisdiction` of `DOC-971bbacf86cd7a94` goes from a documented absence to `New York`, following the owner-requested review of held absences. The merger and insurance overlays, `gold_override_signoff.csv` and `header_restoration.csv` are byte-identical to rc.11.
  - **Motor Cargo:** the rc.11 `subsidiaries` values of `DOC-91af5bdd6f0ad4bb` were already right; the exhibit lists `Motor Cargo, a Utah corporation` as its own entry. Only that entry's evidence span is corrected here. The rc.11 cut is unchanged.
  - **Needs-human queue:** goes from 290 to 217 rows. 75 rows close because their cells now have a reviewed value. 2 rows open: `DOC-18f682a3054d35c5` and `DOC-3c328f7374a079a9` share the same text but disagree on the wording of `authorized_capital`, so both cells are held back until the labels agree.
  - **Coverage:** 44,770 of 50,299 cells, up from 43,882 in rc.11.
  - rc.1 to rc.11 are unchanged.

### Added: staged production-scoring overlay `v9.3.1-rc.11` (corporate subclass fields)

- `mailroom_cache/v9.3.0/pre-release/v9.3.1-rc.11/` is a new cut. It is built from the sandbox's v9.3 label-repaired release at builder and labels commit `0e083b71` (local-mailroom-sandbox #453).
  - **Corporate subclass fields:** before this cut the release targeted only the Dojo core fields, so no earlier cut carried a corporate subclass field. The near-gold labels for `trustee`, `registered_agent`, `certifying_officer`, `authorized_capital`, `subsidiaries` and the other salient fields of each record's subclass are now in the corporate overlay: 534 labels, 323 populated and 211 documented absences. The corporate overlay grows from 1,523 to 2,111 labels.
  - **Reviewed subclass corrections:** the corrections reviewed since rc.10 are carried, with the fields derived from them: 54 corporate, 9 contract `Consulting Agreements` with their `cuad_family`, and 1 merger `mixed_cash_stock`. Scoring does not apply `subclass` from the overlay, so the Hub subclass stays the raw truth.
  - **Other labels:** the near-gold contract, merger and correspondence labels admitted since rc.10 are carried as well. In contract there are 6 new labels and 2 upgrades from a rule or CUAD-span value to a reviewed one. In merger there are 16 new labels and 3 party lists upgraded from a rule value to near-gold. Correspondence has 4 new documented absences.
  - **Protected truth:** compared with rc.10, no cell was removed, and no reviewed, near-gold, interim-reviewed, owner or Hub value changed. 14 values changed: 9 derived contract `cuad_family` values follow the reviewed corrections, and 5 rule or CUAD-span values were upgraded to near-gold. Insurance and `header_restoration.csv` are byte-identical to rc.10.
  - **Needs-human queue:** grows from 262 to 290 rows. In 23 cells a reviewed absence overrides a populated value, so they need sign-off; the value stays the reviewed absence.
  - **Overrides of Hub values:** go from 1,005 to 1,069 rows in `gold_override_signoff.csv`. All 64 new rows are reviewed subclass corrections.
  - **Coverage:** 43,882 of 50,299 cells, up from 43,257 of 48,688 in rc.10. 1,547 of the 1,611 new target cells are corporate subclass fields; those without a label yet count as unlabeled.
  - rc.1 to rc.10 are unchanged.

### Added: staged production-scoring overlay `v9.3.1-rc.10` (near-gold labels for 61 contracts)

- `mailroom_cache/v9.3.0/pre-release/v9.3.1-rc.10/`: a new cut based on rc.9, rebuilt from the sandbox's regenerated
  v9.3 label-repaired release (builder commit `736fe3ee`, labels commit `f8a9c5bd`).
  - The 61 SEC EDGAR contracts that have neither CUAD clause labels nor reviewed field labels now
    carry near-gold labels for the nine scored contract fields. Each comes from independent label
    and check passes, with disagreements settled by a reviewing model; 21 documents' earlier
    unreviewed candidates were reviewed in place (175 accepted, 7 corrected). They are near-gold,
    not human gold. The contract overlay grows from 6,552 to 6,787 labels.
  - The builder fix that stops treating an event-defined CUAD date ("the date of the last
    signature") as a documented absence reaches the cache: about 90 contract `effective_date` /
    `agreement_date` cells move from absent to unlabeled.
  - No cell held by a reviewed, near-gold, interim-reviewed, owner or Hub source changed value or
    presence. 27 cells where the rc.1 assist file disagrees with a new near-gold value keep the
    near-gold value and join `queues/needs_human.csv` (235 to 262 rows) for sign-off.
  - Coverage 43,257 of 48,688 cells (rc.9: 43,022). The corporate record, correspondence,
    insurance and merger overlays, `gold_override_signoff.csv` and `header_restoration.csv` are
    byte-identical to rc.9. rc.1 to rc.9 are unchanged.

### Added: staged production-scoring overlay `v9.3.1-rc.9` (merger Effective Times, one recipient)

- `mailroom_cache/v9.3.0/pre-release/v9.3.1-rc.9/`: rc.8 with six reviewed corrections from the
  sandbox's `data/labels/review/validation_corrections.jsonl`, each checked against the document
  text. They answer the outside-diff findings on #250 that still held in rc.8.
  - Merger `effective_time`: `DOC-5d30efc302f3c431`, `DOC-cbc95a0d161254eb` and
    `DOC-fc07b37a0f0d1234` were labeled absent although the agreement defines the Effective Time
    (the interim audit marks them `missed_value`); `DOC-7d93372810daa57b` stopped before the
    later-time alternative; `DOC-e6c8852b877c4598` cited a section the agreement lacks. Each now
    holds the defining clause.
  - Correspondence `recipient` of `DOC-2ccf94f14bd5f040` is unlabeled: two reviewed sources
    disagreed and the tie rank picked the sender of the quoted message.
  - Coverage 43,022 of 48,688 cells. Queues, builder outputs and the contract, corporate record
    and insurance overlays are byte-identical to rc.8. rc.1 to rc.8 are unchanged.

### Added: staged production-scoring overlay `v9.3.1-rc.8` (field completeness matches provenance)

- `mailroom_cache/v9.3.0/pre-release/v9.3.1-rc.8/`: rc.7 with `master/..._field_completeness.csv`
  recomputed from the validated provenance. rc.7 built that table before validation, so 10 of its
  74 rows disagreed with its own provenance; the largest was merger `effective_date`, reported
  75.7% complete while 113 of its cells are held as `disputed_unresolved` (1.3% once corrected).
  The overlay, queues, builder, labels and provenance are byte-identical to rc.7, so scoring does
  not change; only the report, the master summary's digests and `MANIFEST.json` differ. The stager
  now refuses to stage a cut whose table disagrees with its provenance. rc.1 to rc.7 are unchanged.

### Added: staged production-scoring overlay `v9.3.1-rc.7` (party-role words, merger signing dates)

- `mailroom_cache/v9.3.0/pre-release/v9.3.1-rc.7/`: rc.6 with two more stager rules.
  - Contract and merger `parties` lose party-role words ("the Customer", "Licensee", "Member"),
    descriptions of a party ("an individual", "your", "the party named above") and alias clauses
    ("d/b/a X"); a role label before a name is trimmed ("the Supplier: X" becomes X). 180
    `parties` cells change. `DOC-e37d7016ebb3e7bc` held only "Member" and "Franchisee", so its
    `parties` is now unlabeled and queued.
  - A merger `effective_date` that is only the signing date follows the owner's answer on the
    `signing_date_as_effective_date` rows of the sandbox interim audit. That answer is still
    pending, so the 90 generated merger effective dates (all signing dates) are now held as
    `disputed_unresolved` and queued, alongside the 23 audited ones already held since rc.5. The
    manifest records `signing_date_policy: pending`.
  - Coverage 43,023 of 48,688 cells, 235 cells for a person, 1,005 overrides awaiting sign-off
    and 735 header restorations. rc.1 to rc.6 are unchanged.

### Added: staged production-scoring overlay `v9.3.1-rc.6` (rc.5 review findings applied)

- `mailroom_cache/v9.3.0/pre-release/v9.3.1-rc.6/`: rc.5 with three name cells corrected and the
  master summary's digests relabelled.
  - `DOC-cbc95a0d161254eb` `financial_advisors` drop the "the retention of" lead-in (now "Keefe,
    Bruyette & Woods, Inc." and "Boenning & Scattergood, Inc.").
  - `DOC-d9157f4ad78024e5` `merger_sub` and its `parties` element are now "Gibraltar Merger Sub
    Inc." without the preceding "Subsidiary of Standard Industries Holdings Inc., and". The
    evidence quotes are unchanged.
  - The master summary's `outputs_sha256` now hashes the released `master/` files and matches
    `MANIFEST.json`. The builder's own digests move to `builder_outputs_sha256`, and
    `needs_human` reports the queue length (144).
  - Everything else is as in rc.5: coverage 43,114 of 48,688 cells, 144 cells for a person,
    1,005 overrides awaiting sign-off and 735 header restorations. rc.1 to rc.5 are unchanged.

### Added: staged production-scoring overlay `v9.3.1-rc.5` (review findings applied)

- `mailroom_cache/v9.3.0/pre-release/v9.3.1-rc.5/`: rc.4 with the fixes from review.
  - 23 merger `effective_date` labels are signing dates whose interim audit still waits for the
    owner. They are now `disputed_unresolved` (not truth) and queued, until the owner decides
    whether a signing date counts as the effective date.
  - Party lists no longer hold suffix-only captures ("Inc.") or bare defined terms ("the
    Company"). That cleaned 50 more `parties` lists, and the `acquirer` "Inc." and the `target`
    "Holdings, Inc." are now unlabeled and queued.
  - Two pairs of documents with identical text carried conflicting labels (`maud_clauses`, and
    `parties` with `cuad_clauses`). Those 6 cells are disputed and queued for a person.
  - Assist notice terms with the same period under another operator ("at least six (6)
    months" against "six (6) months") are now queued for review instead of dropped. An extended
    Hub value would now leave the Hub agreement and enter the overlay; no rc.5 cell is affected.
  - The summary's `label_cells_targeted` is recomputed (48,688, previously 48,686).
  - Coverage: 43,114 of 48,688 cells. The queues hold 144 cells for a person and 1,005 Hub
    overrides awaiting sign-off. `header_restoration.csv` is unchanged (735). rc.1 to rc.4 are
    unchanged.
- `mailroom_cache/README.md`, `mailroom_cache/REGISTRY.json`: regenerated. They list rc.5 and
  describe both label paths (label-sets precedence, and production-overlay replacement), the
  non-Hub scope of validation and the rc.5 rules.

### Added: staged production-scoring overlay `v9.3.1-rc.4` (validated labels, header restoration list)

- `mailroom_cache/v9.3.0/pre-release/v9.3.1-rc.4/`: the rc.3 master after several validation
  passes against the document text. These checks changed 1,983 cells.
  - 600 `cuad_family` values now use the canonical key that the scorer compares, not the raw CUAD
    folder name.
  - 228 `governing_law` values held a whole clause. Each now holds the jurisdiction the clause
    names, and that jurisdiction is found in the text. 13 clauses that name none stay as they
    were and are queued.
  - 218 `parties` lists lost defined-term aliases ("(\"Licensee\")") and clause fragments.
  - 904 Hub correspondence `keywords` lists lost the maildir user, folder and timestamp tokens.
    These replace Hub values, so they are listed for sign-off.
  - 7 partial dates are now unlabeled and queued, and 10 entity lists lost duplicate entries.
  - 16 reviewed corrections were applied. Each quotes the document: wrong or missing agreement
    and effective dates, and one governing law.
  - Coverage: 43,145 of 48,688 cells. The queues now hold 104 cells for a person and 1,005 Hub
    overrides awaiting sign-off.
- `queues/header_restoration.csv` (new): 735 correspondence documents whose labels quote the
  original Enron email header (sender, recipients, date, subject). The cleaned corpus text
  dropped that header. These labels are kept as truth, and the next official release restores
  the listed header lines into `doc_text` so a model can read them. `MANIFEST.json` records the
  count, the validation counts and the input sha256s. rc.1 to rc.3 are unchanged.
- `mailroom_cache/README.md`, `mailroom_cache/REGISTRY.json`: regenerated. They list rc.4 and
  describe the validation step and the header-restoration queue.

### Added: staged production-scoring overlay `v9.3.1-rc.3` (self-contained, magnitudes repaired)

- `mailroom_cache/v9.3.0/pre-release/v9.3.1-rc.3/`: the same merged master as rc.2, with two
  changes.
  - `builder/` now holds the repaired-label builder's four output files, verified
    byte-identical to builder commit `f0951873`, so the cut restages without that unmerged
    branch. `MANIFEST.json` records the builder script's sha256 and commit; the script itself
    stays in the sandbox (this repository holds no code).
  - Twelve staged `termination_notice_period` values that the builder had cut to "eighty (180)
    days" now carry the document's own spelling ("one hundred eighty (180) days").
  - Coverage is unchanged: 43,154 of 48,688 cells, 101 Hub overrides awaiting sign-off, 84 cells
    for a person. rc.1 and rc.2 are unchanged.
- The sandbox scores production against a pinned cut: `config/staged_overlays.yaml` holds this
  repository's commit and the cut's `MANIFEST.json` sha256 (`dataset.staged_overlay`).
- `mailroom_cache/README.md`, `mailroom_cache/REGISTRY.json`: regenerated. They describe
  `builder/` and how production pins a cut.

### Added — staged production-scoring overlay `v9.3.1-rc.2` (planned v10 labels)

- `mailroom_cache/v9.3.0/pre-release/v9.3.1-rc.2/` — the merged master label set on Hub v9.3
  (`ff4ca546`), staged for the planned v10 release and not published: `master/` (joined wide
  CSV, per-cell provenance, completeness, summary; 43,154 of 48,688 cells labeled against 24,812
  in the Hub labels), `overlay/<class>.jsonl` (the 18,441 labels that differ from the Hub,
  101 of them Hub overrides marked `override: true`) for deployments to pull for production
  scoring, and `queues/` (84 cells for a person; the 101 overrides awaiting sign-off).
- `mailroom_cache/README.md`, `mailroom_cache/REGISTRY.json` — regenerated: both pre-release kinds
  (`label-sets`, `production-overlay`) and how production applies the overlay.

### Added — SemVer label cache (`mailroom_cache/`)

- `mailroom_cache/` — semantically versioned cache of the mailroom-dataset labels,
  generated by `scripts/export_mailroom_cache.py` in `Exios66/local-mailroom-sandbox`.
  One folder per dataset release (`v9.1.0`, `v9.3.0`) with an `hf-revision/` pin
  manifest; unpublished label work nests under it as an immutable pre-release.
- `mailroom_cache/v9.3.0/pre-release/v9.3.1-rc.1/` — first pre-release on Hub tag v9.3
  (`ff4ca546`): the full 3,302-row repaired label set (two accepted subclass repairs),
  the review records behind the repairs, the near-gold catalogs, overlay and
  supplementary output, and the repaired interim labels; sha256 for every file in
  its `MANIFEST.json`, all versions in `mailroom_cache/REGISTRY.json`.
- `README.md` (repository tree) and `AGENTS.md` (law 1: generated outputs) name the cache.

### Added — next GPU tier evaluation protocol (#224)

- `reports/NEXT-GPU-TIER-PROTOCOL.md` — repeatable methodology to compare future Modal GPU SKUs to SAND-032 on L4: corpus pin (`ed7576b6…`, `ground_truth` / `all`, seed 42, nested 20 ⊂ 50 ⊂ 100), metrics dictionary (busy-window $, tok/s per GPU, $/doc, $/1M tokens, quality by class), separate Axis A (replica scale-out) and Axis B (serving-knob ladder) templates, pre-spend checklist, and pointers to hub L4 baselines; links [#225](https://github.com/LLM-Mailroom-Services/mailroom-issues/issues/225) for DeepSeek-class planning.
- `reports/README.md` — index row for the protocol doc.
- `reports/AMFAM-BIWEEKLY-ONEPAGER.md` — beat 5 links the canonical protocol doc.

### Fixed — reports site Pages source (#222)

- `README.md`, `AGENTS.md`, `reports/README.md` — document that GitHub Pages
  publishes the reports site from branch `gh-pages` with folder `/docs`, not
  from `main`.

### Added — presentation PNGs; dark, high-contrast figures; every API model covered

- `reports/viz/**/*.png` + `reports/viz/MANIFEST.json` — every report figure as a
  presentation-ready 2× PNG, with the SHA-256 of the SVG each was rendered from.
- All figures redrawn as dark, high-contrast cards on one /dataviz-validated palette;
  each model keeps one color across every chart (Qwen3-8B-AWQ on Modal, Qwen3.7-Flash,
  DeepSeek-V4.1-Flash, Granite-4.2-8B and Qwen3-8B via the API). The site is dark.
- The per-token comparison and the sorter table now include every API model the
  eval-environment measured (Qwen3.7-Flash n = 50 token counts; Qwen3-8B sorter n = 20).

### Added — reports site on GitHub Pages; warm vs cold, $/1M tokens and Modal vs API break-even

- `docs/index.html`, `docs/reports/{master,cost-comparison,gpu-economics}.html`,
  `docs/.nojekyll` — the three reports as a static GitHub Pages site (published
  from branch `gh-pages` `/docs`; inline SVG, no JavaScript, no external
  requests),
  generated by the sandbox alongside the markdown.
- `reports/COST-COMPARISON-MODAL-VS-API.md` §3 — per-document break-even and the
  optimal scenario: verdict per class, every measured Modal configuration against
  the cheapest hosted model, warm 1×L4 / 2×L4 and cold-batch break-even volumes,
  and the deployment where Modal wins on both cost and quality.
- Every break-even verdict names the model on each route: Qwen3-8B-AWQ is the only
  model self-hosted on Modal, and Qwen3.7-Flash and the other hosted models ran through
  the API only. §3.2 compares the same model on both routes (Qwen3-8B-AWQ on Modal vs
  Qwen3-8B via the API).
- `reports/MODAL-VLLM-GPU-REPORT.md` — cost per 1M tokens on three bases and at
  falling utilization, and a warm vs cold GPU section (boot measurements, warm
  vs cold per workload, batch size to amortize a cold start, keep warm vs scale
  to zero). New figures under `reports/figures/gpu/` and
  `reports/figures/cost/modal-vs-api-breakeven.svg`.

### Removed

- `reports/figures/cost/break-even.svg` — replaced by
  `modal-vs-api-breakeven.svg` (the old chart used the boot alone as the cold
  cost and compared against one model only).
### Added — frozen v1 prompt reference & lineage docs

- `docs/PROMPTS.md` — constellation prompt lineage: frozen v1 vs GEPA mutation
  heads vs production pins, with links to eval-environment and sandbox.
- `docs/prompts/frozen-v1/` — sha256-locked read-only copies of `sorter_v1` and
  the five specialist `*_v1` stems (sourced from eval-environment manifest and
  sandbox `eval_environment_lineage.json` @ sandbox `52c92392`, eval-environment
  `48aab48c`).
- `docs/prompts/README.md` — layout, integrity check, refresh procedure.
- `README.md`, `docs/CONSTELLATION.md`, `AGENTS.md`, `reports/README.md` —
  cross-links to the prompt reference.

### Added — cross-repo evaluation reports

- `reports/MASTER-REPORT.md` — current status and research findings for the
  API leg (eval-environment), the Modal + vLLM leg (local-mailroom-sandbox,
  SAND-032) and the ModernBERT intake classifier (mailroom-ml), with the
  cross-leg verdict and the report-audit record.
- `reports/COST-COMPARISON-MODAL-VS-API.md` — Modal L4 vs hosted API cost per
  document and per 0.1 quality, batch and warm-fleet break-even, sorter routes,
  spend and caveats.
- `reports/MODAL-VLLM-GPU-REPORT.md` — the Modal + vLLM leg's GPU economics
  (SAND-032): cost per token for all 24 runs and against the hosted API, the
  spend ledger broken into busy, idle, boot and out-of-run time, client-slot
  occupancy and per-replica vLLM metrics, and the effect of the second L4
  (scale-out, routing, admission, load balance).
- `reports/figures/` — cost and GPU figures drawn for these reports
  (`cost/`, `gpu/`), plus verbatim copies of the source repos' charts;
  `reports/README.md` indexes them.
- `README.md` — new Reports section and `reports/` in the repository layout.

### Added — repository scaffold (initial)

- `README.md` — canonical entry point: what this hub is, what belongs here,
  the constellation, templates, and governance tooling. Rewritten from the
  one-line placeholder.
- `AGENTS.md` — agent navigation rules: the ten laws, triage duties,
  specialist roster, commands, and label-taxonomy summary.
- `docs/CONSTELLATION.md`, `docs/ROUTING.md`, `docs/LABELS.md`,
  `docs/LIFECYCLE.md` — ecosystem map, filing decision tree, label reference,
  and the triage flow.
- `.github/labels.json` — declarative label taxonomy (source of truth),
  codifying the existing repo labels and adding the `type/epic`, `type/rfc`,
  `priority/*`, and `status/*` routing families.
- `.github/ISSUE_TEMPLATE/` — `config.yml`, `bug_report.yml`,
  `feature_request.yml`, `task_todo.yml`, `epic.yml`, `rfc.yml`.
- `.github/PULL_REQUEST_TEMPLATE/pull_request.yml` — hub governance PR form.
- `.github/workflows/issue-governance.yml` — label-manifest audit (PR) and
  sync (merge to main) gate.
- `scripts/labels.py` — `audit`/`sync` driver for the label manifest.
- `CHANGELOG.md`, `LICENSE` (MIT), `.gitignore`.