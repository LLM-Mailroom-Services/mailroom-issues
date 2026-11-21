# Changelog

All notable changes to this repository's own files (docs, templates, the
label manifest, and governance tooling) are documented here. Issue numbers
refer to this repo's issues.

## [Unreleased]

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