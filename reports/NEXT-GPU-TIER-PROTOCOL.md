# Next GPU tier evaluation protocol

_Repeatable methodology to compare any future Modal GPU SKU against the SAND-032 L4 baseline · documentation only · fixes [mailroom-issues#224](https://github.com/LLM-Mailroom-Services/mailroom-issues/issues/224)_

## Purpose

Any upgrade path (more L4 replicas, a larger single-GPU SKU, or a multi-GPU topology for a heavier checkpoint) must be measured the same way SAND-032 measured Qwen3-8B-AWQ on Modal L4. This protocol defines corpus pins, draw structure, mandatory metrics, and two **independent** experimental axes so AMFAM and internal reports can read “more GPUs” and “better serving” without conflating them.

**L4 reference reports (numbers cited here come only from these files):**

| Report | Use for |
| --- | --- |
| [MODAL-VLLM-GPU-REPORT.md](MODAL-VLLM-GPU-REPORT.md) | Setup, metric definitions, Axis A (§6) and Axis B (Stage 1 ladder, §3.1), spend ledger |
| [COST-COMPARISON-MODAL-VS-API.md](COST-COMPARISON-MODAL-VS-API.md) | Per-class $/doc and quality at n = 50 on `ed7576b6`, busy-window costing |
| [MASTER-REPORT.md](MASTER-REPORT.md) | Cross-leg headline scores, five-class sweep table, ladder summary |

**Heavy-GPU / DeepSeek-class planning** (spend-gated, no Modal burn in that track): [mailroom-issues#225](https://github.com/LLM-Mailroom-Services/mailroom-issues/issues/225). Optional topology and VRAM-floor notes for cost posture only — not measured Modal quality — appear in hub attachments such as `DEEPSEEK-LLAMA-QWEN-COST-TOPOLOGY.md`; do not treat those as SAND-032-comparable results.

## Hard spend gate

- **No Modal GPU spend** for a new SKU or replica count without: (1) explicit human go from Jack, (2) wallet authorization on the Modal account, and (3) a written cap and pre-spend checklist (below) attached to the tracking issue.
- SAND-032 operated under a **$5.00 program cap** and closed at **$2.80** fleet-window ledger ([MODAL-VLLM-GPU-REPORT.md](MODAL-VLLM-GPU-REPORT.md) Summary). New tiers must declare their own cap before the first deploy.
- This document does **not** authorize deploys. Implementation and runbooks live in `Exios66/local-mailroom-sandbox`; exports land back in `mailroom-issues/reports/` via `export_hub_reports.py`.

## Corpus and data identity

| Field | Value |
| --- | --- |
| Dataset | Public Hugging Face [`Lucius-Morningstar/mailroom-dataset`](https://huggingface.co/datasets/Lucius-Morningstar/mailroom-dataset) |
| Config | `ground_truth` |
| Split | `all` |
| Corpus size | **3,302** documents (full split) |
| RNG seed | **42** (same as SAND-032) |
| Nested draws | **20 ⊂ 50 ⊂ 100** — the 20-document subset must be contained in the 50-document subset, which must be contained in the 100-document subset, per class and program stage ([MODAL-VLLM-GPU-REPORT.md](MODAL-VLLM-GPU-REPORT.md) §1) |

### Pin rules (authoritative vs hub tag)

- **Authoritative pin:** parquet **data revision** SHA **`ed7576b6…`** (full hash in run headers and hub tables as `ed7576b6`). All L4 baseline $/doc and quality cells in the hub reports use this revision.
- **Acceptable load:** `revision="v9.1"` **or** the data SHA above — eval loaders must resolve to the same parquet rows as `ed7576b6`.
- **Eng Ops clarification:** the hub tag `v9.1` tip commit may be **README-only** (e.g. tip `bc9eab28…`). **Do not require** hub tag tip SHA == parquet data SHA. Record both in the run header when they differ; gate comparisons on the **data** SHA and document IDs, not on tag tip.
- **Do not** compare against API-leg draws on revision `46a4d3c2` / train split as if they were paired; [COST-COMPARISON-MODAL-VS-API.md](COST-COMPARISON-MODAL-VS-API.md) §1 and §6 state the legs differ by revision and split.

## Metrics dictionary

Definitions match [MODAL-VLLM-GPU-REPORT.md](MODAL-VLLM-GPU-REPORT.md) §1 unless noted.

| Metric | Definition | Report in every cell |
| --- | --- | --- |
| **Wall** | Batch wall time (seconds), first request admitted through last response | Yes |
| **tok/s** | Throughput; for cross-SKU comparison report **tok/s per GPU** (aggregate tok/s ÷ GPU count) | Yes |
| **$/doc** | **Busy-window GPU $** ÷ completed documents | Yes |
| **$/1M tokens** | Busy-window GPU $ ÷ (prompt + completion tokens) × 10⁶; on a fixed SKU hourly rate this tracks 222.2 ÷ (tok/s per L4) for L4 at $0.80/h — substitute the new SKU’s $/GPU-h in the same formula | Yes |
| **Quality by class** | Task-specific score on the same metric SAND-032 used (see table below) | Yes |

**Cost bases (secondary columns, not optional for program closeout):**

- **Busy-window GPU $** = wall × replicas × ($/GPU-hour ÷ 3600). SAND-032 L4: **$0.80/GPU-h** ([MODAL-VLLM-GPU-REPORT.md](MODAL-VLLM-GPU-REPORT.md) §1). Primary basis for $/doc and $/1M tokens in hub tables.
- **Billed GPU $** = (wall + cold boot) × replicas × rate — lower bound on Modal invoice for the run.
- **Fleet-window ledger** — program total including idle between runs (SAND-032: $2.80 on $5.00 cap).

**Quality metrics by document class** (match [MASTER-REPORT.md](MASTER-REPORT.md) five-class sweep):

| Class | Primary quality metric |
| --- | --- |
| Correspondence | Overall extraction score |
| Insurance claims | Overall extraction score |
| Corporate records | Overall extraction score |
| Contracts | CUAD clause-detection micro-F1 |
| Merger agreements | MAUD per-question micro accuracy |

Record **docs ok / docs attempted**, schema validity if scored, and p50/p95 latency when the sandbox export provides them (SAND-032 did for scale-out and ladder runs).

**Utilization evidence:** SAND-032 did not sample SM utilization; **client-slot occupancy** and **tok/s per GPU** are the required proxies until DCGM/`nvidia-smi` sampling is added ([MODAL-VLLM-GPU-REPORT.md](MODAL-VLLM-GPU-REPORT.md) §5–§7).

## Two axes — never conflate

Treat **Axis A** and **Axis B** as separate experiments. Do not merge replica count and serving-knob changes into one “configuration” column without labeling which axis moved.

### Axis A — 1→N replica scale-out (“more GPUs”)

**Question:** If serving posture is held fixed, does adding replicas reduce wall time without raising $/doc?

**Design:**

- Hold the **frozen serving posture** constant (for L4 baseline: SAND-032 **L5** — `awq_marlin`, fp8 KV, thinking off, CUDA graphs on, `max_num_seqs` 16, `max_inputs` = `max_num_seqs` per container).
- Hold **client concurrency = replicas × per-replica admission** (SAND-032: 8 per L4 on the 1× vs 2× correspondence comparison).
- Vary only **replica count** (e.g. 1× → 2× on the same SKU).
- Use the **same document IDs** at n = 100 for the paired comparison (correspondence in SAND-032).

**L4 baseline facts** ([MODAL-VLLM-GPU-REPORT.md](MODAL-VLLM-GPU-REPORT.md) §6.1, [MASTER-REPORT.md](MASTER-REPORT.md) §3):

| Metric | 1×L4 · c8 | 2×L4 · c16 |
| --- | ---: | ---: |
| Wall | 95.0 s | 46.1 s (**2.06×** faster) |
| tok/s per L4 | 2,579 | 2,654 |
| $/1M tokens | $0.0862 | $0.0837 |
| $/doc | $0.00021 | $0.00021 (flat) |
| Quality (score) | 0.2886 | 0.2966 |

**Routing gate:** Second replica helps only if Modal’s router balances load (`max_inputs` 32 at c64 → 51/49 split, 3,141 tok/s per L4). Imbalance (`max_inputs` 64 → 97/3) **worsens** $/1M tokens 3.2× ([MODAL-VLLM-GPU-REPORT.md](MODAL-VLLM-GPU-REPORT.md) Summary, §6.1).

#### Axis A reporting template (fill per SKU)

**Program:** _e.g. SAND-0xx_ · **SKU:** _e.g. L4 / H100 / B200:4_ · **Posture:** _frozen rung name_ · **Class:** _e.g. correspondence_ · **n:** _100_ · **Data:** `ed7576b6…`

| Replicas | Fleet label | Wall (s) | tok/s per GPU | $/doc | $/1M tok | Quality | Req/replica split | Notes |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1 | | | | | | | | |
| 2 | | | | | | | | |
| N | | | | | | | | |

**Checklist — Axis A complete when:**

- [ ] Same document IDs as the 1-replica row
- [ ] Serving knobs identical across rows
- [ ] Router balance logged (requests per replica)
- [ ] All five mandatory metrics present per row

### Axis B — Serving-knob ladder (“better serving”)

**Question:** At fixed replica count, how much do engine/router knobs move $/1M tokens and wall without changing GPU count?

**Design:**

- Hold **replica count fixed** (SAND-032 Stage 1: **1×L4**, correspondence **n = 20**, **c8**).
- Climb rungs **L0 → L5** (or the SKU-specific ladder documented in the sandbox before spend). L0→L5 on L4 is the reference shape: thinking off, marlin, seqs, CUDA graphs, etc. ([MODAL-VLLM-GPU-REPORT.md](MODAL-VLLM-GPU-REPORT.md) §3.1 table).
- **Same 20 documents every rung** (nested draw).

**L4 baseline facts** (correspondence n = 20, 1×L4 · c8; [MODAL-VLLM-GPU-REPORT.md](MODAL-VLLM-GPU-REPORT.md) §3.1):

| Rung | tok/s per L4 | $/1M tokens | $/doc |
| --- | ---: | ---: | ---: |
| L0 · baseline | 1,261 | $0.176 | $0.00035 |
| L5 · frozen config | 2,238 | $0.099 | $0.00020 |

**~44% reduction** in $/1M tokens from L0 to L5 at equal quality band (MASTER-REPORT: L5 cut wall ~43.6% and $/doc ~43.5% vs L0 at ~0.28 overall score).

#### Axis B reporting template

**Program:** _·_ **SKU:** _·_ **Replicas:** _1_ · **Class:** correspondence · **n:** _20_ · **Data:** `ed7576b6…`

| Rung | Knob summary | Wall (s) | tok/s per GPU | $/doc | $/1M tok | Quality | Notes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| L0 | | | | | | | |
| L1 | | | | | | | |
| L5 | | | | | | | |

**Checklist — Axis B complete when:**

- [ ] Replica count unchanged across rungs
- [ ] Document set identical (20 doc IDs logged)
- [ ] Quality recorded per rung (flag regressions before wider n = 50 / 100 sweeps)

### Five-class sweep (after axes A and B on correspondence)

Mirror SAND-032 Stage 3: **2×** (or chosen production replica count) at the **frozen L5-equivalent posture**, **n = 50** per class, nested inside n = 100 where applicable. Report every cell with the five metrics plus class-specific quality.

**L4 baseline $/doc @ n = 50** ([COST-COMPARISON-MODAL-VS-API.md](COST-COMPARISON-MODAL-VS-API.md) §2, [MASTER-REPORT.md](MASTER-REPORT.md) §3):

| Class | Score (headline) | $/doc | Run id |
| --- | ---: | ---: | --- |
| Correspondence | 0.3004 | $0.00014 | `sand032-s3-corr50` |
| Insurance claims | 0.6881 | $0.00054 | `sand032-s3-insurance50` |
| Corporate records | 0.4583 | $0.00050 | `sand032-s3-corporate50` |
| Contracts | 0.6011 (overall) | $0.0022 | `sand032-s3-contracts50` |
| Merger agreements | 0.0830 (overall) | $0.0043 | `sand032-s5-merger50-maud` |

## Pre-spend checklist (new GPU SKU or replica count)

Complete **before** any Modal deploy or billed smoke test:

1. **Issue & cap:** Tracking issue linked to #224; program cap in USD; Jack go + wallet auth recorded in the issue thread.
2. **Data pin:** Loader tested offline against `ed7576b6…` / `ground_truth` / `all`; seed 42; nested ID lists for 20/50/100 generated and archived.
3. **SKU economics:** $/GPU-hour from [Modal pricing](https://modal.com/pricing) at commit time (do not extrapolate beyond published rates). For multi-GPU containers, document **aggregate** $/hr and **GPU count** in the run header.
4. **VRAM / topology:** Checkpoint fits with published recipe or sandbox deploy README; if only planning (e.g. DeepSeek-class), follow [#225](https://github.com/LLM-Mailroom-Services/mailroom-issues/issues/225) — no invented Modal $/doc or quality for unreleased SKUs.
5. **Axis plan:** Explicit schedule — Axis B ladder on 1 replica (correspondence n = 20) **before** Axis A scale-out at frozen posture; five-class sweep only after L5-equivalent frozen.
6. **Routing:** `max_inputs` = `max_num_seqs`; client concurrency = replicas × admission; router balance in acceptance criteria.
7. **Exports:** Run reports + `hub_data.json` path agreed; hub regenerate command in [reports/README.md](README.md) for PR back to `mailroom-issues`.
8. **Abort rules:** Cold-boot timeout, max wall per stage, and “stop if ledger > X% of cap” defined up front (SAND-032 aborted sorter cost $0.08 — [MODAL-VLLM-GPU-REPORT.md](MODAL-VLLM-GPU-REPORT.md) §2).

## Program closeout

- Regenerate hub markdown into this repo; cross-check busy-window $ against run headers (see MASTER-REPORT audit notes for `sand032-s5` / `sand032-s6` boot vs busy basis).
- Update [MODAL-VLLM-GPU-REPORT.md](MODAL-VLLM-GPU-REPORT.md) only via sandbox export — do not hand-edit generated tables here.
- Link the program issue from AMFAM or stakeholder one-pagers when those beats reference GPU tier comparisons.

## Version

| Field | Value |
| --- | --- |
| Protocol version | 1.0 |
| L4 baseline program | SAND-032 |
| Hub reports commit context | local-mailroom-sandbox @ 95d89fa8f401 (per report headers) |
