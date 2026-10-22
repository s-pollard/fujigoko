# Odysseus on Aso

Dated experiment record: 2026-10-21. Tested upstream revision `934d23c` from the curated main branch, with two subsequent uncommitted local routing patches. Findings describe this revision and this session, not every release.

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

## unresolved findings and next checks

- Configure deliberate repo workspace access. File tools returned `outside the allowed roots` or no workspace even when Shell could read the repo. Successful shell editing did not resolve that boundary mismatch.
- Restore or deliberately configure ChromaDB/vector retrieval; avoid assuming all memory and skills fail merely because ToolIndex is degraded.
- Test saved memory and skill retrieval across sessions; these were not demonstrated to the same extent as Hermes's reported persistence.
- Fix authenticated context discovery and verify the soft budget under a long agent session; do not trust the UI percentage without its denominator.
- Package the two routing changes with broader regression tests and a public-safe reproduction before proposing an upstream fix. Do not install unrelated draft PRs blindly.
- Retest background activity visibility and cancellation, model-server ownership, and remote access independently. Yamanaka inspection was proposed in Odysseus but not established as completed by these tests.
