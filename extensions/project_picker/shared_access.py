"""Add explicitly configured people to this machine relay's authorization set."""

from __future__ import annotations

import os
from typing import Any


async def setup(bot: Any, runner: Any, components: Any) -> None:
    raw = os.getenv("CCDB_ADDITIONAL_USER_IDS", "").strip()
    if not raw:
        return
    values = [value.strip() for value in raw.split(",") if value.strip()]
    if not values or any(not value.isdigit() or not 17 <= len(value) <= 20 for value in values):
        raise ValueError("CCDB_ADDITIONAL_USER_IDS must contain numeric Discord IDs")
    chat = bot.get_cog("ClaudeChatCog")
    if chat is None or chat._allowed_user_ids is None:
        raise RuntimeError("Shared access requires Ebi's configured chat authorization")
    chat._allowed_user_ids.update(int(value) for value in values)
