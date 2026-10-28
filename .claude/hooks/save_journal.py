"""Copy this project's Claude Code session logs into journal/.

02-120 build journal hook. Claude Code runs this at the start and end of every
session in this folder. It copies every session log that Claude Code keeps for
this folder, so sessions from before you set this up are included too.
You can also run it by hand: python save_journal.py

Personal details (email addresses, IP addresses, the Windows username in file
paths) are replaced with placeholders as each log is copied.
"""

import json
import os
import re
import sys
from pathlib import Path


def project_dir() -> Path:
    env_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_dir:
        return Path(env_dir)
    return Path(__file__).resolve().parent.parent.parent


def read_hook_input() -> dict:
    if sys.stdin is None or sys.stdin.isatty():
        return {}
    try:
        return json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return {}


def log_folder(hook_input: dict, project: Path) -> Path:
    transcript_path = hook_input.get("transcript_path")
    if transcript_path:
        return Path(transcript_path).expanduser().parent
    slug = re.sub(r"[^A-Za-z0-9]", "-", str(project.resolve()))
    return Path.home() / ".claude" / "projects" / slug


# "\\?\." also catches dots written as "\." inside regex patterns in commands.
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\\?\.[A-Za-z0-9-]+)+")
IPV4 = re.compile(r"(?<![\d.])(?:\d{1,3}\\?\.){3}\d{1,3}(?!\d|\.\d)")


def redact(text: str, username: str) -> str:
    text = EMAIL.sub("[email]", text)
    text = IPV4.sub("[ip]", text)
    if username:
        text = re.sub(re.escape(username), "[user]", text, flags=re.IGNORECASE)
    return text


def redact_value(value, username: str):
    """Redact every string (keys too) inside a parsed JSON value."""
    if isinstance(value, str):
        return redact(value, username)
    if isinstance(value, list):
        return [redact_value(v, username) for v in value]
    if isinstance(value, dict):
        return {redact(k, username): redact_value(v, username) for k, v in value.items()}
    return value


def redact_line(line: str, username: str) -> str:
    """Redact one JSONL line, keeping it valid JSON."""
    if not line.strip():
        return line
    try:
        record = json.loads(line)
    except json.JSONDecodeError:
        return redact(line, username)
    return json.dumps(redact_value(record, username), ensure_ascii=False) + "\n"


def main() -> None:
    project = project_dir()
    source = log_folder(read_hook_input(), project)
    if not source.is_dir():
        print(f"save_journal: no Claude Code logs found at {source}", file=sys.stderr)
        return
    journal = project / "journal"
    journal.mkdir(exist_ok=True)
    username = Path.home().name
    copied_count = 0
    for log_file in sorted(source.glob("*.jsonl")):
        destination = journal / log_file.name
        source_mtime = log_file.stat().st_mtime
        if destination.exists() and destination.stat().st_mtime == source_mtime:
            continue
        with open(log_file, encoding="utf-8") as src, open(destination, "w", encoding="utf-8") as dst:
            for line in src:
                dst.write(redact_line(line, username))
        os.utime(destination, (source_mtime, source_mtime))  # marks it up to date
        copied_count += 1
    print(f"save_journal: {copied_count} session log(s) updated in {journal}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # a journal problem must never block a Claude Code session
        print(f"save_journal: {error}", file=sys.stderr)
