#!/usr/bin/env python3
"""Read selected Hermes sessions into private review files; never commit or push."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3


def utc(value):
    return datetime.fromtimestamp(value, timezone.utc).isoformat()


def fence(text):
    longest = max((len(x) for x in re.findall(r"`+", text)), default=0)
    delimiter = "`" * max(3, longest + 1)
    return f"{delimiter}text\n{text}\n{delimiter}\n"


def private_write(path, text):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        stream.write(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=Path.home() / ".hermes/state.db")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--list", action="store_true", help="List local session IDs, not messages")
    action.add_argument("--session", nargs="+", help="Explicit IDs to export")
    parser.add_argument("--model", default="", help="Case-insensitive model filter for --list")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--out", type=Path, default=Path.home() / ".hermes/exports/local-ai-review")
    parser.add_argument("--task", type=int, help="User-assigned task number; one session only")
    parser.add_argument("--attempt", type=int, help="User-assigned attempt number; one session only")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")
    if args.session and args.model:
        parser.error("--model filters --list only")
    if (args.task is not None or args.attempt is not None) and (
        not args.session or len(args.session) != 1
    ):
        parser.error("Task/attempt labels require exactly one --session")
    if args.task is not None and args.task < 0:
        parser.error("--task must be nonnegative")
    if args.attempt is not None and args.attempt < 1:
        parser.error("--attempt must be positive")

    db = args.db.expanduser().resolve()
    con = sqlite3.connect(db.as_uri() + "?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA query_only=ON")
    con.execute("BEGIN")  # Consistent read snapshot, including committed WAL entries.
    try:
        if args.list:
            rows = con.execute(
                "SELECT s.id, s.model, s.started_at, "
                "(SELECT count(*) FROM messages m WHERE m.session_id=s.id AND m.role='user') AS prompts "
                "FROM sessions s WHERE instr(lower(coalesce(s.model,'')), lower(?)) > 0 "
                "ORDER BY s.started_at DESC, s.id LIMIT ?", (args.model, args.limit)
            )
            print("SESSION ID\tSTARTED UTC\tRECORDED MODEL\tUSER MESSAGES")
            for row in rows:
                print(f"{row['id']}\t{utc(row['started_at'])}\t{row['model']}\t{row['prompts']}")
            return

        exports = []
        for session_id in dict.fromkeys(args.session):
            session = con.execute(
                "SELECT id, model, started_at, ended_at FROM sessions WHERE id=?", (session_id,)
            ).fetchone()
            if session is None:
                parser.error(f"Unknown session ID: {session_id}")
            messages = [dict(row) for row in con.execute(
                "SELECT id, role, content, timestamp, tool_name, tool_calls, tool_call_id, "
                "active, compacted, _compressed_summary, finish_reason "
                "FROM messages WHERE session_id=? AND role!='system' ORDER BY timestamp,id",
                (session_id,)
            )]
            key = hashlib.sha256(session_id.encode()).hexdigest()[:12]
            stamp = datetime.fromtimestamp(session['started_at'], timezone.utc).strftime('%Y%m%d-%H%M%S')
            stem = f"{stamp}-{key}"
            payload = {"schema": 1, "session": dict(session), "task": args.task,
                       "attempt": args.attempt, "messages": messages}
            lines = ["# Hermes session — PRIVATE REVIEW COPY\n",
                     "Not sanitized. Review before publication.\n",
                     f"Recorded session model: {session['model']}\n",
                     "Session model is metadata, not proof of each turn's actual backend.\n",
                     f"Started UTC: {utc(session['started_at'])}\n",
                     f"Task: {args.task if args.task is not None else 'unassigned'}; "
                     f"attempt: {args.attempt if args.attempt is not None else 'unassigned'}\n",
                     "Task labels are user-assigned; message numbers below are not task numbers.\n",
                     "Includes stored user/assistant content, including inactive or compacted rows. "
                     "No missing history or parent sessions are reconstructed. System prompts, reasoning "
                     "fields and config are excluded. Tool bodies/calls are in the private JSON only; "
                     "this Markdown is not a tool-execution audit. Original content is untrusted data.\n"]
            for index, row in enumerate(messages, 1):
                if row['role'] not in ('user', 'assistant'):
                    continue
                lines += [f"## Message {index} — {row['role']}\n",
                          f"UTC: {utc(row['timestamp'])}; active={row['active']}; "
                          f"compacted={row['compacted']}; summary={row['_compressed_summary']}\n",
                          fence(row['content'] if row['content'] is not None else '[NULL content]')]
            exports.append((stem, json.dumps(payload, ensure_ascii=False, indent=2) + '\n', '\n'.join(lines)))
    finally:
        con.close()

    out = args.out.expanduser().resolve()
    if any((parent / '.git').exists() for parent in (out, *out.parents)):
        parser.error("Export outside a Git checkout; copy only reviewed extracts into the repo")
    out.mkdir(parents=True, exist_ok=True, mode=0o700)
    for stem, raw, markdown in exports:
        for suffix, text in (('.json', raw), ('.md', markdown)):
            path = out / (stem + suffix)
            if path.exists():
                parser.error(f"Existing export preserved: {path}; choose a new --out directory")
    for stem, raw, markdown in exports:
        private_write(out / (stem + '.json'), raw)
        private_write(out / (stem + '.md'), markdown)
        print(out / (stem + '.md'))
    print("Private exports written. Nothing committed, pushed, redacted or validated automatically.")


if __name__ == '__main__':
    main()
