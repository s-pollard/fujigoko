# Odysseus on Aso

Initial experiment record: 2026-10-21, with a [2026-10-22 follow-up](#follow-up--2026-10-22) below. Tested upstream revision `934d23c` from the curated main branch. Two local routing patches were applied initially, followed by a third workspace-memory patch. Source changes were not reported committed or accepted upstream. Findings describe the tested setup, not every release.

## setup and verified capabilities

- Installed natively in a Python virtual environment and launched the web UI with Uvicorn. The UI was reachable and login worked.
- Connected the custom OpenAI-compatible provider to the existing Hermes-managed llama.cpp service and Qwen3.8-27B-UD-Q4_K_M. This reused the model and GPU backend; it did not connect Odysseus to Hermes's full agent or inherit Hermes's saved skills/memory.
- A model reply claimed to be Claude. This was incorrect self-identification, not evidence of an Anthropic backend. Use endpoint configuration and server evidence for identity.
- Agent mode produced actual approved Bash tool calls on Aso. The agent workspace and repo working directory differed between runs; working directory does not establish file-tool authorization.
- Inspected both homelab repos, summarized the production/lab boundary, and prepared an AdGuard placement correction on a dedicated branch. The user reviewed the four replacements across three files, committed, and pushed. Merge state is not asserted here.

Earlier replies in Chat mode described tool results. Later logs showed chat-to-agent auto-escalation for explicit paths, so the mode label alone neither proves nor disproves execution. Actual tool records are the evidence. A terminal-only chat interface was not established by this test; the verified interaction was the web UI.

## planning quality and performance observations

Repository orientation was useful but needed corrections: a mirror was initially described with doubled usable capacity; existing snapshot retention was reused as a proposed backup policy; live DB/file backup consistency was overstated; documented state was sometimes presented too confidently. Those proposals were not implemented.

An orientation run reported about 251,000 cumulative input tokens, 6,422 output tokens, and five minutes elapsed. Backend logs showed repeated calls with individual prompts around 28,000–33,000 tokens in the later rounds. The cumulative number was not one 251K prompt. Truncated combined file output caused rereads. Informal generation rates around 53–73 tokens/second do not measure end-to-end task efficiency or accuracy.

## disappearing Shell: evidence and root cause

Shell was enabled in the settings UI, but some turns omitted Bash/Python/read-write schemas. Logs showed tools selected as relevant yet absent from the sent list's usual positions, with total counts changing between successful and failed turns. ChromaDB ToolIndex initialization also failed, causing keyword fallback; that was a separate observed degradation.

Two overlapping classifiers were identified:

1. `routes/chat_routes.py` marked any standalone `current` token as explicit web intent. A hyphenated branch such as `docs/adguard-current-placement` matched because hyphens are word boundaries. The downstream web-intent filter removed Shell and file tools.
2. `src/action_intents.py` classified `current … status` as a web lookup before considering terminal/workspace intent. Removing the first trigger alone did not fix the full reproduction.

Read-only classifier checks reproduced the distinction:

| Prompt | Before the second patch |
| --- | --- |
| Use Shell to show the current Git branch and working-tree status | web: current/latest lookup request |
| Use Shell to show the Git branch and working-tree status | workspace: terminal workspace request |

A separate turn re-enabled Bash through `ui_control`; the following command worked, but the next `current … status` request failed again. That toggle was not sufficient to fix classification. The root cause was not the hyphen itself, GPU capability, or a need to keep prompting the model to try harder.

## local mitigations applied

### explicit agent input budget

Using `src.settings.load_settings` and `save_settings`, set:

```text
agent_input_token_budget = 45000
```

Read-back printed 45000. Source inspection showed a non-default positive value acts as an explicit soft input cap; the default 6000 acts as an auto-scaling sentinel. This is input budgeting, not a replacement for model context metadata or an unlimited output allowance. Enforcement under a long session has not yet been demonstrated.

Metadata discovery requests to the local server's slots and models endpoints returned 401 while completion calls succeeded. Odysseus fell back to a 131,072-token model-family window despite the worker's observed 65,536-token setting. The explicit cap mitigates agent input growth; authenticated discovery, accurate UI context percentages, and auxiliary-route budgets remain unresolved.

### routing patch 1

In `routes/chat_routes.py`, removed only `current` from the broad explicit-web-intent regex. Genuine explicit search/weather/news terms remained. Syntax parsing and `git diff --check` passed. This was insufficient on its own because the second classifier still matched `current … status`.

### routing patch 2

In `classify_tool_intent` in `src/action_intents.py`, inserted an early rule before the other routing patterns:

```python
if re.search(
    r"^\s*(?:please\s+)?use\s+(?:the\s+)?(?:shell|terminal|bash)\b",
    text, re.I,
):
    return ToolIntent(True, category="workspace",
                      reason="explicit terminal execution request")
```

Local checks passed for both Shell/Git prompts returning `workspace`, while explicit weather search and exchange-rate questions still returned `web`. Syntax validation and whitespace checks passed. After restarting Odysseus, the previously failing full request produced a real Bash call without a tool toggle and returned the repo's branch/status.

This validates one reproduction, not a comprehensive routing fix. Other broad words, alternative imperative phrasing, negation, multilingual requests, and mixed local/web tasks need regression coverage. Source backups were made in temporary storage; they are not durable recovery artifacts. The patches were not reported committed, pushed, or accepted upstream. Preserve/review the local diff before updating Odysseus.

## related upstream reports

These are related reports, not proof that a fix is present in the installed revision. Status was checked during this investigation and can change.

| Reference | Relevance |
| --- | --- |
| [Issue 6103](https://github.com/odysseus-dev/odysseus/issues/6103) | Explicit modes and additive tool selection |
| [Issue 4048](https://github.com/odysseus-dev/odysseus/issues/4048) | Missing file tools when ChromaDB is unavailable; keyword fallback weaknesses; open when checked |
| [PR 6275](https://github.com/odysseus-dev/odysseus/pull/6275) | Carry recently used tools across turns; draft when checked, with runtime validation explicitly outstanding |
| [Issue 5193](https://github.com/odysseus-dev/odysseus/issues/5193) | Static 131K context vs smaller serving window; reported with Ollama, not the identical llama.cpp discovery path; open when checked |
| [Discussion 3662](https://github.com/odysseus-dev/odysseus/discussions/3662) | Workspace/file tools rejecting project paths; historical discussion, not a verified fix for this install |
| [Discussion 2454](https://github.com/odysseus-dev/odysseus/discussions/2454) | Auto-memory extraction, Qwen reasoning/JSON limits, and clarification that vector failure should degrade retrieval rather than prevent memory creation |

No exact upstream report for the `current` false-positive reproduction was found in the searches performed. No new upstream issue was filed during this session.

## follow-up — 2026-10-22

Evidence below is user-supplied tool output, UI inspection, and terminal output from the continued Aso test session. No new live inspection was performed while writing this record.

### repository synchronization

Aso's Fujigoko checkout was switched to `main` and fast-forwarded to `4482cf9`, incorporating the reviewed SMART exporter, AdGuard placement, and local-AI records. Remote branch-label cleanup was deferred and was not subsequently reported completed. This is dated checkout evidence, not a requirement to remain at that commit.

### explicit workspace binding and file-tool verification

Inspection of the installed source established supported workspace selection via `/workspace set <absolute-repo-path>` or the workspace picker. Selection is per chat/request, not global. The user selected the Fujigoko checkout.

- `get_workspace` returned the selected repo, and `read_file` read its `SECURITY.md` directly without Shell.
- A missing disposable test file was created with `write_file`, read back, changed with `edit_file`, and read back again with the expected replacement.
- No existing repo documents were changed by that test, and nothing was staged or committed.
- Cleanup commands were supplied afterward, but removal and a clean status were not explicitly reported. Check for the disposable test file before committing unrelated work.
- An earlier out-of-workspace file access was refused. The successful read/create/edit test itself did not retest outside-root refusal.

This resolves the demonstrated repo file-tool access problem when the workspace is explicitly bound. Workspace persistence across fresh conversations remains separate. Shell starts in the workspace but is not confined to it.

### local patch 3: preserve memory in workspace tool selection

Memory requests repeatedly reported `manage_memory` unavailable even while other tools worked. Installed source showed:

```python
_relevant_tools = set(_WORKSPACE_TERMINUS_TOOLS)
```

That workspace selection replaced the normal tool set; `_WORKSPACE_TERMINUS_TOOLS` included skills but omitted memory, despite `manage_memory` normally being always available.

The local mitigation added `manage_memory` to the `_WORKSPACE_TERMINUS_TOOLS` set in `src/agent_loop.py`. Syntax and whitespace checks were included in the supplied patch procedure. After the restart procedure, an actual `manage_memory` add result was reported with the complete homelab boundary. Later retrieval from a fresh chat returned that stored text.

This changes selection, not authorization: existing disabled-tool and incognito checks still apply. It does not establish that every turn exposes memory. Older conversations continued to report it missing, and one fresh-chat path worked while another failed.

Broad web-intent classification remains another observed hazard. A memory prompt containing “search” can enter the web-only path, including when the word appears in a prohibition. Avoid treating every missing-tool response as a disabled UI toggle. Exact per-request selection and sent schemas are still needed to explain all failures.

### memory storage, retrieval, and pinned recall

The durable fact tested was: Fujigoko is production; Gusuku is disposable learning infrastructure; Fujigoko must never depend on Gusuku for required home services; useful experiments graduate by being rebuilt on Fujigoko.

| Test | Observed result |
| --- | --- |
| Explicit save | Actual `manage_memory` add returned the complete fact |
| Fresh-chat retrieval | Actual memory-tool results included the complete saved fact and entry identifiers |
| Automatic relevance selection | A response indicator showed four pinned identity entries and one recalled homelab-role entry; the full boundary was not among those automatically supplied |
| Agent recovery | The agent called memory, received the boundary, and answered the dependency direction correctly |
| Pinned boundary | After one complete boundary entry was pinned, a fresh-chat answer used it correctly without any tool lookup |

Storage and explicit cross-chat retrieval are verified; automatic relevance selection is not reliably supplying the important rule. Pinning worked for this specific durable boundary, not as a general guarantee for every instruction.

Brain UI inspection showed overlapping identity and homelab entries, including two copies of the complete boundary. Later tool output returned more entries than the earlier inspection, consistent with additional extraction. Duplicate cleanup was discussed but not performed or verified. The Brain management list shows stored memories, not necessarily the subset injected into a particular answer; use the answer's pinned/recalled details to inspect that subset.

One failed recall attempt used web results and reversed the dependency direction in its final answer, despite other parts stating it correctly. It was not a memory-only success. Later memory-based responses sometimes added an unsupported claim that Gusuku should build on production's stability. The accepted rule permits selected interactions but does not require or broadly recommend production dependencies for the lab.

### bounded maintenance task

Odysseus executed a read-only Python-via-Shell scan of local Markdown links in the Fujigoko checkout and reported no missing file targets. External URLs and same-page anchors were excluded. The displayed command was truncated, so full Markdown syntax coverage and fragment-anchor validation were not established. Treat this as a successful small tool-execution task, not a complete documentation validator.

### private remote-access setup

The user configured Tailscale Serve in background mode to proxy to the loopback-bound Odysseus web service. Terminal output confirmed a private tailnet HTTPS route and that Serve was running. Keep the actual hostname, tailnet identifiers, management URL, and addressing in private operational notes.

Aso must remain awake with Odysseus and the local inference backend running. Serve's background mode does not itself start or supervise those applications. Router port forwarding and public Funnel exposure were not used. Login remains required.

This verifies proxy configuration only: no successful off-LAN browser login or remote model response was reported. External access, application behavior behind the proxy, and reboot persistence of the complete stack remain to be tested.

### additional upstream reading

Read during the memory investigation; reports and proposals are context, not proof of installed fixes:

- [Discussion 2406](https://github.com/odysseus-dev/odysseus/discussions/2406): persistent memory versus relevance-selected recall; manual seeding and fresh-chat tests.
- [Issue 4948](https://github.com/odysseus-dev/odysseus/issues/4948): configurable recall count.
- [Issue 4949](https://github.com/odysseus-dev/odysseus/issues/4949): duplicate consolidation and proposed manual merging.
- [Issue 6194](https://github.com/odysseus-dev/odysseus/issues/6194): ordinary “from/on” phrases triggering local-machine routing and replacing personal-assistant tools.
- [Issue 6034](https://github.com/odysseus-dev/odysseus/issues/6034): proposed richer retrieval and memory revision; not adopted by this test.

## unresolved findings and next checks

- Harden tool selection, especially memory availability and web intent/negation across conversations. The three local patches cover observed paths, not the entire classifier.
- Verify the automatic memory relevance path and duplicate handling without adding repeated copies of the same rule. Back up the memory store before cleanup.
- Restore or deliberately configure ChromaDB/vector retrieval; the follow-up did not report that service repaired.
- Verify skill persistence in fresh conversations; memory success is not skill verification.
- Fix authenticated context discovery and verify the 45,000-token soft budget under a long session; do not trust the UI percentage without its denominator.
- Preserve and review all three local source patches before upstream updates; add broader regression tests before proposing them upstream.
- Verify unattended startup, background-job visibility, cancellation, and complete-stack behavior after reboot.
- Test the configured private HTTPS route from an actual off-LAN client.
- Check disposable test-file cleanup and deferred branch-label cleanup. No new production host configuration or Odysseus-to-Yamanaka execution was established by these follow-up tests.
