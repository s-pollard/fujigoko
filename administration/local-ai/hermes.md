# Hermes Agent on Aso

Dated experiment record: 2026-10-21. Evidence is the interactive session's commands, user-pasted results, and reviewed diffs. This page is not a fresh inspection of any host.

## setup and demonstrated use

- Installed Hermes Agent v0.22.3 and selected local Qwen3.8-27B-UD-Q4_K_M through Hermes-managed llama.cpp Vulkan b11671; see the [shared setup](README.md).
- Selected the local terminal backend. Messaging platforms were not configured during the initial wizard. Later housekeeping logs mentioned gateway activity; the final service installation state was not independently reconciled.
- Reduced reasoning effort from medium to low after output exhaustion. Cloud-dependent tools and provider configuration were not comprehensively validated; local model hosting does not make every enabled tool offline or keyless.
- Used GitHub-authenticated local clones of Fujigoko and Gusuku for documentation orientation and audits. No repository-level AGENTS.md was reported during the inspection.
- Demonstrated read-only remote diagnostics on Yamanaka after dedicated SSH access was established. Credentials and connection details are intentionally excluded here.

## work completed with assistance

| Work | Outcome and limits |
| --- | --- |
| Documentation audit | Identified completed Immich restoration and Kawaguchi container/appdata cleanup still listed as pending; kept legacy-share cleanup separate |
| Recovery runbook | Aligned Yamanaka storage and Uptime Kuma placement with live evidence; retained the limitation that host failure also removes its local monitoring |
| Git workflow | Reviewed changes, committed and pushed branches, and merged the first documentation PR; later exporter documentation was separately prepared and pushed during the session |
| Yamanaka baseline | Inspected hardware, container state, failed units, and monitoring endpoints without changing host configuration |
| Monitoring | Established Prometheus scrape state and investigated the Alloy-to-Loki path; corrected malformed probes before drawing a final conclusion |
| Kawaguchi SMART exporter | Helped diagnose restoration and runtime-user permissions; the user performed the Unraid changes, and Hermes later verified target health and device metrics from Prometheus |

The exporter had a saved Unraid template but no running container. Recreated privileged, it initially ran as `nobody`; setting a `USER=root` environment variable did not change runtime UID. An explicit runtime user override to root resolved device permission errors. Metrics then covered nine devices. This did not establish that every disk was problem-free. A short test of the flagged HDD completed without error; a historical attribute warning remained distinct from an active failure.

An additional exported NVMe device did not establish its role or contradict the documented two-device cache pool. Do not infer an OS role from capacity alone.

## persistence and learned procedures

Hermes reported saving durable environment boundaries and repo navigation to memory and creating a `homelab-repos` skill. A later review removed volatile contradiction lists, branch names, and other state from the reusable skill. Host placement, purchase state, and outstanding work should be re-derived from current repositories and live evidence.

A `monitoring-check` skill was created after the Loki investigation. Its corrected rules include:

- construct explicit UTC query windows and print the interpreted time range;
- validate selector syntax and timestamp units before interpreting empty results;
- use build/process metadata plus container/port mapping for endpoint identity;
- treat `/ready` as readiness only, not identity;
- do not recommend infrastructure changes based on malformed probes.

The reported writes were checked during the session. A controlled new-session test of all learned behavior remains useful; saving a skill does not prove reliable future application.

## failures, corrections, and mitigations

### media-tokenization failure

A request failed with HTTP 400, `Failed to tokenize prompt`. The relevant backend evidence reported one media marker and zero bitmaps. That finding superseded the early guesses about context exhaustion or tokenizer mismatch for this incident. A new conversation answered successfully, while resuming the affected history reproduced the failure. The exact source of the unmatched marker was not established.

### independent context overflow

A separate request explicitly contained 65,715 tokens against a 65,536-token server window. Hermes telemetry treated the model as having a 262,144-token context and compressed only after overflow. This was a client/server budget mismatch, not the media-marker failure.

The following settings were accepted:

```text
model.context_length = 65536
compression.threshold_tokens = 45000
```

Later resumed-session errors still reported a 262,144-token client window, so the context-length setting was not proven effective on every route/session. The absolute compression cap was configured, but this is not a claim that all overflow paths were fixed. Do not increase the worker context blindly: cache memory and available VRAM constrain it.

### reasoning and background activity

Reasoning exhausted the output budget on repeated continuation attempts. Lowering reasoning to low allowed further work. Background-review and compression calls also used the main local model. Inference logs showed continued token generation, cancellation, and replacement tasks while the visible CLI appeared idle. High utilization alone did not establish a stuck process.

The user wanted automatic review/learning retained. No blanket recommendation to disable those features follows from the observed activity. Review scheduling, concurrency, cancellation, and output limits remain areas to validate.

### incorrect operational conclusions withdrawn

- Tailscale's resolver appearing in Aso's resolver configuration did not prove Aso bypassed AdGuard; forwarding remained possible.
- Cloudflare DoH connection-reset messages established upstream errors, not necessarily failed client queries after retries/fallbacks.
- A bare `{container}` selector was invalid LogQL. Later empty queries used incorrect timestamp magnitudes. Valid queries returned data from the same Loki instance; the conclusion that ingestion was broken was withdrawn.
- Sparse historical scrape sampling did not prove an exporter succeeded exactly once. Sample-count metric names and resolution need checking before historical claims.
- Consistent database dumps plus separate live file copies do not automatically form an app-consistent recovery set. Proposed retention and transfer methods were not implemented requirements.

### Git and session handling

A fresh clone lacked Git identity. An attempted correction accidentally wrote command text into identity settings; it was corrected repo-locally and the author verified before the resulting commit was accepted. Use single-purpose config commands and `git config --get` for reads. Amending a commit changes its hash.

Ctrl+C after completed edits did not remove on-disk changes. Git status/diff were used to recover the exact state. `hermes -c` resumed saved history, including problematic history; resumption is not a clean context reset. A tmux session was suggested for SSH continuity, but installation/use should be verified rather than assumed.

## inference follow-up — 2026-10-23

Paid model API inference was used during later testing, with reported spend of at least $4.71. The exact provider/model and final total are not established by this record. These later results must not be presented as proof that the initial local model completed the same tasks.

The intended ongoing homelab helper must use local inference; paid API inference is not the deployment option or a required fallback. Evaluation will use the available RX 7900 XTX now, targeting configurations that could later fit an RX 9060 XT 16 GB. The RTX 3060 Ti is currently inaccessible. No new model or GPU purchase is confirmed. See the [shared inference direction](README.md#inference-direction--2026-10-23).

The Paperless restore test provides a useful task benchmark: verified recovery, content search, original checksums, isolation, normal startup, restart persistence, and browser rendering. Its backup coverage remains incomplete because Yamanaka-to-Motosu backup setup has not been implemented; see [backup status](../../backups/README.md).

## remaining work

- Resolve effective context metadata on resumed sessions and auxiliary routes.
- Reproduce/fix unmatched media-marker history handling.
- Verify cancellation and background-job visibility without disabling desired learning.
- Test persistent memory/skill use in a new session and scope remote access deliberately.
- Keep backend logs private; command lines and logs can contain authentication material.
