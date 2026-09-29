# Agent hook starter kit

Optional starting point for the take-home challenge. It saves you the wiring
and nothing else. There is no detection logic here.

Change anything, use another language, or ignore the kit entirely.

Please clone this repository rather than forking it, and keep your solution private.

## Files

| Path | Purpose |
|---|---|
| `.claude/settings.json` | Registers the hook with Claude Code |
| `.codex/hooks.json` | Registers the hook with Codex |
| `.cursor/hooks.json` | Registers the hook with Cursor |
| `hook/hook.py` | Reads the event, logs it, and calls `decide()` |

Requires Python 3 and one of the agents above. No other dependencies.

The same hook script serves all three agents. Use whichever you prefer.

## Try it

```sh
cd agent-hook-starter-kit
claude        # or: codex, or open the folder in Cursor
```

1. Approve the hook when asked. Claude Code and Cursor ask you to trust the
   workspace. Codex asks you to review the hook under `/hooks`.
2. Ask the agent to run `echo hello`. It runs, and the event is appended to
   `logs/events.jsonl`.
3. Ask the agent to run `echo STARTER-KIT-CANARY-DENY`. It is blocked.

The canary only proves the wiring. Remove it once your own logic is in place.

Two notes:

- **Codex** finds the script through the git root, so work from a clone.
- **Cursor** also loads Claude Code hook settings by default, so events may be
  logged twice. Delete the config you do not need.

## Yours to decide

The kit registers one event for all tools, and an unhandled error in the hook
lets the action proceed. Both are placeholders, not recommendations.

## Official docs

Each agent documents its events, output formats, and debugging.

- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
- [Codex hooks](https://developers.openai.com/codex/hooks)
- [Cursor hooks](https://cursor.com/docs/hooks)
