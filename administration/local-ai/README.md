# local AI administration experiments

Experiment record: 2026-10-21 (America/Chicago). This records observations from interactive testing on Aso, not a declaration that the agents are production services. UTC logs can show 2026-10-22 for the same evening.

- [Hermes Agent](hermes.md) — setup, homelab work, memory/skills, inference failures, and lessons
- [Odysseus](odysseus.md) — setup, tool execution, routing diagnosis, local patches, and remaining work
- [Workstation inventory](../../hosts/workstations.md) — hardware source of truth

## scope and boundary

Aso remains a personal administration workstation. Fujigoko services must continue without it or either agent. Gusuku remains disposable; useful experiments are rebuilt on Fujigoko rather than making production depend on the lab.

The agents can help inspect documentation, propose plans, execute authorized diagnostics, and prepare reviewed changes. A local model is not an authority on host state. Distinguish repository claims, direct tool results, user-supplied evidence, and assumptions. Container readiness does not prove application correctness, backup recoverability, or disk health.

These dated records preserve failures and corrections. They do not replace the live inventories, service records, or recovery runbooks. Re-read those files and verify live state when needed. Do not copy changing findings into permanent memory as timeless facts.

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

## next work

1. Verify the server's serving window and both clients' effective budgets with authenticated discovery or an explicit supported override.
2. Make Odysseus tool availability and repo workspace access reliable without prompt vocabulary workarounds.
3. Verify memory/skill persistence in a new session, including behavior when vector retrieval is unavailable.
4. Retest a small representative administration task end to end before expanding autonomy. Backup implementation remains separate work requiring app-consistent methods and restore verification.
