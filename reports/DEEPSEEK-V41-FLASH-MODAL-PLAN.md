# DeepSeek-V4.1-Flash on Modal + vLLM — planning runbook

_Planning only · fixes [mailroom-issues#225](https://github.com/LLM-Mailroom-Services/mailroom-issues/issues/225) · **SPEND-GATED** — no Modal deploy, no billed smoke, no invented Modal quality or $/doc figures_

## Purpose

Self-hosting **`deepseek-ai/DeepSeek-V4.1-Flash`** on Modal with vLLM is a **different GPU tier** than SAND-032 (Qwen3-8B-AWQ on 1–2×L4). This document records open-weight identity, VRAM topology, a draft vLLM flag posture, API baselines from the hub, and **empty** Modal evaluation cells aligned with the next-GPU-tier protocol ([#224](https://github.com/LLM-Mailroom-Services/mailroom-issues/issues/224) · [`reports/NEXT-GPU-TIER-PROTOCOL.md`](NEXT-GPU-TIER-PROTOCOL.md) — on `main` after [#226](https://github.com/LLM-Mailroom-Services/mailroom-issues/pull/226) merges; until then use that path on branch `docs/next-gpu-tier-protocol-224`).

**Topology and Modal $/hr (base, no region multiplier)** are cited from the hub attachment `DEEPSEEK-LLAMA-QWEN-COST-TOPOLOGY.md` (compiled 2026-09-27) and [Modal pricing](https://modal.com/pricing) as referenced there — not re-measured in this PR.

## Hard spend gate

| Requirement | Status |
| --- | --- |
| Explicit human go from **Jack** | **Not granted** — issue carries `attention/blocked` |
| Modal wallet authorization | **Not granted** |
| Written **$/hr cap** on the tracking issue | **Required before first deploy** — propose cap in #225 thread when go is requested |
| Pre-spend checklist from [NEXT-GPU-TIER-PROTOCOL.md](NEXT-GPU-TIER-PROTOCOL.md) | **Incomplete** — planning doc only |

**No Modal API calls, deploys, or GPU burn** are authorized by this file. Implementation runbooks live in `Exios66/local-mailroom-sandbox` after go; exports return here via `export_hub_reports.py`.

**Idle warm burn:** base fleet rates below are **~31× (4×B200)** and **~45× (8×H200)** higher than a single L4 at **~$0.80/GPU-h** — the same cold-vs-warm lesson as [MODAL-VLLM-GPU-REPORT.md](MODAL-VLLM-GPU-REPORT.md), amplified. Region multipliers **1.15–1.75×** apply on top of base $/hr.

## Why not L4 (Qwen topology does not transfer)

| Fact | Implication |
| --- | --- |
| Sparse MoE **~552B** backbone; **8B active (prefill) / 16B active (decode)**; Engram ~196B sparse memory | Active FLOPs resemble a small dense model; **weight residency** does not |
| Checkpoint **~511 GB** on disk (native **MXFP4** routed experts + **MXFP8** elsewhere — not AWQ) | Does **not** fit 1×L4, 2×L4, A10, or single-H100 80GB production paths |
| vLLM recipe **`vram_minimum_gb: 614`** (= checkpoint × 1.2 headroom) | Plan **4×B200** (primary) or **8×H200** (fallback); do **not** port SAND-032 1–2×L4 YAML without a new VRAM plan |
| Measured mailroom Modal leg is **Qwen3-8B-AWQ** only | [MASTER-REPORT.md](MASTER-REPORT.md) §3 — no DeepSeek Modal cells exist |

### GPU topology summary (planning)

| Topology | Aggregate HBM | Fits 614 GB floor? | Modal base $/hr (no region mult.) |
| --- | ---: | --- | ---: |
| **4×B200** | 720–768 GB | Yes (recipe path) | **$25.00** (4 × $6.250) |
| **8×H200** | 1,128 GB | Yes (recipe; Engram CPU offload common) | **$36.32** (8 × $4.540) |
| 8×H100 80GB | 640 GB | Marginal on paper — **no published vLLM recipe; do not plan** | $31.59 |
| 1×L4 / 2×L4 | 24–48 GB | **Impossible** | ~$0.80 / ~$1.60 |

With region multiplier 1.15–1.75×: 4×B200 ≈ **$28.75–$43.75/hr**; 8×H200 ≈ **$41.77–$63.55/hr**.

## Open-weight checkpoint (scope #225 §1)

| Field | Value |
| --- | --- |
| Hugging Face repo | [`deepseek-ai/DeepSeek-V4.1-Flash`](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) |
| License | **MIT** |
| OpenRouter slug (API leg) | `deepseek/deepseek-v4.1-flash` |
| Released | 2026-09-10 (DeepSeek + HF + OpenRouter) |
| Hub revision pin for **Modal** | **Not pinned in this plan** — record the resolved HF revision in the first deploy issue after go; do **not** invent a commit SHA here |

Retired aliases (`deepseek-v4-flash`, `deepseek-v4-flash-vision-exp`) route to V4.1-Flash on OpenRouter.

## API baselines (hosted — not Modal)

All figures below are from [MASTER-REPORT.md](MASTER-REPORT.md) (eval-environment / OpenRouter). API draws use the eval-environment corpus pin documented in that report; **do not** treat them as paired to Modal `ed7576b6` rows without the cross-leg caveats in [COST-COMPARISON-MODAL-VS-API.md](COST-COMPARISON-MODAL-VS-API.md).

### Specialist extraction (n = 20)

| Class | DeepSeek score | $/doc (API) | Cheapest among measured N=20 models on this class? |
| --- | ---: | ---: | --- |
| Correspondence | 0.4419 | $0.00060 | **Cheapest $**; Qwen3-8B scores higher (0.5130) |
| Insurance claims | **0.7974** | $0.00067 | **Best score and cheapest $** among N=20 legs |
| Corporate records | **0.4415** | $0.00098 | **Best score and cheapest $** among N=20 legs |
| Contracts | 0.5137 | $0.0025 | Qwen3-8B higher score (0.6169); DeepSeek cheaper $ |
| Merger agreements | 0.2423 | $0.0038 | Granite higher score; DeepSeek not quality leader |

**Cost across five specialist N=20 tasks:** DeepSeek total **$0.171** vs $0.324 (Qwen3-8B as filed) and $0.349 (Granite) — cheapest on **all five** specialist $/doc cells; quality leadership on **insurance** and **corporate** at n = 20.

### LLM sorter (API)

| Run | n | Class accuracy | Subclass accuracy | $/doc |
| --- | ---: | ---: | ---: | ---: |
| `20260927T101544Z-eval-classification` | 100 | **95%** | 64% | $0.0010 |

Use API sorter numbers only for **quality/cost baselines** until a Modal sorter cell exists under the same prompt lock as eval #19/#20 (see [MASTER-REPORT.md](MASTER-REPORT.md) audit notes).

## Serving posture (draft — planning text only)

Mirror SAND-032 **discipline** (frozen prompts, thinking off for JSON extraction, guided JSON) on a **heavier replica** — not the L4 engine bundle.

### Container / image (reference)

| Knob | Planned value | Notes |
| --- | --- | --- |
| Image | `vllm/vllm-openai:nightly` with **vLLM ≥ 0.30.0** | Architecture support landed 2026-09-10 |
| Weights | `deepseek-ai/DeepSeek-V4.1-Flash` | Native MXFP4/MXFP8 checkpoint |
| Mailroom text-only | `--language-model-only` | Drops ViT; frees VRAM for KV |
| Tokenizer / parsers | `--tokenizer-mode deepseek_v41`, `--tool-call-parser deepseek_v41`, `--reasoning-parser deepseek_v41` | Per vLLM recipe |
| Reasoning | **`thinking: false`** (or explicit budget) on extraction JSON | Default thinking-on inflates completions |
| Ready timeout | `VLLM_ENGINE_READY_TIMEOUT_S=3600` | Long first load |
| Context cap | `max_model_len` **16k–32k** for mailroom windows | Not 1M context for eval |
| Concurrency | Client **c = 8** initially (match API legs); raise only after warm smoke | Same lesson as scale-matrix / run-50 |
| `max_num_seqs` | Start **32–128**; tune under Axis B | Do not copy L4 `max_num_seqs` 16 blindly |

### Modal fleet (primary vs fallback)

**Primary — cost-lean Blackwell**

- `gpu=B200:4`, tensor parallel **TP4**
- Engram CPU offload per vLLM recipe defaults
- `scaledown_seconds`: **120** (attended) or **600** (unattended) — same policy choices as DMR-076 / run-50

**Fallback — Hopper**

- `gpu=H200:8`, **TP8**
- Engram CPU offload; identical mailroom flags otherwise

**Do not deploy:** L4, A10, single-H100, or 8×H100 without a published recipe and explicit VRAM proof.

### Cold start expectations

- First boot: **many minutes** to **≥1 h** (recipe 3600 s ready timeout; FlashInfer autotune can dominate first boot on some SKUs).
- Budget fleet idle time under cap — SAND-032 showed **19%** of ledger on non-run fleet time at **$2.80 / $5.00** on L4; expect higher **$/hr** sensitivity on B200/H200.

## Modal evaluation map — protocol [#224](NEXT-GPU-TIER-PROTOCOL.md)

When spend is authorized, run cells in **Axis B → Axis A → five-class sweep** order. Until then, cells are **PLANNED** with API quality/$ as **reference only** (right column). **Modal $/doc, wall, tok/s, and quality cells stay empty.**

**Program label (proposed):** `SAND-0xx-deepseek-v41` · **SKU:** B200:4 (primary) · **Data pin for Modal:** `ed7576b6…` / `ground_truth` / `all`, seed **42**, nested **20 ⊂ 50 ⊂ 100**

### Axis B — serving ladder (1× fleet = 4×B200 container)

Correspondence **n = 20**, replicas fixed at one 4×B200 deployment. Climb L0→L5 **analog** (thinking off, graphs, seq caps) — exact rung names to be defined in sandbox before spend.

| Rung | Knob summary | Wall | tok/s per GPU | $/doc | $/1M tok | Quality | API ref (n=20) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| L0 | baseline nightly + minimal flags | — | — | — | — | — | score 0.4419 · API $0.00060 |
| L5-equiv | frozen mailroom posture (thinking off, LM-only, JSON) | — | — | — | — | — | same |

_L4 reference for shape only:_ L0→L5 cut $/1M tokens ~44% at 1×L4 ([NEXT-GPU-TIER-PROTOCOL.md](NEXT-GPU-TIER-PROTOCOL.md) Axis B) — **do not** assume the same delta on MoE Blackwell.

### Axis A — scale-out (posture frozen at L5-equivalent)

Hold serving knobs; vary **replica count** only if Modal exposes multiple 4×B200 containers with balanced routing. Many heavy checkpoints use **one multi-GPU container** — Axis A may be **N/A** or “1 container vs 2 containers” rather than 1×L4 vs 2×L4; document the actual Modal deployment shape in the sandbox runbook.

| Replicas | Fleet | Wall | tok/s per GPU | $/doc | $/1M tok | Quality | Notes |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 4×B200 | — | — | — | — | — | Primary topology |
| 2 | 2×(4×B200) | — | — | — | — | — | Only if router balance proven |

### Five-class sweep (n = 50, frozen posture)

| Class | Modal quality | Modal $/doc | Modal run id | API DeepSeek (n=20) score | API $/doc |
| --- | ---: | ---: | --- | ---: | ---: |
| Correspondence | — | — | — | 0.4419 | $0.00060 |
| Insurance claims | — | — | — | **0.7974** | $0.00067 |
| Corporate records | — | — | — | 0.4415 | $0.00098 |
| Contracts | — | — | — | 0.5137 | $0.0025 |
| Merger agreements | — | — | — | 0.2423 | $0.0038 |

**Sorter (separate track):** API n=100 class **95%** — Modal cell **PLANNED**; compare only after prompt/shape lock with API classification leg.

### L4 contrast (measured — why API→Modal break-even differs)

| Surface | L4 Modal (measured) | DeepSeek Modal |
| --- | --- | --- |
| Insurance specialist n=50 | 0.6881 @ $0.00054 (`sand032-s3-insurance50`) | **UNMEASURED** |
| Fleet $/hr | ~$1.60 (2×L4) | ~$25 (4×B200 base) |
| $/doc on heavy checkpoint | See [COST-COMPARISON-MODAL-VS-API.md](COST-COMPARISON-MODAL-VS-API.md) | **UNMEASURED** — topology $/hr only |

Modal $/doc for DeepSeek remains **UNMEASURED** until a serving smoke exists; do not scale Qwen L4 $/doc linearly by hourly ratio.

## Issue #225 scope checklist

- [x] Confirm open-weight HF: `deepseek-ai/DeepSeek-V4.1-Flash` (MIT); revision pinned at deploy time, not in this plan
- [x] Draft Modal deploy + vLLM flags runbook (4×B200 primary, 8×H200 fallback) — **planning text only**
- [x] Map API baselines → expected Modal cells under [#224](NEXT-GPU-TIER-PROTOCOL.md) protocol — **PLANNED** cells, no fabricated Modal scores
- [x] Explicit **SPEND-GATED** gate documented — **no deploy until Jack authorizes $/hr cap**

## Related

| Item | Link |
| --- | --- |
| Next GPU tier protocol | [`reports/NEXT-GPU-TIER-PROTOCOL.md`](NEXT-GPU-TIER-PROTOCOL.md) ([#226](https://github.com/LLM-Mailroom-Services/mailroom-issues/pull/226)) |
| Topology brief (attachment) | `DEEPSEEK-LLAMA-QWEN-COST-TOPOLOGY.md` (hub session attachment, 2026-09-27) |
| vLLM recipe | https://recipes.vllm.ai/deepseek-ai/DeepSeek-V4.1-Flash |
| SAND-032 L4 baseline | [MODAL-VLLM-GPU-REPORT.md](MODAL-VLLM-GPU-REPORT.md) |

## Version

| Field | Value |
| --- | --- |
| Document version | 1.0 |
| Issue | [#225](https://github.com/LLM-Mailroom-Services/mailroom-issues/issues/225) |
| Hub reports context | per [reports/README.md](README.md) provenance block |
