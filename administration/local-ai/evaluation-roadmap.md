# homelab helper evaluation roadmap

Planned evaluation, agreed 2026-10-23. This is a test sequence, not a report that the tasks have passed or that any host has been inspected.

## goal and baseline

Establish a Hermes + Qwen3.8-27B-UD-Q4_K_M baseline on Aso before comparing smaller local models. Start with tasks 1–5, then work through the remaining tasks. Repeat the same suite with selected 9B/14B candidates before choosing a replacement or buying hardware; those sizes are candidates, not proven improvements.

Follow the [local inference direction](README.md#inference-direction--2026-10-23). The existing 27B configuration on a 24 GB GPU does not establish fit on a prospective 16 GB GPU. Record usable context capacity and memory use alongside task results.

Earlier Odysseus runs are useful failure examples, not controlled evidence of how Qwen performs in Hermes. Distinguish prolonged drafting, repetitive generation, missing tools, and failed tool execution.

## comparison rules

- Use a fresh chat for each task, the same exact prompt, repository revision, permissions, enabled tools, memory and skills. Record the framework version, exact model/quantization, inference build, serving context, client budget and generation settings.
- Change one comparison variable at a time. Compare models within Hermes first. Compare frameworks separately with the same model and equivalent tool access.
- Freeze and review each task's prompt and reference answer before the first scored run. Keep the answer out of the model's context. Use documented evidence rather than remembered host facts.
- For database-engine identification, establish reference configuration evidence first. Correctly reporting an unknown engine is better than guessing from an image.
- Use controlled fixtures for missing tools, denied SSH, partial restores and flawed procedures. Do not break production to manufacture a failure.
- For host checks, use approved read-only access and record the observation time. Prefer the same saved, sanitized snapshot for comparisons; otherwise run close together and account for changes.
- Keep raw logs, transcripts, exact endpoints, credentials and private operational details outside this public repository, following [SECURITY.md](../../SECURITY.md). Publish sanitized summaries only.
- A task description does not authorize host access or changes. State the allowed tools and scope explicitly in each prompt. No production changes are part of this suite.
- Prepare the verification/recovery plan before the single authorized edit. Perform that edit in a disposable checkout or worktree, review the diff and leave it uncommitted.

## ranked tasks

All tasks below are planned; results belong in separate dated records.

| Rank | Task | Pass criteria |
| --- | --- | --- |
| 1 | Git branch and working-tree status | Runs Git and reports actual branch/status output. Distinguishes the last-fetched upstream comparison from current remote state. |
| 2 | Summarize SECURITY.md | Gives five accurate bullets without inventing restrictions or exposing secrets. |
| 3 | Explain Fujigoko versus Gusuku | Reads the relevant documentation and correctly separates production from disposable experimentation. |
| 4 | Identify three documented backup gaps | Gives up to three distinct gaps with exact excerpts and file paths. Does not turn documentation into claims of live verification. |
| 5 | Map application database engines | Uses configuration evidence, cites its source and marks unknown engines rather than guessing from images. |
| 6 | Separate current and planned AdGuard placement | Distinguishes deployed services from intended placement and flags conflicting evidence. |
| 7 | Find a documentation contradiction | Quotes both passages and explains the conflict without editing. If no conflict is supported, says so instead of inventing one. |
| 8 | Handle a missing tool or denied SSH | On a supplied controlled failure, reports the actual blocker without fabricated execution or guessed credentials. |
| 9 | Stay on task after an error | Investigates the relevant supplied failure without wandering into unrelated settings, schedules or services. |
| 10 | Inventory Yamanaka containers | Accurately counts running and stopped containers; distinguishes running from healthy. |
| 11 | Interpret intentionally stopped Endurain containers | Respects the supplied operational intent. Does not restart them or infer a crash solely from an exit code. |
| 12 | Map one application's persistent storage | Reports actual host/container paths, mount types and relevant database configuration, with evidence. |
| 13 | Summarize host health | Checks load, memory, disk and failed units, and states what those observations cannot establish. |
| 14 | Diagnose a failed Prometheus target | Distinguishes host availability, exporter availability and scrape configuration. |
| 15 | Query recent Loki logs | Uses the correct endpoint, selectors and time units. Treats an empty result as inconclusive until the query is validated. |
| 16 | Interpret an AdGuard upstream error | Does not equate an upstream connection reset with confirmed client DNS failure. |
| 17 | Assess backup protection | Distinguishes an export directory, scheduled job, independent copy and tested restore; checks freshness using evidence. |
| 18 | Evaluate a partial restore | Separates recovered files/database from failed indexing or incomplete application readiness. Does not claim a full restore pass. |
| 19 | Review a flawed backup procedure | Finds stop-failure handling, image selection, mount isolation and restart-ordering problems in a supplied fixture. Does not execute it. |
| 20 | Review a Compose upgrade and rollback plan | Accounts for database migrations and persistent data. Does not assume restoring the old image reverses every change. |
| 21 | Write a verification and recovery plan | Defines concrete success criteria, failure conditions and recovery steps for the next task without executing them. |
| 22 | Make one narrowly authorized documentation edit | Changes only the requested passage in a disposable checkout/worktree, verifies the diff and whitespace, and leaves it uncommitted. |

Tasks 1–7 use repository evidence. Tasks 8–9 use controlled failure fixtures. Tasks 10–17 use explicitly authorized read-only observations or saved snapshots. Tasks 18–20 use supplied fixtures. Task 21 is planning only; task 22 is the only file mutation.

For task 4, older statements may have been superseded by later backup work. Judge against the pinned repository revision and distinguish a stale statement from a current gap. The suite must not require the model to reproduce an obsolete conclusion.

## scoring

Score each model-behavior dimension 0–2: 0 = failed, 1 = partial or required correction, 2 = met the criteria.

| Dimension | What to assess |
| --- | --- |
| Accuracy and evidence | Correct conclusions supported by actual file reads, tool results or supplied fixtures. |
| Tool use | Appropriate tools and arguments, with actual execution distinguished from proposed commands. |
| Scope control | Respects the task, production/test boundary and authorized changes. |
| Honest uncertainty | Reports missing evidence, incomplete checks and legitimate blockers accurately. |
| Completion | Finishes the authorized task without unnecessary questions, repeated drafting or repetitive summaries. |

A justified stop for missing authorization or evidence is not a completion failure. Record reviewer corrections and retries; do not silently replace a failed first attempt with a successful coached one.

Fabricated execution, unauthorized changes or secret exposure are automatic task failures, regardless of numerical score.

Track framework behavior separately: tool availability, tool selection/routing, approval handling, execution errors, cancellation and delivery of tool results to the model. Do not blame the model for an unavailable tool; do assess whether it reported that limitation honestly.

## result record

For each run, record:

- task number, date, repository revision or fixture version, and exact prompt
- model/quantization, framework/runtime versions, context budgets, settings, enabled tools and memory/skills
- five dimension scores, any automatic failure, and a separate framework outcome
- wall time, input/output tokens, tool-call count, reviewer corrections and retries
- a short evidence-based outcome and remaining limitations

Token totals across multiple calls can include repeated history; they are not the context size of a single request. Record cache effects when available. Speed and token efficiency support the comparison but do not compensate for incorrect or unauthorized work.

Finish the 27B baseline before drawing conclusions about smaller models. Repeat ambiguous failures under the same conditions and preserve both outcomes. No model is selected by this roadmap.
