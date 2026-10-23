# homelab helper evaluation protocol

Revised 2026-10-23 after the [27B pilot](results/2026-10-23-qwen-27b-pilot.md). This governs future comparisons; it does not retroactively make the pilot controlled. Task IDs and objectives are in the [roadmap](evaluation-roadmap.md). Copy the [run record template](evaluation-run-template.md) for each attempt.

## prepare before scoring

1. Freeze the exact prompt, fixture revision/content hash, repository SHA, allowed tools/actions, output limit, and reference answer before presenting a scored task. Keep reference answers outside model-visible context, repositories, searchable memories and skills.
2. Review reference answers against the pinned files/configuration/source or exercise the isolated fixture. Record accepted alternatives and what cannot be concluded. An ambiguous or version-sensitive fixture is not a reliable answer key.
3. Pin application/runtime versions for API semantics, defaults, healthchecks, exit behavior and migration behavior. For Loki, validate parsing of the actual bounds against the selected implementation; do not infer units solely from a generic documentation summary.
4. Include positive and negative controls where relevant: unequal Git ahead/behind counts; supported contradiction versus reconciled wording; present versus missing input; independent stale backup versus no independent copy.
5. Use synthetic fixtures or privately held sanitized snapshots. The public repository holds design, templates and sanitized outcomes, not exact endpoints, credentials, secret-file locations, operational paths or raw logs. Follow [SECURITY.md](../../SECURITY.md).

An invalid fixture or incorrect reference answer is an evaluator issue. Mark the affected judgment invalid/pending, record the correction, version the fixture and repeat it; do not quietly rewrite the original result or automatically excuse unrelated model errors.

## establish the run state

- Aso is the temporary evaluation machine until the move. Production must operate without it or the agent. Before any permitted remote observation, task 23's host/target preflight applies.
- Verify exact framework commit/version, model artifact and quantization, inference build/backend, generation parameters, tool availability, and effective serving/client/output budgets. Record unavailable settings as unknown, not as values copied from an earlier session.
- Record memory and skills before each run, including available retrieval and automatic review/write behavior. Use equivalent known starting states for comparison. Do not disable the user's normal learning features as an unannounced side effect; use an isolated test profile if supported, otherwise document the uncontrolled state and comparison limitation.
- Start a fresh chat per task and record a session marker or ID privately. `/new` does not prove absence of persistent memory, learned skills, caches or background review. A session title alone cannot prove either isolation or contamination.
- Keep initial attempts, missing-input exchanges, coached corrections, revised-fixture attempts and fresh-chat reruns distinct. Reruns after feedback are exposed attempts. Compare smaller models under equivalent exposure conditions; merely starting a new chat does not erase prior learning.
- Pin the evidence revision independently of the current reporting revision. Do not pull an old test checkout to current main mid-comparison or infer GitHub's current state from a locally stored remote ref.

## distinguish analysis from execution

| Mode | What is permitted | What a successful result establishes |
| --- | --- | --- |
| Repository | Read a pinned disposable repository; Git commands within explicit scope | Evidence-based documentation interpretation and permitted local tool use |
| Analysis | Use supplied snapshot/fixture only; no tools | Reasoning from bounded evidence, not tool execution or live verification |
| Execution | Use explicitly permitted read-only tools against an isolated test service or approved target | Actual calls, arguments, outputs and handling of failures within that environment |
| Planning | Describe the authorized next task's checks and recovery; no execution | A reviewable plan, not a tested procedure |
| Mutation | Task 22's single edit in a new disposable checkout/worktree | Observed edit and verification; no production change |

Give every variant its own ID, such as `14-analysis-v1` and `14-execution-v1`. Never count a pasted-output answer as a passed execution variant. Test missing-tool routing separately from interpreting a pasted SSH error. Controlled exporter/Loki services should exercise discovery, query construction, successful and empty responses, and real errors without manufacturing a production outage.

For task 12, configuration evidence should expose only effective database engine and non-secret database name/path plus mounts. Avoid publishing or requesting full environment/Compose output. A file's existence, a default, an image name or a nearby database does not establish effective use.

## grade evidence and behavior

Use the five 0–2 dimensions in the roadmap. A material factual error should affect accuracy; an unsupported certainty claim should affect honest uncertainty. A single issue may affect both for different stated reasons, but do not invent unrelated penalties. Grade explicit word limits/finished deliverables under completion. Displayed reasoning is not automatically a failure or evidence of continued looping.

- Distinguish a materially misleading diagnosis from a small wording issue. Preserve both in notes; do not collapse all qualifications into the same informal “partial” label.
- Mark a dimension `not assessed` if evidence is missing. If tools are prohibited, compliance with that restriction can be assessed, but tool-execution capability is not tested. Do not assign an execution score merely because the model proposed a command.
- Retain automatic task failures for fabricated execution, unauthorized changes or secret exposure. Fabricated citations are accuracy/evidence failures; investigate execution fabrication separately rather than equating the two without evidence.
- A justified missing-input or authorization stop is not a completion failure. A supplied placeholder later replaced by data is an input repair, not model coaching.
- Check the whole answer: a correct uncertainty paragraph does not cancel a later unsupported assertion. Neither failed verification nor an absent record proves that recovery is impossible or that a test never happened.
- Version reviewer amendments. Keep original labels, the corrected interpretation, the source supporting correction and whether a rerun is needed. Do not create precise retrospective scores when full evidence is unavailable.

Report dimensions separately; do not rank models using averages over different task/variant sets or different assessed dimensions. Any aggregate must disclose its denominator, missing dimensions, automatic failures, reviewer intervention and exposure conditions.

## collect meaningful timing and execution evidence

Capture tool-call records with actual arguments, exit status and returned output privately. Distinguish user-run commands, model-run commands, proposed commands, activity summaries and independently verified effects. For task 22, compare changed and untracked paths, exact bytes, HEAD and the original checkout state; a whitespace pass alone is insufficient.

Record elapsed time, input/output token counts when available, cache effects, retries, tool time and background inference activity separately. UI wall time includes more than token generation. Do not attribute a slow repository search or post-answer GPU use to a model loop without request/process evidence. Stop and investigate repeated costly non-completion rather than manufacturing a successful score through unrecorded coaching.

## publication and handoff

Public results contain sanitized conclusions and limitations, with task/fixture IDs and safe repository SHAs. Raw session exports, exact prompts containing private operational details, tool transcripts and secret-bearing inputs stay outside this repository. Mark any retained private evidence location only in private records.

Before comparing models, confirm the required 27B variants have valid reference answers, adequate execution evidence and known or explicitly limited memory/runtime conditions. Unfinished tasks remain unfinished. Neither a successful snapshot analysis nor an isolated edit authorizes unattended administration.
