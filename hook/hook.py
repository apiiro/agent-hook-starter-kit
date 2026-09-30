#!/usr/bin/env python3
"""Starter hook for coding agents. The wiring is provided, the decisions are yours.

Works with Claude Code, Codex, and Cursor. Each sends one JSON event on stdin
and reads the exit code as the answer:
  exit 0   no opinion, the normal permission flow runs
  exit 2   block, with stderr as the reason

Provided: the registration files run this script on one hook, the one that
fires before every tool call. Which hooks to use is your decision. When a
shell command installs or clones a local folder, decide() also gets that
folder. The spotting is deliberately naive. The README lists what it covers.

Yours: decide(). Take it wherever you want.
"""

import json
import os
import re
import shlex
import sys
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "events.jsonl"
CANARY = "STARTER-KIT-CANARY"


def decide(event, folders):
    """Return a reason to block, or None to allow. This is the function to write.

    event     the agent's tool call, exactly as the agent sent it. Every tool
              call arrives here, not only installs.
    folders   local source folders the command installs or clones, as
              {text in the command: pathlib.Path}. Empty for anything else.
              Nothing in them has been run. They are the real folders, so do
              not modify them.
    """
    for source, folder in folders.items():
        if (folder / CANARY).exists():  # Proves the wiring. Remove it.
            return "Starter kit canary file found in %s" % source
    return None


# --- Provided interception. Deliberately naive. ------------------------------

SHELL_TOOLS = {"Bash", "Shell"}
COMMANDS = {("pip", "install"), ("pip3", "install"), ("npm", "install"),
            ("npm", "i"), ("npm", "add"), ("git", "clone")}


def requested_folders(command, cwd):
    """Yield (source, folder) for each local folder a plain command brings in."""
    for segment in re.split(r"&&|\|\||[;|\n]", command):
        try:
            words = shlex.split(segment)
        except ValueError:
            continue
        if tuple(words[:2]) not in COMMANDS:
            continue
        for word in words[2:]:
            folder = Path(cwd, os.path.expanduser(word))
            if not word.startswith("-") and folder.is_dir():
                yield word, folder


def log(record):
    LOG_PATH.parent.mkdir(exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")


def main():
    event = json.loads(sys.stdin.read())
    log({"event": event})

    tool_input = event.get("tool_input")
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    folders = {}
    if event.get("tool_name") in SHELL_TOOLS and isinstance(command, str):
        folders = dict(requested_folders(command, event.get("cwd") or os.getcwd()))

    reason = decide(event, folders)
    log({"folders": list(folders), "blocked": reason})
    if reason:
        sys.stderr.write(reason + "\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
