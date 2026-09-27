# Hugging Face corpus cache (`data/hf_cache`)

Colocated, loader-compatible byte cache for
[`Lucius-Morningstar/mailroom-dataset`](https://huggingface.co/datasets/Lucius-Morningstar/mailroom-dataset)
train parquets. Binaries live under `corpus/` with filenames derived from the
`llm-mailroom` `hf_corpus_loader._cached_get_bytes` URL-key scheme so consumers
can skip Hub downloads when revision content matches the manifest pin.

## Pin

| Field | Value |
|---|---|
| Dataset | `Lucius-Morningstar/mailroom-dataset` |
| Revision (SHA) | `ed7576b676343e0b402ec5412cded301e629bdee` (v9.1 content pin) |
| Previous cache revision | `46a4d3c240a36671cde0182fff4960f6b8b73aca` |

Authoritative file list, sizes, and SHA-256 digests: [`MANIFEST.json`](MANIFEST.json).

The Hub tag `v9.1` may point at a different commit than this pin; the manifest
records that drift. Prefer the SHA in `MANIFEST.json` over the moving tag.

## How the constellation calls this cache

Runtime loaders in `llm-mailroom` resolve parquet bytes through
`MAILROOM_HF_CACHE_DIR`, which defaults to `{MAILROOM_BASE_DIR}/hf_cache/corpus`
(see `packages/llm-mailroom/src/pipeline/hf_corpus_loader.py`). Point the env
var at this directory after checkout:

```bash
export MAILROOM_HF_CACHE_DIR="/path/to/mailroom-issues/data/hf_cache/corpus"
```

`load_corpus(revision=<FULL_CORPUS_REVISION>)` walks the `/parquet` ladder and
`_cached_get_bytes` reads the matching `.bin` when the URL key hash matches.
Companion revision pins (`hf_corpora.FULL_CORPUS_REVISION`, sandbox
`FAMILY_HF_REVISION`) must stay aligned with `MANIFEST.json` `revision`.

## Sparse checkout (cache only)

```bash
git clone --filter=blob:none --sparse https://github.com/LLM-Mailroom-Services/mailroom-issues.git
cd mailroom-issues
git sparse-checkout set data/hf_cache
export MAILROOM_HF_CACHE_DIR="$PWD/data/hf_cache/corpus"
```

No Git LFS — cache files are normal git blobs. Refresh procedure and acceptance
criteria: [issue #201](https://github.com/LLM-Mailroom-Services/mailroom-issues/issues/201).
