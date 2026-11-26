# Mailroom label cache (`mailroom_cache`)

Semantically versioned, cached copies of the
[`Lucius-Morningstar/mailroom-dataset`](https://huggingface.co/datasets/Lucius-Morningstar/mailroom-dataset) labels and of the
label repairs and enhancements made after each release. **Generated, never hand-edited:** the
builder is `scripts/export_mailroom_cache.py` in [`Exios66/local-mailroom-sandbox`](https://github.com/Exios66/local-mailroom-sandbox).

## Layout

The top-level folder is the dataset release (`vMAJOR.MINOR.0`, one per Hub tag). Everything made
between that release and the next minor version nests under it, as an immutable SemVer
pre-release:

```text
mailroom_cache/
  REGISTRY.json                         every cached version with its pins and digests
  vX.Y.0/                               dataset release = Hub tag vX.Y
    hf-revision/MANIFEST.json           channel "hf-revision": tag commit + parquet parent (pin only)
    pre-release/vX.Y.P-rc.N/            channel "pre-release": unpublished label work on vX.Y
      MANIFEST.json                     base revision, source commit, counts, sha256 of every file
      repairs/full-label-set/*.csv      the full repaired label set, one row per document
      repairs/review/                   review verdicts and decisions behind the repairs
      enhancements/gold/                near-gold catalogs (schema-gated)
      enhancements/gold-overlay/        the near-gold overlay production runs merge
      enhancements/gold-supplementary/  supplementary labeler output (never ground truth)
      enhancements/interim/             repaired interim gap fills and corrections
    pre-release/vX.Y.P-rc.N/            kind "production-overlay": the merged master, staged
      MANIFEST.json                     inputs (builder commit, sha256), coverage, overlay counts
      master/                           joined wide CSV, per-cell provenance, completeness, summary
      overlay/<class>.jsonl             every label that differs from Hub vX.Y (pulled by deployments)
      builder/                          the builder outputs it was staged from (rc.3 on)
      queues/needs_human.csv            unresolved disputes and join cells a person must decide
      queues/gold_override_signoff.csv  Hub overrides, decided_by blank until initialled
      queues/header_restoration.csv     correspondence whose labels quote the lost Enron header (rc.4 on)
```

A pre-release is either `label-sets` (the raw sandbox layers, as cut) or `production-overlay`
(those layers merged into one master by the repaired-label builder, then staged as an overlay).
Production scoring applies one pinned `production-overlay`, never "the newest": the sandbox pins
the version, this repository's commit and the MANIFEST.json sha256 in `config/staged_overlays.yaml`
and refuses a cut that does not match (`scripts/pull_staged_overlay.py`, then `dataset.staged_overlay`
in the run config). The Hub label comes first, replaced field by field by `overlay/<class>.jsonl`,
where `override: true` marks a replaced Hub value. Each record's `content_sha256` is checked
against the document before it is applied. The overlay already contains the interim and
near-gold labels it merged, so it is applied instead of those layers, never on top of them.

From rc.4 the stager also validates the merged staged (non-Hub) labels before staging
(`validation_repair` in the manifest); Hub-backed cells are only keyword-cleaned. It keeps only
whole ISO dates, maps `cuad_family` to its canonical key, reduces whole governing-law clauses to
the named jurisdiction, and removes defined-term aliases and clause fragments from `parties`. It
strips the maildir user, folder and timestamp tokens from Hub correspondence `keywords`, and
applies reviewed corrections (a populated one must quote the document text). From rc.5 it also
drops bare defined terms ("the Company") and suffix-only captures ("Inc.") from `parties` and
unlabels a name field that holds only one. It holds back as `disputed_unresolved` an interim
value whose audit waits for the owner, and the conflicting values of documents with the same
text. Both go to `queues/needs_human.csv`. From rc.6 a party, advisor or counsel name loses a
describing lead-in ("the retention of X", "Subsidiary of Y, and X" become X; the evidence quote is
kept), and the master summary's `outputs_sha256` hashes the `master/` files, with the builder's
own digests under `builder_outputs_sha256`. From rc.7 `parties` also loses party-role words ("the
Customer", "Member"), descriptions of a party ("an individual", "your") and alias clauses ("d/b/a
X"), and a role label before a name is trimmed ("the Supplier: X" becomes X). A merger
`effective_date` that is only the signing date follows the owner's answer in the interim audit
(`signing_date_policy` in the manifest): held back as disputed while it is pending, cleared or
kept once it is recorded.

Some correspondence labels quote the original Enron email header (sender, recipients, date,
subject). The cleaned corpus text dropped that header, so `queues/header_restoration.csv` lists
each such document with its maildir file and the quoted header lines. The next official release
restores those lines into `doc_text`, so a model can read what the labels expect.

- **Patch** (`X.Y.P`) counts label repair rounds on release `X.Y`.
- **Pre-release** (`-rc.N`) is one cut of that round. A cut is never rewritten: changed labels
  get the next `rc.N`. Build metadata `+hf.<tag commit>` in each manifest names the Hub revision.
- When the Hub publishes the repairs as a new tag, it gets its own `vX.Y.0/hf-revision/`.

## Versions

| Version | Channel | Path | Pins |
| --- | --- | --- | --- |
| `9.1.0` | hf-revision | `v9.1.0/hf-revision/` | Hub `v9.1` → `bc9eab28` (data `ed7576b6`) |
| `9.3.0` | hf-revision | `v9.3.0/hf-revision/` | Hub `v9.3` → `ff4ca546` (data `7fd99b40`) |
| `9.3.1-rc.1` | pre-release | `v9.3.0/pre-release/v9.3.1-rc.1/` | label-sets on `9.3.0`; sandbox labels `10c2adaf` |
| `9.3.1-rc.10` | pre-release | `v9.3.0/pre-release/v9.3.1-rc.10/` | production-overlay on `9.3.0`; sandbox labels `f8a9c5bd` |
| `9.3.1-rc.2` | pre-release | `v9.3.0/pre-release/v9.3.1-rc.2/` | production-overlay on `9.3.0`; sandbox labels `10c2adaf` |
| `9.3.1-rc.3` | pre-release | `v9.3.0/pre-release/v9.3.1-rc.3/` | production-overlay on `9.3.0`; sandbox labels `10c2adaf` |
| `9.3.1-rc.4` | pre-release | `v9.3.0/pre-release/v9.3.1-rc.4/` | production-overlay on `9.3.0`; sandbox labels `dbf16215` |
| `9.3.1-rc.5` | pre-release | `v9.3.0/pre-release/v9.3.1-rc.5/` | production-overlay on `9.3.0`; sandbox labels `9e641d99` |
| `9.3.1-rc.6` | pre-release | `v9.3.0/pre-release/v9.3.1-rc.6/` | production-overlay on `9.3.0`; sandbox labels `9e641d99` |
| `9.3.1-rc.7` | pre-release | `v9.3.0/pre-release/v9.3.1-rc.7/` | production-overlay on `9.3.0`; sandbox labels `9e641d99` |
| `9.3.1-rc.8` | pre-release | `v9.3.0/pre-release/v9.3.1-rc.8/` | production-overlay on `9.3.0`; sandbox labels `9e641d99` |
| `9.3.1-rc.9` | pre-release | `v9.3.0/pre-release/v9.3.1-rc.9/` | production-overlay on `9.3.0`; sandbox labels `3c24ccba` |

The current family pin is `v9.3.0`. Two label paths exist, and a run uses
one of them. With the `label-sets` layers, precedence is the Hub label, then interim truth, then
the near-gold overlay for fields nothing else labels. With a `production-overlay` cut, the
overlay replaces the Hub value field by field (`override: true`), and the interim and near-gold
layers are not applied again. Supplementary output is never ground truth.

## Use

```bash
git clone --filter=blob:none --sparse https://github.com/LLM-Mailroom-Services/mailroom-issues.git
cd mailroom-issues
git sparse-checkout set mailroom_cache/v9.3.0
cd mailroom_cache/<pre-release path>   # e.g. v9.3.0/pre-release/v9.3.1-rc.1
python3 -c "import json;[print(v['sha256']+'  '+k) for k,v in json.load(open('MANIFEST.json'))['files'].items()]" | sha256sum -c --quiet
```

`sha256sum` prints nothing when every file matches its manifest digest.

## Regenerate

In `Exios66/local-mailroom-sandbox`, with `mailroom-issues` checked out next to it:

```bash
python scripts/export_mailroom_cache.py --version X.Y.P-rc.N --full-labels <repaired-labels.csv>
python scripts/export_mailroom_cache.py --version X.Y.P-rc.N --check
```
