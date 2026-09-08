"""Create only resources owned by this machine's durable provisioning receipt."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .api import save_receipt, snowflake

VIEW = 1 << 10
SEND = 1 << 11
THREAD_SEND = 1 << 38
CREATE_THREADS = (1 << 35) | (1 << 36)
BOT_ALLOW = sum(1 << i for i in (6, 10, 11, 13, 14, 15, 16, 20, 21, 24, 31, 34, 35, 36, 38))
CHANNELS = (
    ("cheat-sheet", 0, "Machine-local project workflow and GitHub handoff guide."),
    ("control-center", 0, "Use /cdnew to select a local project; continue inside its thread."),
    ("workers", 0, "Worker conversations and coordination for this computer."),
    ("🎙️ Auto Transcripts", 2, None),
    (
        "voice-transcripts",
        0,
        "Private speaker-attributed transcripts from this machine's voice room.",
    ),
)


async def provision(
    api: Any, guild_id: str, bot_id: str, owner_id: str, category: str, state: Path
) -> dict[str, Any]:
    for value in (guild_id, bot_id, owner_id):
        snowflake(value)
    if not category.strip() or len(category) > 100:
        raise ValueError("Category name must contain 1–100 characters")
    me = await api.request("GET", "/users/@me")
    if me["id"] != bot_id:
        raise ValueError("Token belongs to a different bot than EXPECTED_BOT_ID")
    await api.request("GET", f"/guilds/{guild_id}/members/{bot_id}")
    existing = await api.request("GET", f"/guilds/{guild_id}/channels")
    receipt = (
        json.loads(state.read_text())
        if state.exists()
        else {
            "guild_id": guild_id,
            "bot_id": bot_id,
            "owner_id": owner_id,
            "category_name": category,
            "channels": {},
        }
    )
    if any(
        receipt[k] != v
        for k, v in {
            "guild_id": guild_id,
            "bot_id": bot_id,
            "owner_id": owner_id,
            "category_name": category,
        }.items()
    ):
        raise ValueError("Receipt identity differs; use a separate machine state directory")
    overwrites = [
        {"id": guild_id, "type": 0, "allow": "0", "deny": str(VIEW)},
        {"id": bot_id, "type": 1, "allow": str(BOT_ALLOW), "deny": "0"},
        {"id": owner_id, "type": 1, "allow": str(BOT_ALLOW), "deny": "0"},
    ]
    if not receipt.get("category_id"):
        if any(c["type"] == 4 and c["name"] == category for c in existing):
            raise ValueError("Category already exists without its receipt; inspect before adopting")
        created = await api.request(
            "POST",
            f"/guilds/{guild_id}/channels",
            {
                "name": category,
                "type": 4,
                "permission_overwrites": overwrites,
            },
        )
        receipt["category_id"] = created["id"]
        save_receipt(state, receipt)
    elif not any(c["id"] == receipt["category_id"] and c["type"] == 4 for c in existing):
        raise ValueError("Recorded category is missing; inspect before recreating")
    for position, (name, kind, topic) in enumerate(CHANNELS):
        if name in receipt["channels"]:
            if not any(
                c["id"] == receipt["channels"][name]
                and c.get("parent_id") == receipt["category_id"]
                and c["type"] == kind
                for c in existing
            ):
                raise ValueError(f"Recorded channel {name} is missing or moved; inspect first")
            continue
        if any(
            c.get("parent_id") == receipt["category_id"] and c["name"] == name for c in existing
        ):
            raise ValueError(f"Channel {name} exists without a receipt; inspect before adopting")
        channel_overwrites = [dict(o) for o in overwrites]
        if name == "cheat-sheet":
            channel_overwrites[0]["deny"] = str(VIEW | SEND | THREAD_SEND | CREATE_THREADS)
            # Server administrators retain access, as Discord requires.
        payload = {
            "name": name,
            "type": kind,
            "parent_id": receipt["category_id"],
            "position": position,
            "permission_overwrites": channel_overwrites,
        }
        if topic:
            payload["topic"] = topic
        created = await api.request("POST", f"/guilds/{guild_id}/channels", payload)
        receipt["channels"][name] = created["id"]
        save_receipt(state, receipt)
    return receipt
