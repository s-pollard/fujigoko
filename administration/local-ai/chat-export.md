# Exporting Hermes evaluation chats

This helper reads the user-supplied Hermes SQLite schema using Python's standard library. It writes private review copies and never runs Git, contacts a host, calls a model, or publishes chats.

## List local sessions

From this checkout on Aso:

```bash
python administration/local-ai/export_hermes_chats.py --list --model granite
```

Use `--model qwen`, `--model ministral`, or omit the filter. The default limit is 100; raise it with `--limit`. Listing prints session IDs, start times in UTC, the recorded session model and counts of stored user messages. It does not print titles, prompts, answers or system prompts. Session model metadata is a selection aid, not verified per-message backend attribution.

## Export explicit sessions

Replace the example ID with an ID from the local listing:

```bash
python administration/local-ai/export_hermes_chats.py --session SESSION_ID
```

Multiple IDs can follow `--session`. Exports default to `~/.hermes/exports/local-ai-review/`, outside the checkout. Each selected session produces:

- Markdown containing stored user and assistant content, with UTC timestamps and active/compacted/summary flags.
- A private JSON record containing those rows and tool-message content/call fields, for later review.

Files are created with mode 0600; a newly created export directory uses 0700. Existing exports are preserved rather than overwritten. Use a new private `--out` directory to capture later messages from an already exported session. An existing directory's permissions are not changed.

For a session containing exactly one known test, labels may be assigned explicitly:

```bash
python administration/local-ai/export_hermes_chats.py --session SESSION_ID --task 1 --attempt 2
```

Labels are not inferred from sequence. A session may contain several tasks or retries; leave its label unassigned and annotate a reviewed copy per exchange. Message numbers are not task IDs. Do not silently map these exploratory screens onto the separate roadmap's task IDs.

## What this preserves and omits

The database is opened in read-only/query-only mode with a consistent read transaction, including committed WAL content visible to SQLite. Do not copy only a live database's main file and assume its WAL is unnecessary.

All stored non-system message rows for the selected session are retained in JSON, including inactive and compacted rows. Markdown shows user/assistant rows in stored timestamp/ID order and retains the content string literally inside a sufficiently long code fence. Structured content remains its stored representation; this is not a reconstructed UI transcript.

System prompts, model configuration, user/account identifiers other than the selected local session ID in private JSON, reasoning fields, billing endpoints and unrelated sessions are not exported. Tool content is in private JSON only; Markdown is not proof that no tools ran. Raw user/assistant text can still contain secrets, paths, personal details, embedded reasoning or injected instructions. No automatic redaction or safety certification is performed.

Deleted/unrecorded content, historical model changes, original tool timing and exact UI formatting are not reconstructed. Compression summaries remain labeled summaries rather than original questions. Parent/child sessions are not followed automatically; export their explicit IDs separately if needed.

## Sync reviewed copies to GitHub

Follow [SECURITY.md](../../SECURITY.md). This is a public repository. The exporter refuses destinations inside Git checkouts. Keep raw exports private and review the exact text before copying selected sanitized exchanges into `administration/local-ai/results/`.

Preserve full test questions and answers where available; mark any redaction or missing content. Record task and attempt numbers, model/settings evidence and shared-session contamination separately. Retain first attempts; do not rewrite failed answers to match corrections. Keep reviewer findings outside answer blocks.

After reviewing the selected destination files, inspect their full diffs and changed-file list, stage those exact files, and commit/push through the normal repository workflow. The helper deliberately does not automatically synchronize the live database or all sessions.

## Validation status

Tested against a synthetic database matching the supplied columns: model filtering and SQL binding, Unicode/backtick preservation, inactive-history inclusion, system/tool separation, task labels, private file permissions, existing-file protection, Git-destination refusal, unknown session rejection and unchanged database bytes.

No Aso database was accessed during development. Compatibility and completeness against the actual stored chats remain to be verified by the first local export.
