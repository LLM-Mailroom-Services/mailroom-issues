# Prompt lineage across the constellation

How mailroom **sorter** and **specialist** prompts are versioned, where the
**frozen v1** reference lives in this hub, and where to find the **current**
progressed copies that passed GEPA guardrails (and, where recorded, eval
promotion checkpoints).

## Resolution layers (eval-environment model)

Eval runs resolve prompts through four layers (full detail:
[`eval-environment/docs/prompt-lineage.md`](https://github.com/LLM-Mailroom-Services/eval-environment/blob/main/docs/prompt-lineage.md)):

| Layer | Lineage | Source | Typical use |
| --- | --- | --- | --- |
| **Frozen v1** | `mailroom-dataset-v1` | `prompts/manifest.json` + generated `frozen_v1.py` | **Default eval baseline** — never edited in place |
| **Archived v0** | same lineage | `archived_production.py` | `--prompt-source archived` — pre-concise production specialists |
| **Mutations v2+** | same lineage | `prompts/mutations.json` + `prompts/<key>.md` | GEPA candidates; each apply passed **five gates** (anchor, naming, additive-only, metadata, length budget) |
| **Production** | pipeline | `llm.prompts.prompt_templates` / Langfuse | `--prompt-source production` — live mailroom templates |

**Constellation reference copy of frozen v1:**
[`docs/prompts/frozen-v1/`](prompts/frozen-v1/) ([README](prompts/README.md)).

## Frozen v1 in this hub (do not edit)

| Key | Hub path | Origin at freeze |
| --- | --- | --- |
| `sorter_v1` | [`prompts/frozen-v1/sorter/sorter_v1.txt`](prompts/frozen-v1/sorter/sorter_v1.txt) | llm-mailroom production `sorter` template |
| `contracts_specialist_v1` | [`prompts/frozen-v1/specialists/contracts_specialist_v1.txt`](prompts/frozen-v1/specialists/contracts_specialist_v1.txt) | sandbox `contracts_specialist_v33_simplified` |
| `corporate_records_specialist_v1` | [`prompts/frozen-v1/specialists/corporate_records_specialist_v1.txt`](prompts/frozen-v1/specialists/corporate_records_specialist_v1.txt) | sandbox `corporate_records_specialist_simplified` |
| `correspondence_specialist_v1` | [`prompts/frozen-v1/specialists/correspondence_specialist_v1.txt`](prompts/frozen-v1/specialists/correspondence_specialist_v1.txt) | sandbox `correspondence_specialist_simplified` |
| `insurance_claims_specialist_v1` | [`prompts/frozen-v1/specialists/insurance_claims_specialist_v1.txt`](prompts/frozen-v1/specialists/insurance_claims_specialist_v1.txt) | sandbox `insurance_claims_specialist_simplified` |
| `merger_agreement_specialist_v1` | [`prompts/frozen-v1/specialists/merger_agreement_specialist_v1.txt`](prompts/frozen-v1/specialists/merger_agreement_specialist_v1.txt) | sandbox `merger_agreement_specialist_simplified` |

Sha256 locks:
[`docs/prompts/frozen-v1/MANIFEST.json`](prompts/frozen-v1/MANIFEST.json) · sandbox
[`config/prompts/eval_environment_lineage.json`](https://github.com/Exios66/local-mailroom-sandbox/blob/main/config/prompts/eval_environment_lineage.json).

## Current progressed prompts (mutation heads)

After a mutation is **applied**, its full text lives in eval-environment
`prompts/<key>.md` and in `prompts/mutations.json`. The table below is the
**latest guardrail-validated mutation per role** on eval-environment
`main` @ `48aab48c77ea349abed3b0779e319bf8cd75beee` (refresh this doc when
`mutations.json` advances).

| Agent / role | Frozen v1 (hub) | **Current mutation head** | Eval-environment file |
| --- | --- | --- | --- |
| Sorter | `sorter_v1` | **`sorter_v3`** | [`prompts/mutations.json`](https://github.com/LLM-Mailroom-Services/eval-environment/blob/main/prompts/mutations.json) (entry `sorter_v3`; full text in JSON until mirrored to `prompts/sorter_v3.md`) |
| Contracts specialist | `contracts_specialist_v1` | **`contracts_specialist_v3`** | [`prompts/contracts_specialist_v3.md`](https://github.com/LLM-Mailroom-Services/eval-environment/blob/main/prompts/contracts_specialist_v3.md) |
| Corporate records specialist | `corporate_records_specialist_v1` | **`corporate_records_specialist_v5`** | [`prompts/corporate_records_specialist_v5.md`](https://github.com/LLM-Mailroom-Services/eval-environment/blob/main/prompts/corporate_records_specialist_v5.md) |
| Correspondence specialist | `correspondence_specialist_v1` | **`correspondence_specialist_v6`** | [`prompts/correspondence_specialist_v6.md`](https://github.com/LLM-Mailroom-Services/eval-environment/blob/main/prompts/correspondence_specialist_v6.md) |
| Insurance claims specialist | `insurance_claims_specialist_v1` | **`insurance_claims_specialist_v3`** | [`prompts/insurance_claims_specialist_v3.md`](https://github.com/LLM-Mailroom-Services/eval-environment/blob/main/prompts/insurance_claims_specialist_v3.md) |
| Merger agreement specialist | `merger_agreement_specialist_v1` | **`merger_agreement_specialist_v3`** | [`prompts/merger_agreement_specialist_v3.md`](https://github.com/LLM-Mailroom-Services/eval-environment/blob/main/prompts/merger_agreement_specialist_v3.md) |

**How to read “current”:**

1. **GEPA head** — highest `_vN` for that role in
   [`prompts/mutations.json`](https://github.com/LLM-Mailroom-Services/eval-environment/blob/main/prompts/mutations.json)
   (passed apply-time gates when appended).
2. **Eval promotion checkpoint** — paired A/B evidence may **hold** or **promote**
   an earlier mutation even when the GEPA head moved forward. Example (Modal +
   Qwen3-8B-AWQ, SAND-032): **`correspondence_specialist_v2` PROMOTE**;
   insurance and corporate v2 **HOLD** — see
   [reports/MASTER-REPORT.md](../reports/MASTER-REPORT.md) §3.
3. **Production pipeline** — live LangGraph / LangChain pins in vendored
   llm-mailroom (Family B), e.g. sandbox registry
   [`prompt_registry.py`](https://github.com/Exios66/local-mailroom-sandbox/blob/main/src/mailroom_sandbox/prompt_registry.py):
   `sorter` → `sorter_v14`, `contracts_specialist` → `contracts_specialist_v33`.
   Production is **not** automatically the GEPA head; promotion is a separate
   decision.

## Sandbox local stems (Modal / vLLM)

Sandbox run YAMLs pin **frozen v1 specialist stems** (`*_simplified` /
`contracts_specialist_v33_simplified`), not vendor production mirrors. Inventory:
[`local-mailroom-sandbox/config/prompts/README.md`](https://github.com/Exios66/local-mailroom-sandbox/blob/main/config/prompts/README.md).

Sorter smoke / some Modal sorter runs use local classification variants
(`sorter_reviewer_local_v0`, `judge_local_v0`) — distinct from eval-environment
`sorter_v1`. See sandbox README § “Local 7B/8B smoke variants”.

## GEPA iteration & provenance (implementation repos)

| Concern | Repository |
| --- | --- |
| Mutation loop, gates, `prompt_engineer.py` | [`eval-environment`](https://github.com/LLM-Mailroom-Services/eval-environment) |
| Modal eval injection, lineage sha locks | [`local-mailroom-sandbox`](https://github.com/Exios66/local-mailroom-sandbox) |
| Historical GEPA board / entity-extraction prompt versions | [`llm-entity-extraction`](https://github.com/Exios66/llm-entity-extraction) (`.opencode/agents/PROMPT_ENGINEER_GEPA_PROVENANCE.md`) |
| Live pipeline templates & Langfuse | [`llm-mailroom`](https://github.com/Exios66/llm-mailroom) |

**Agent specialty:** for run-failure diagnosis and prompt-version issues spanning
llm-entity-extraction + llm-mailroom, triage issues here but invoke the
`prompt-engineer` subagent (see [AGENTS.md](../AGENTS.md)).

## Issue routing

- **Cross-repo prompt freeze / alignment / promotion policy** → this hub (epic or RFC).
- **Single-repo prompt edits** → eval-environment (mutations), sandbox (local stems),
  or llm-mailroom (production templates) — link back to the hub epic.

See [ROUTING.md](ROUTING.md).
