# Frozen prompt reference (`docs/prompts/`)

Constellation-wide **read-only** copies of the eval-environment **frozen v1**
lineage (`mailroom-dataset-v1`). Implementation and GEPA iteration stay in
[`eval-environment`](https://github.com/LLM-Mailroom-Services/eval-environment),
[`local-mailroom-sandbox`](https://github.com/Exios66/local-mailroom-sandbox),
and [`llm-entity-extraction`](https://github.com/Exios66/llm-entity-extraction);
this hub holds the **reference snapshot** and the routing docs that point at
**current** progressed prompts elsewhere.

> **Do not edit** files under `frozen-v1/` by hand. Refresh from upstream with
> the procedure in [Refreshing the frozen copy](#refreshing-the-frozen-copy).
> For live mutation heads and production pins, see
> [docs/PROMPTS.md](../PROMPTS.md).

## Layout

```
docs/prompts/
├── README.md                          # this file
└── frozen-v1/
    ├── MANIFEST.json                  # sha256 lock + source commits (hub metadata)
    ├── eval_environment_lineage.json  # sandbox ↔ eval-environment specialist map
    ├── sorter/
    │   └── sorter_v1.txt              # production sorter at v1 freeze
    └── specialists/
        ├── contracts_specialist_v1.txt
        ├── corporate_records_specialist_v1.txt
        ├── correspondence_specialist_v1.txt
        ├── insurance_claims_specialist_v1.txt
        └── merger_agreement_specialist_v1.txt
```

## What v1 means

| Artifact | Role |
| --- | --- |
| **`sorter_v1`** | The mailroom **production** sorter template at freeze time (~17k chars). Eval runs default to this key unless `--prompt-version` selects a mutation. |
| **`*_specialist_v1` (five agents)** | **Concise class-specific** specialist stems promoted from sandbox `*_simplified` / `contracts_specialist_v33_simplified` @ sandbox commit `303e7f0` (see `eval_environment_lineage.json`). These are **not** the long vendor `PROMPT_VERSIONS` production pins. |

Specialist bytes in this tree are copied from
`local-mailroom-sandbox/config/prompts/<sandbox_stem>.txt` and must match
`eval-environment/prompts/<eval_environment_key>.md` (body after the markdown H1).

## Integrity

Each file is sha256-locked in [`frozen-v1/MANIFEST.json`](frozen-v1/MANIFEST.json).
The sandbox enforces the same digests in
`config/prompts/eval_environment_lineage.json` and
`tests/test_eval_environment_lineage.py`.

```bash
# from mailroom-issues root — quick local check
python3 - <<'PY'
import hashlib, json
from pathlib import Path
root = Path("docs/prompts/frozen-v1")
manifest = json.loads((root / "MANIFEST.json").read_text())

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

for key, meta in manifest["versions"].items():
    path = root / meta["hub_path"]
    got = sha(path)
    exp = meta["sha256"]
    assert got == exp, f"{key}: {got} != {exp}"
print("frozen-v1 digests OK")
PY
```

## Refreshing the frozen copy

Run only after a **sanctioned** eval-environment re-freeze (see eval-environment
issue tracker — cross-repo alignment is org-governed, not a drive-by edit).

1. Check out pinned siblings:
   - `LLM-Mailroom-Services/eval-environment` @ commit recorded in
     `MANIFEST.json` `source_repos.eval-environment.commit` (update after refresh).
   - `Exios66/local-mailroom-sandbox` @ matching lineage lock.
2. Re-copy specialist `.txt` stems listed in `eval_environment_lineage.json`.
3. Re-copy `sorter_v1` from `eval-environment/prompts/sorter_v1.md` (strip leading
   `#` title line; file body must match `manifest.json` `chars` / `sha256`).
4. Update `MANIFEST.json` source commits and `CHANGELOG.md` `[Unreleased]`.
5. Open a PR here; link the eval-environment / sandbox PRs that performed the
   re-freeze.

## Related constellation docs

- [PROMPTS.md](../PROMPTS.md) — resolution layers, **current** mutation heads,
  production pins, and where to run evals.
- [CONSTELLATION.md](../CONSTELLATION.md) — repository map.
- [reports/MASTER-REPORT.md](../../reports/MASTER-REPORT.md) — latest cross-leg
  prompt promotion evidence (e.g. correspondence v2 on Qwen AWQ).
