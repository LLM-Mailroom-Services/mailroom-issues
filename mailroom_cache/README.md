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
```

- **Patch** (`X.Y.P`) counts label repair rounds on release `X.Y`.
- **Pre-release** (`-rc.N`) is one cut of that round. A cut is never rewritten: changed labels
  get the next `rc.N`. Build metadata `+hf.<tag commit>` in each manifest names the Hub revision.
- When the Hub publishes the repairs as a new tag, it gets its own `vX.Y.0/hf-revision/`.

## Versions

| Version | Channel | Path | Pins |
| --- | --- | --- | --- |
| `9.1.0` | hf-revision | `v9.1.0/hf-revision/` | Hub `v9.1` → `bc9eab28` (data `ed7576b6`) |
| `9.3.0` | hf-revision | `v9.3.0/hf-revision/` | Hub `v9.3` → `ff4ca546` (data `7fd99b40`) |
| `9.3.1-rc.1` | pre-release | `v9.3.0/pre-release/v9.3.1-rc.1/` | builds on `9.3.0`; sandbox labels `10c2adaf` |

The current family pin is `v9.3.0`. Label precedence when a run reads
these sets is unchanged: Hub label, then interim truth, then the near-gold overlay for fields
nothing else labels. Supplementary output is never ground truth.

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
