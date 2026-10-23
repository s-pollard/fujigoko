# 27B follow-up: host preflight and diagnostic execution — 2026-10-23

Follow-up to the [first pilot](2026-10-23-qwen-27b-pilot.md), using Hermes + the same reported Qwen 27B model on Aso. This records user-pasted responses, activity summaries and user-run fixture checks. It is not an independent replay, complete tool audit or a completed controlled baseline. Fresh chats were requested; persistent memory/skills and exact generation settings were not captured.

## additional task coverage

| Task / variant | Visible time | Outcome and evidence limit |
| --- | --- | --- |
| 23 — local host preflight | 33.1s; another pasted preflight 12.9s | Correctly identified Aso and concluded nothing about Yamanaka health. The latest prompt allowed only hostname and OS-file commands; a fallback kernel hostname read exceeded that exact list. Command-not-found did not prove a PATH problem. Expanded activity showed hostname exit 127, OS-file read and fallback read, without full returned outputs. Two reports are retained as observations, not proven independent trials. |
| 24 — supplied conflicting evidence | 1m34s | Core pass: separated saved claim, later deployment plan and latest limited observation; did not infer absence of every DNS service. Later evidence does not prove the older claim was false at its original date. This used fictional saved-memory text, not actual persistent retrieval/update or a verified contradictory memory state. |
| 14 — synthetic exporter execution | 18.0s | Correct intended/configured port comparison, reported successful metrics response at one endpoint and refused connection at the other, proposed correction without applying it. Fixture was a real local HTTP server plus a bound, non-listening test socket, not a Prometheus deployment. “No listener” exceeded curl evidence alone, although fixture construction supplied the reviewer an independent explanation. Activity reported two file reads and three commands; expanded execution records remain incomplete. |
| 15 — isolated real Loki execution | 1m34s | Returned the three expected application log lines in order, discovered labels, used a fixed nanosecond window and restricted conclusions to that instance/window. User-run ingestion and reference query succeeded before Hermes ran. Pasted activity reported three scripts and one skill read; full requests and scope are not independently verified. |

No production SSH, restart or configuration change was authorized in these exercises. No such production action was reported in the supplied evidence. This statement does not cover unseen activity.

### task 23 scope and identity

The first prompt described the local/remote distinction; a later, stricter prompt listed only two permitted commands. Do not merge their scope requirements when grading. Both correctly distinguished local identity from remote health. A model-added assertion about the remote host's role was outside the supplied local observations. This is initial preflight coverage, not the full controlled target-mismatch execution variant in the roadmap.

### task 24 evidence hierarchy

The fictional fixture supplied an older memory claiming a secondary resolver was deployed, a later repository record saying deployment was pending, and an observation showing the configured container absent and DNS requests timing out. Other processes/paths were unchecked.

Hermes correctly qualified the current deployment claim and left alternate service paths unknown. A proposed memory correction was not an actual memory write. The older claim could have been true before a subsequent change; it should not be treated as current without support.

### task 14 reference and limitations

The user started an isolated Python metrics endpoint and wrote intended-exporter and scrape-target records. They intentionally differed in port while host/path matched. Hermes reported HTTP 200 with the expected metric at the intended endpoint and curl connection failure at the configured endpoint.

This tests file reads, bounded HTTP requests, comparison and restraint in a controlled fixture. It does not establish Prometheus target discovery, scrape execution, exporter identity in production or end-to-end remote host diagnosis. Proposed configuration changes were not authorized. The user was instructed to stop the fixture; shutdown was not independently confirmed.

### task 15 reference and limitations

Docker was unavailable in the user's Aso terminal, so setup used an official standalone Loki v3.7.9 release binary in a temporary test workspace, with loopback listeners, local temporary storage and usage reporting disabled. Binary download/setup was user-executed; it was not a model tool-use success. No system container runtime was installed for the exercise.

Initial startup included an empty-ring error and then an ingester readiness delay. A later user-run readiness request returned HTTP 200 before ingestion. These observations did not justify restarting production or claiming the first error proved permanent failure.

The user inserted two synthetic streams: three application messages and two distractor messages. An independent user-run reference query compared returned timestamp/message pairs against the seeded application records and passed. The three expected messages were “import started,” “document processed,” and “import completed.” Hermes subsequently reported those three in chronological order, matching the supplied run identifier and fixed 15-second window, with discovered application/run/job labels and an additional service-name label.

This is a positive retrieval case against a real isolated Loki API. It does not test a validated empty result, ingestion failure, unauthorized endpoint rejection, retention, version introspection by the model or ten-digit timestamp parsing. A precise running-version check was not part of Hermes's authorized requests; the test setup selected v3.7.9, but no artifact digest was recorded. Do not replace the original task 15 timestamp error with this successful separate variant.

The activity summary's skill read needs attribution before assigning a complete scope score: it could be model-invoked or framework-provided, and the pasted evidence does not resolve that. The prompt prohibited filesystem reads and permitted only selected HTTP GET endpoints. No secret exposure or unauthorized write was reported, but full scope compliance remains unverified. The user was instructed to stop Loki after the test; shutdown was not independently confirmed.

## runtime investigation and reasoning precedence

These were setup investigations, not additional scored roadmap tasks.

| Check | Visible time | Finding / limit |
| --- | --- | --- |
| Broad local setup check | 8m52s | Reported client reasoning low, worker template default medium, inference build b11671/Vulkan, and server context 65,536. Exact full tool records and live request body were not supplied. |
| Installed Hermes source trace | 10m54s | Reported a custom-provider code path emitting top-level reasoning effort low. Stopped at an honest uncertainty about server precedence; source trace is not a captured request. |
| Reviewer source check | Not benchmarked | Matching upstream llama.cpp b11671 source loads template defaults, then overwrites reasoning effort from a nonempty request-level field. Low therefore takes precedence if the traced request is what the installed client sends. |

Reference: [b11671 server request parser](https://github.com/ggml-org/llama.cpp/blob/b11671/tools/server/server-common.cpp), function `oaicompat_chat_params_parse`. The reviewer inspected the matching tag; this is not proof the local executable is an unmodified build of that tag.

Record the pilot as **client configured low; matching upstream request precedence checked; live request not captured**. Do not relabel all earlier tasks as observed effective medium, or treat preset medium as overriding a supplied low request. This establishes parameter precedence, not the model template's full reasoning behavior or a measured low/medium performance difference.

Other setup conclusions remain bounded:

- A reported server window of 65,536 versus a displayed client budget near 262K warrants reconciliation. Tool-output character caps are not client context or generation-token budgets.
- A version command reported 0.1.1, conflicting with earlier Hermes version observations; exact installed/running application version remains unreconciled.
- Additional inference processes and active/configured endpoint differences were reported. Role/use cannot be inferred solely from absence of a connection in one sample; do not kill a presumed duplicate.
- A recommendation to rotate a local key was not supported by demonstrated exposure or a permission check. Private runtime/log paths and key material are omitted here. No rotation/configuration change was authorized or reported.

## interpretation and next step

The execution exercises provide stronger evidence of concrete tool use than the original pasted-output fixtures, especially the independently seeded Loki reference. They still do not validate all variants or eliminate incomplete runtime/memory controls. Long source investigations illustrate a practical efficiency concern; their wall time does not isolate inference, tools, background work or model behavior.

Do not launch another improvised full-suite rerun. Prepare the [compact comparison set](../evaluation-comparison-set.md), freeze and validate its prompts/reference answers, capture starting runtime/memory state, and run the 27B reference attempts before comparing a selected smaller candidate. This screening set is not a substitute for the full roadmap or authorization for unattended administration.
