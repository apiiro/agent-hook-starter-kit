#!/usr/bin/env python3
"""Starter hook for coding agents. Wiring only, no detection logic.

Works with Claude Code, Codex, and Cursor. Each sends one JSON event on stdin
and reads the exit code as the answer:
  exit 0   no opinion, the normal permission flow runs
  exit 2   block, with stderr as the reason

The README links the hooks reference for each agent.
"""

import json
import sys
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "events.jsonl"

# Proves the block path works before you have any logic.
# Ask the agent to run:  echo STARTER-KIT-CANARY-DENY
CANARY = "STARTER-KIT-CANARY-DENY"


def decide(event):
    """Return a reason to block, or None to let the action through. Replace me."""
    if CANARY in json.dumps(event.get("tool_input", {})):
        return "Starter kit canary string found in the tool input."
    return None


def main():
    event = json.loads(sys.stdin.read())

    # Record every event so you can see what the agent sends.
    LOG_PATH.parent.mkdir(exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as log:
        log.write(json.dumps(event) + "\n")

    reason = decide(event)
    if reason:
        sys.stderr.write(reason + "\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
