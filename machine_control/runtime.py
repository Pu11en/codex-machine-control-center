from __future__ import annotations

import plistlib
from pathlib import Path
from typing import Any


def dotenv_quote(value: str) -> str:
    if "\n" in value or "\r" in value or "\0" in value:
        raise ValueError("Configuration values must be single-line")
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def environment_text(
    token: str,
    owner_id: str,
    receipt: dict[str, Any],
    projects: Path,
    data: Path,
    source: Path,
    backend: str,
    executable: str,
    additional_user_ids: str = "",
) -> str:
    if backend not in {"claude", "codex"}:
        raise ValueError("Backend must be claude or codex")
    values = {
        "DISCORD_BOT_TOKEN": token,
        "DISCORD_OWNER_ID": owner_id,
        "DISCORD_CHANNEL_ID": receipt["channels"]["control-center"],
        "CCDB_CHANNEL_IDS": ",".join(receipt["channels"][c] for c in ("control-center", "workers")),
        "COORDINATION_CHANNEL_ID": receipt["channels"]["workers"],
        "CCDB_BACKEND": backend,
        "CCDB_PERMISSION_MODE": "acceptEdits",
        "CCDB_WORKING_DIR": str(projects),
        "CCDB_PROJECT_ROOTS": str(projects),
        "CCDB_DATA_ROOT": str(data / "relay"),
        "CUSTOM_COGS_DIR": str(source / "extensions" / "project_picker"),
        "CCDB_MENTION_ANYWHERE": "false",
        "CCDB_MONITOR_ALL_CHANNELS": "false",
        "MACHINE_CATEGORY_ID": receipt["category_id"],
        "MAX_CONCURRENT_SESSIONS": "3",
        "SESSION_TIMEOUT_SECONDS": "3600",
        "API_HOST": "127.0.0.1",
        "API_PORT": "9876",
        "PATH": ":".join(
            [
                str(source / ".venv/bin"),
                str(Path(executable).parent),
                "/opt/homebrew/bin",
                "/usr/local/bin",
                "/usr/bin",
                "/bin",
                "/usr/sbin",
                "/sbin",
            ]
        ),
    }
    if additional_user_ids:
        values["CCDB_ADDITIONAL_USER_IDS"] = additional_user_ids
    values["CCDB_CLAUDE_COMMAND" if backend == "claude" else "CCDB_CODEX_COMMAND"] = executable
    return "".join(f"{k}={dotenv_quote(v)}\n" for k, v in values.items())


def launch_agent(source: Path, env: Path, logs: Path) -> bytes:
    return plistlib.dumps(
        {
            "Label": "com.ai.machine-control-center",
            "ProgramArguments": [
                str(source / ".venv" / "bin" / "ccdb"),
                "start",
                "--env",
                str(env),
            ],
            "WorkingDirectory": str(source),
            "RunAtLoad": True,
            "KeepAlive": True,
            "ThrottleInterval": 15,
            "Umask": 0o077,
            "StandardOutPath": str(logs / "relay.stdout.log"),
            "StandardErrorPath": str(logs / "relay.stderr.log"),
        },
        sort_keys=False,
    )
