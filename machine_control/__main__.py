from __future__ import annotations

import argparse
import asyncio
import json
import shutil
import sys
from pathlib import Path

from dotenv import dotenv_values

from .admin import grant_once
from .api import DiscordAPI, DiscordError, private_write, session
from .provision import provision
from .runtime import environment_text, launch_agent


async def run(args: argparse.Namespace) -> None:
    config = dotenv_values(args.env, interpolate=False)
    token = config.get("DISCORD_BOT_TOKEN")
    if not token:
        raise ValueError("DISCORD_BOT_TOKEN is required in --env")
    async with session(token) as transport:
        api = DiscordAPI(transport)
        if args.command == "admin-once":
            print(await grant_once(api, args.guild, args.user, args.state.resolve()))
            return
        for key in ("DISCORD_GUILD_ID", "EXPECTED_BOT_ID", "DISCORD_OWNER_ID"):
            if not config.get(key):
                raise ValueError(f"{key} is required in --env")
        data = args.data.expanduser().resolve()
        source = Path(__file__).resolve().parents[1]
        projects = args.projects.expanduser().resolve()
        executable = shutil.which(args.backend)
        if not executable:
            raise ValueError(
                f"Install and sign in to {args.backend.title()} on this computer first"
            )
        if args.apply and sys.platform != "darwin":
            raise ValueError("The Mac installer must be applied on macOS")
        if not args.apply:
            me = await api.request("GET", "/users/@me")
            if me["id"] != config["EXPECTED_BOT_ID"]:
                raise ValueError("Token belongs to a different bot than EXPECTED_BOT_ID")
            channels = await api.request("GET", f"/guilds/{config['DISCORD_GUILD_ID']}/channels")
            print(
                json.dumps(
                    {
                        "mode": "preview",
                        "category": args.category,
                        "existing_categories": [c["name"] for c in channels if c["type"] == 4],
                        "projects": str(projects),
                        "state": str(data),
                        "backend": args.backend,
                        "executable": executable,
                    },
                    indent=2,
                )
            )
            return
        if not (source / ".venv" / "bin" / "ccdb").exists():
            raise ValueError("Run uv sync --extra relay first")
        receipt = await provision(
            api,
            str(config["DISCORD_GUILD_ID"]),
            str(config["EXPECTED_BOT_ID"]),
            str(config["DISCORD_OWNER_ID"]),
            args.category,
            data / "provision.json",
        )
        projects.mkdir(parents=True, exist_ok=True)
        logs = data / "logs"
        logs.mkdir(parents=True, exist_ok=True, mode=0o700)
        env_path = data / "relay.env"
        # Runtime settings belong to the operator after first setup.
        if not env_path.exists():
            private_write(
                env_path,
                environment_text(
                    token,
                    str(config["DISCORD_OWNER_ID"]),
                    receipt,
                    projects,
                    data,
                    source,
                    args.backend,
                    executable,
                ),
            )
        plist_path = data / "com.ai.machine-control-center.plist"
        private_write(plist_path, launch_agent(source, env_path, logs))
        print(
            json.dumps(
                {
                    "status": "provisioned; start and verify on macOS",
                    "category_id": receipt["category_id"],
                    "channels": receipt["channels"],
                    "environment": str(env_path),
                    "launch_agent": str(plist_path),
                },
                indent=2,
            )
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Per-computer Discord control center setup")
    sub = parser.add_subparsers(dest="command", required=True)
    setup = sub.add_parser("setup", help="Preview; add --apply on the target Mac to provision")
    setup.add_argument("--env", type=Path, required=True)
    setup.add_argument("--category", default="IMAC CODEX CONTROL CENTER")
    setup.add_argument("--backend", choices=("claude", "codex"), default="codex")
    setup.add_argument("--projects", type=Path, default=Path.home() / "Developer")
    setup.add_argument(
        "--data", type=Path, default=Path.home() / "Library/Application Support/AIMachineControl"
    )
    setup.add_argument("--apply", action="store_true")
    admin = sub.add_parser("admin-once", help="Assign an authorized account Admin on join, once")
    admin.add_argument("--env", type=Path, required=True)
    admin.add_argument("--guild", required=True)
    admin.add_argument("--user", required=True)
    admin.add_argument("--state", type=Path, required=True)
    try:
        asyncio.run(run(parser.parse_args()))
    except (ValueError, DiscordError, OSError) as error:
        parser.exit(1, f"Setup stopped: {error}\n")


if __name__ == "__main__":
    main()
