# Agent hook starter kit

Wiring for a coding-agent hook. Claude Code, Codex, and Cursor each send a JSON
event to `hook/hook.py`. Your logic goes in `decide()`.

## Run it

```sh
cd agent-hook-starter-kit
claude          # or codex, or open the folder in Cursor
```

Approve the hook when asked. Every event and decision is then appended to
`logs/events.jsonl`. To check the wiring, ask the agent to run
`npm install ./samples/canary-package`. It is blocked.

## decide(event, folders)

Return a reason to block, or `None` to allow. An allowed command runs for real.
You get two inputs and can work from either.

1. **The event.** The agent's tool call, as sent. Fields are documented in
   each agent's hooks reference, linked below.
2. **A local folder.** Put your sample under `samples/` and ask the agent to install it. The folder arrives in `folders`, which is empty for any other command.

Simulate the hook without an agent:

```sh
echo '{"tool_name":"Bash","cwd":".","tool_input":{"command":"npm install ./samples/canary-package"}}' | python3 hook/hook.py
```

The canary check in `decide()` and the folder spotting are placeholders.
Replace or extend anything.

## Files

| Path | Purpose |
|---|---|
| `hook/hook.py` | The hook |
| `samples/` | Put your samples here. Holds the canary sample |
| `.claude/settings.json` | Claude Code registration |
| `.codex/hooks.json` | Codex registration, needs a git checkout |
| `.cursor/hooks.json` | Cursor registration. Cursor also reads the Claude Code file, so delete one if events log twice |

The registration files hook one event, the one before every tool call. Which
hooks to use is your call. Each agent's reference lists them:
[Claude Code](https://code.claude.com/docs/en/hooks),
[Codex](https://developers.openai.com/codex/hooks),
[Cursor](https://cursor.com/docs/hooks).

Requires Python 3.
