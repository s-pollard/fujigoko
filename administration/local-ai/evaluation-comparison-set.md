# compact model comparison set

Prepared after the [27B follow-up](results/2026-10-23-qwen-27b-follow-up.md), 2026-10-23. Runnable pack v1 and a separate evaluator key have been created and locally validated; no model comparison has been run on that pack. Host/runtime/memory controls still require capture before comparative scoring. No smaller model is selected here. Use the [protocol](evaluation-protocol.md) and [run template](evaluation-run-template.md).

The purpose is a manageable first comparison of practical reliability, evidence discipline and latency. Retain the full 24-task roadmap for broader coverage. Passing this screen does not establish production or unattended readiness.

## pack v1 coverage

Eight task IDs, nine cases because task 7 has a positive/negative pair:

| Task | Case | Reference to prepare before scoring |
| --- | --- | --- |
| 1 | Git status with unequal ahead/behind counts | Disposable repository with known graph, clean/dirty state and locally stored upstream; correct left/right labels and remote-staleness caveat |
| 5 | Database engine from bounded evidence | Synthetic service/config snippets containing supported engines, a non-database dependency and a genuinely unknown engine; no credentials |
| 7 | Real contradiction | Two explicit same-scope, same-time incompatible claims with exact source text |
| 7 | Apparent contradiction | Dates/target qualifiers or ambiguous wording that do not establish a contradiction; correct abstention |
| 8 | Actual unavailable executable | Real failed invocation through the terminal; no installation/substitution or fabricated probe result. This narrower variant does not test a disabled Hermes tool/connector |
| 14 | Exporter endpoint mismatch | Isolated exporter and supplied intended/scrape configuration, prechecked success/failure; label this synthetic and do not claim a real Prometheus scrape |
| 15 | Real Loki label discovery and retrieval | Isolated pinned Loki, exact seeded records and distractors, bounded requests and a prevalidated fixed window |
| 22 | One exact authorized edit | New disposable checkout/worktree, predetermined original/expected bytes, source-state protections and uncommitted result |
| 24 | Conflicting evidence | Fictional memory/repository/dated observations with known scope limits; this case tests interpretation, not actual memory management |

Task 23 host preflight is a prerequisite for execution cases, not an extra scored case in this nine-case screen. Pack v1 uses a verified absent executable for case 8; missing Hermes-tool routing remains an uncovered roadmap variant. Task 22 uses an evaluator-prepared worktree and does not score worktree creation.

## frozen pack and validation

The separately supplied files are `homelab-comparison-v1.zip` and `homelab-comparison-v1-evaluator-key.md`. The evaluator key and setup source must stay out of the tested agent's authorized inputs and context. No private artifact links, generated service endpoints, run paths or raw transcripts are published here.

Archive SHA-256: `af1774774078a73d9880030ccb65aba492d8f775673cd403bc04868fa68af9cf`.

The archive contains a Python setup runner, instructions, validation note, blank run record and file-hash manifest; no Loki binary or answer-key file. It requires Python/Git plus an existing pinned official Loki 3.7.9 Linux amd64 binary for all nine cases. Without that binary, case 15 is explicitly blocked rather than replaced by a mock. It installs/downloads nothing and changes no Hermes settings.

Local validation exercised the unequal Git graph, real missing executable, live success/refusal metrics endpoints, actual pinned Loki discovery and exact seeded retrieval, edit acceptance/rejection, and owned-process shutdown. Source parsing, archive contents and manifest hashes were checked. User-host prechecks remain mandatory.

Exact prompt templates and reference answers are frozen for v1. Only documented temporary paths, loopback ports and absolute Loki timestamps vary per generated fixture; relative data/window structure is fixed. Every final answer has a 200-word limit; evaluator cancels incomplete cases at 180 seconds wall time. Start fresh cases, retain all first attempts, and do not retrospectively relax limits. New templates require a new revision.

## remaining preparation gates

- Freeze exact prompts, fixture identifiers/hashes, expected results, accepted alternatives and explicit failure conditions privately before any scored attempt. Keep reference answers unavailable to the model.
- Reuse the pilot concepts rather than silently reuse its scores. Where prior feedback or memory could affect results, record exposure and establish equivalent starting states. Fresh chats alone do not solve this.
- Pin the repository/application versions and verify installed/running model, framework, inference build, context/output budgets and reasoning setting. Preserve unknowns rather than copying earlier defaults.
- Prepare a controlled memory/skills starting profile if supported. Keep the user's normal learning profile intact. If control is unavailable, label comparisons exploratory.
- Validate all fixture outcomes independently, including API timestamp parsing and actual tool failure. Give each model equivalent endpoint-discovery information; private ephemeral endpoints can vary only under a documented equivalent fixture.
- Retain expanded tool records privately and publish sanitized results. Distinguish agent actions from automatic skill/context injection when assessing scope.
- Use the same explicit output limit and predeclared time budget per case across models. Record cancellation or timeout as an outcome; do not choose the cutoff after seeing which model is slower.
- Define cleanup/ownership and record fixture shutdown separately from model performance. Setup, ingestion and cleanup are evaluator operations unless the task expressly includes them.

## execution order and decision

1. Run pack v1's prechecks on Aso and capture actual runtime/memory controls. Local fixture validation does not establish comparable model starting states; unresolved controls make the comparison exploratory.
2. Run 27B on the frozen cases in separate fresh chats. Preserve first attempts, interventions and tool evidence; do not substitute earlier exposed pilot outputs.
3. Select one smaller candidate, then repeat the same cases under equivalent permissions, tools, memory, exposure and generation settings. Record usable context and memory alongside outcomes; a 24 GB test does not prove 16 GB fit.
4. Compare the five dimensions, material errors, automatic failures, corrections and elapsed time on the same cases. Report unassessed dimensions and incomparable runs rather than forcing a leaderboard.
5. Use the result to choose which model deserves broader roadmap testing. Do not buy hardware or change the production role based only on fitting weights or faster text generation.

No benchmark run, model download, inference-setting change, system package installation or hardware purchase is authorized by this planning document.
