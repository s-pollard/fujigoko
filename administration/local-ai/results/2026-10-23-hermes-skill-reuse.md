# Hermes skill correction and reuse review — 2026-10-23

Follow-up to the [27B execution record](2026-10-23-qwen-27b-follow-up.md). Evidence is user-pasted Hermes responses, displayed diffs/readbacks and activity summaries. The reviewer did not inspect the installed skill files, capture complete tool transcripts or independently replay these operations. This is a coached maintenance session, not a scored model comparison. The exact running model/settings were not recaptured; retain the prior reported 27B context without treating it as a new runtime verification.

## reported saved corrections

Two local Hermes skill files were corrected over several review rounds. These are reports of installed-skill changes, not claims that this public repository contains or deploys those skills.

| Skill location | Reported final correction |
| --- | --- |
| `homelab-repos/references/live-inspection.md` | Label-name discovery uses `/loki/api/v1/labels`, followed by a chosen label's values endpoint. Start with an explicit bounded window; justify expansion. Empty results remain inconclusive pending instance, tenant, selector, time units/window, retention and log-emission checks. |
| Same reference | Build/version metadata describes software; it establishes neither readiness, unique identity nor ingestion history. Returned log entries establish historical presence; labels/series metadata alone does not prove matching lines or current delivery. |
| Same reference | Current Paperless delivery is checked by correlating a known recent Paperless event with its matching ingested entry. General write metrics and label presence alone are insufficient. This establishes delivery of the matched event, not perpetual pipeline health. |
| `monitoring-check/SKILL.md` | Removed remaining “reachability only” wording for `/ready`: it checks readiness and does not establish unique identity. Replaced an unconditional wide discovery window with the bounded-window rule. |
| Same skill | Replaced unsupported timestamp consequences and frequency claims with a version-linked parser description and RFC3339 UTC recommendation. Preserved printing/validating interpreted bounds, including start < end. |

Hermes supplied an actual-looking diff/readback for the reference correction and targeted before/after passages for later changes. The final timestamp diff was manually presented; a complete independently generated before/after comparison was not supplied. No production changes or probes were reported during the correction steps; unseen activity is not certified by that statement.

## fresh-chat reuse findings

The first planning-only reuse response repeated old guidance: readiness reduced to reachability, assumed label names, a wide initial window, a ten-digit-only timestamp mandate and general ingestion indicators in place of application-specific event correlation.

After the second skill was edited, another fresh-chat response correctly used label-name discovery and event correlation but still repeated reachability-only and wide-window instructions. A subsequent report quoted the loaded skill: it contained both the new readiness sentence and an old “Use /ready only as a reachability check,” plus the remaining wide-window instruction.

This supports **conflicting saved instructions** as an explanation for those residual errors. It does not establish a failed save, a model inability to retain all corrections, or a completed test of reference-file retrieval. The planning replies identified the parent homelab skill but did not demonstrate reading the corrected reference. Hermes initially defended readiness and reachability as equivalent instead of recognizing the contradiction.

Both leftover passages were then reportedly corrected. No final fresh-chat reuse test after all corrections was supplied. Record the outcome as partial reuse followed by coached repair, with final reuse validation pending.

## timestamp source check and limits

No recorded source supported the old skill claims about far-future dates, guaranteed HTTP 200 empty responses, mixed-unit 90-day windows or “single most common” failure frequency. Lack of a citation made them unverified; it did not itself prove them false.

In a fresh, narrowly scoped check, Hermes reported retrieving [Loki v3.7.9 params.go](https://github.com/grafana/loki/blob/v3.7.9/pkg/loghttp/params.go) and quoted `parseTimestamp`: after integer parsing succeeds, input string length <= 10 selects seconds; longer strings select nanoseconds. Its subsequent draft also described decimal-second and RFC3339Nano handling and applicability to start/end/time. These are Hermes's source-check findings, not an independent source audit in this repository update.

The saved replacement retains the versioned source link and recommends RFC3339 UTC. It removes the unsupported consequences rather than treating the parser branch as proof of a particular API response or root cause. Parser behavior must remain scoped to parameters/code paths using that function; it is not a universal rule for every timestamp field or endpoint.

## efficiency and framework observations

- The user reported an investigation lasting over an hour with repeated compaction. No compression/request traces or exact total were captured. Context accumulation is a plausible contributor, not a proven sole cause or evidence of a generation loop.
- After interruption and a fresh chat, the one-claim source check visibly took 1m45s; its bounded replacement draft took 1m14s. These UI wall times include tool/framework work and are not inference benchmarks.
- A planning response footer said “ran 2 scripts.” Hermes later attributed its execution tool use to in-memory word counting and identified a DNS script as linked skill metadata, not an executed diagnostic. That self-report is not a complete tool audit. Neither linked filenames nor footer counts alone establish host access.
- A skill-view response reportedly returned “unchanged” after earlier content had been pruned. A later direct read supplied the current passage. Distinguish an available file from content actually delivered into the current context; never reconstruct exact edits from a prior answer when current bytes are unavailable.
- The reviewer also prolonged the session through repeated drafting, incomplete initial fixes and an optimistic duration estimate. This is not clean evidence of model-size limitations.

## working practices learned

1. Read the current affected passages and search for competing instructions across the relevant skills before editing. Fix the authoritative rule and its duplicates together.
2. Separate source verification from mutation. Keep each question bounded, cite the relevant version and avoid expanding into an improvised audit.
3. Verify saved bytes and changed scope. Git is not required for a real diff: compare preserved before/after files. A narrated diff is weaker evidence.
4. Test reuse in a fresh chat without repeating the expected answer in the prompt. Track which parent skill and references were actually loaded.
5. Stop repeated compaction/non-completion, preserve completed on-disk work and continue with one self-contained task. A fresh chat resets conversation history, not persistent skills or memory.
6. Treat activity summaries as leads for inspection, not proof of particular commands, remote access or scope violations.

## smaller-model handoff

Smaller-model exploratory testing can begin in the next session; no smaller model is selected or proven adequate. Keep 27B available as a reference. The 9B/14B sizes remain candidate ranges, not verified fit, speed or reliability claims.

Use the existing [comparison pack and protocol](../evaluation-comparison-set.md): capture actual model/runtime/context settings, freeze an equivalent corrected skill/memory profile, run fresh 27B reference attempts and then one smaller candidate on the same cases. The old pilot and today's coached repairs are not substitutes for those reference runs. Record accuracy, tool use, scope, uncertainty, completion, latency, usable context and VRAM.

Final skill reuse remains pending and long-session compaction remains unresolved. Neither blocks a clearly labeled exploratory screen; neither should be silently treated as fixed in comparative scoring. No model switch, download, inference configuration change or hardware purchase was performed by this documentation update.
