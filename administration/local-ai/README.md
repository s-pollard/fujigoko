# local AI administration experiments

Experiment records: 2026-10-21 through 2026-10-23 (America/Chicago). This records observations from interactive testing on Aso, not a declaration that the agents are production services. UTC logs can show the following date for the same evening.

- [Evaluation roadmap](evaluation-roadmap.md) — 24 tasks, revised variants, comparison rules, and model/framework scoring
- [First 27B pilot](results/2026-10-23-qwen-27b-pilot.md) — original 22 attempts, fresh-chat reruns of 5–9, review corrections and coverage limits
- [Evaluation protocol](evaluation-protocol.md) — fixture validation, memory/session controls, analysis versus execution, and scoring
- [Run record template](evaluation-run-template.md) — repeatable per-attempt evidence and settings record
- [Hermes Agent](hermes.md) — setup, homelab work, memory/skills, inference failures, and lessons
- [Odysseus](odysseus.md) — setup, tool execution, routing diagnosis, local patches, and remaining work
- [Workstation inventory](../../hosts/workstations.md) — hardware source of truth

## scope and boundary

Aso remains a personal administration workstation and the temporary evaluation test bed until the move. Fujigoko services must continue without it or either agent. Gusuku remains disposable; useful experiments are rebuilt on Fujigoko rather than making production depend on the lab.

The agents can help inspect documentation, propose plans, execute authorized diagnostics, and prepare reviewed changes. A local model is not an authority on host state. Distinguish repository claims, direct tool results, user-supplied evidence, and assumptions. Container readiness does not prove application correctness, backup recoverability, or disk health.

These dated records preserve failures and corrections. They do not replace the live inventories, service records, or recovery runbooks. Re-read those files and verify live state when needed. Do not copy changing findings into permanent memory as timeless facts.

## inference direction — 2026-10-23

Local inference is the intended deployment model for the ongoing homelab helper. Paid model API inference is not an acceptable ongoing option for this use case; do not treat it as the default backend or a required fallback. API-assisted testing has incurred at least $4.71 so far; this is a reported lower bound, not a final usage total or monthly estimate.

Current evaluation constraints:

- test now on Aso's existing RX 7900 XTX (24 GB); the RTX 3060 Ti is not currently accessible
- evaluate models and context budgets that could fit a prospective RX 9060 XT **16 GB**
- the RX 9060 XT is a candidate, not a confirmed purchase, and its performance has not been measured
- select for reliable tool calls, Linux/Docker/network/backup troubleshooting, production/test separation, verification, and clear reporting of incomplete checks
- fitting weights in VRAM does not establish usable context capacity or reliable administration behavior
- the current 27B setup is not evidence that the same configuration fits a 16 GB GPU

No replacement model has been selected. Use the completed Paperless restore work as a representative evaluation task, with isolated tests and objective checks. Local inference does not imply that every optional search or other external tool is offline; assess those tool dependencies separately.

## shared inference setup observed during testing

| Component | Observed setup |
| --- | --- |
| Workstation | Aso; Arch Linux, KDE Plasma/Wayland |
| CPU / RAM | Ryzen 7 7800X3D; 32 GB RAM |
| GPU | Radeon RX 7900 XTX; approximately 24 GiB VRAM |
| Model | Qwen3.8-27B-UD-Q4_K_M GGUF; approximately 17.3 GB download |
| Inference | Hermes-managed llama.cpp Vulkan build b11671 |
| Serving window | Worker command line showed `--ctx-size 65536` |
| Cache / acceleration | Q8 K/V cache, flash attention, draft-MTP observed in the worker arguments |

Odysseus was pointed at the existing local OpenAI-compatible inference service. This is Odysseus running its own agent against llama.cpp, not a verified Odysseus-to-Hermes-agent integration. Stopping the inference server interrupts either client. Two llama-server processes were the model router and its worker, not evidence of duplicate model loads.

Generation logs and UI counters showed roughly 50–70 tokens/second in different tasks. Discrete VRAM usage was observed around 21.4 GiB during a model run. These are informal observations, not comparable benchmarks: prompt length, caching, reasoning, speculation, tool rounds, and concurrent work differ. UI cumulative input totals can count repeated history across calls and should not be interpreted as one request's context size.

## operating lessons

- Require actual tool-call records before accepting claims that commands ran or files were read. Model self-identification is not reliable endpoint identification.
- Local inference still has input, output, and context token limits. Reasoning consumes output capacity and compute even without per-token API billing.
- GPU activity after a visible answer can be an auxiliary task, background review, compression, or continued generation. Inspect agent and inference logs rather than infer a cause from utilization alone.
- Use scoped tasks and bounded output. Reading every document repeatedly produced large cumulative input and slow orientation turns.
- Shell access is not a read-only sandbox. A prompt restriction does not technically remove the account's ability to change hosts or use Docker.
- Review diffs and changed-file lists and run `git diff --check`. A clean whitespace check does not establish factual correctness.
- Follow [SECURITY.md](../../SECURITY.md). Keep credentials, key locations/material, exact addressing, management endpoints, raw private logs, and identifying device metadata outside this public repo.

## repository workflow

`main` is the shared accepted documentation for both agents. Hermes and Odysseus have separate documents, not permanent agent-specific branches. Use a short-lived task branch for work that needs review, merge it after verification, then remove the completed branch. Keep the local checkout synchronized with `main` before another task. Do not let both agents edit the same checkout concurrently; use separate worktrees when parallel work is intentional.

Changes to an agent's own upstream source belong in that project's checkout; this repository records their purpose, tested behavior, and remaining limitations.

## latest follow-up — 2026-10-23

The user ran a Hermes + Qwen 27B pilot on low reasoning covering the original 22 task IDs. Original tasks 5–9 shared a chat and were subsequently rerun with fresh-chat instructions; persistent memory/skills and exact runtime settings were not controlled. Strengths were scope restraint, concrete inventory and the reported isolated edit. Weaknesses included unsupported certainty, invented or stretched evidence, and excessive repository auditing. Most diagnostic tasks used supplied snapshots/fixtures rather than model-executed host/API checks. The reviewer also corrected a Loki timestamp assumption after inspecting source. See the [pilot report](results/2026-10-23-qwen-27b-pilot.md); this is not a completed controlled baseline or a live host audit.

The roadmap now retains tasks 1–22 and adds execution-host verification (23) and conflicting-evidence/memory handling (24). Complete reviewed fixtures and missing execution coverage before smaller-model comparisons. No new production changes, deployment readiness or GPU fit were established.

## earlier follow-up — 2026-10-22

Aso's Fujigoko checkout was fast-forwarded to the consolidated `main`. Odysseus then demonstrated direct workspace file reads, creation and editing, cross-chat memory retrieval, and answering from a pinned homelab boundary without tools. A further local source patch added memory to the workspace toolset. A read-only Markdown target-file check executed and reported no missing targets. Private Tailscale Serve access was configured; external-client connectivity is not yet verified. See the [dated Odysseus follow-up](odysseus.md#follow-up--2026-10-22) for evidence and remaining limitations.

## next work

Evaluation priority: prepare frozen prompts/reference answers and controlled profiles using the [evaluation protocol](evaluation-protocol.md), then complete missing/invalid 27B coverage and new tasks 23–24. Keep pilot attempts and reviewer corrections separate from subsequent comparisons.

1. Verify the server's serving window and both clients' effective budgets with authenticated discovery or an explicit supported override.
2. Harden Odysseus tool selection across turns and wording. Explicit workspace read/create/edit access now passes; broad intent filtering remains an issue.
3. Improve automatic memory relevance and duplicate handling. Cross-chat memory-tool retrieval and pinned-rule recall now pass; skill persistence remains untested.
4. Verify unattended startup, cancellation, and off-LAN access end to end. Tailscale Serve is configured, but an actual remote-client test has not been reported.
5. Continue with scoped administration tasks. A local Markdown target-file check ran successfully; backup implementation remains separate work requiring app-consistent methods and restore verification.

