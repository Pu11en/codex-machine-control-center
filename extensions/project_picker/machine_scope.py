"""Scope this application's slash commands to its two machine chat channels."""

from __future__ import annotations

import os
from typing import Any


async def setup(bot: Any, runner: Any, components: Any) -> None:
    channel_ids = {
        int(x.strip()) for x in os.getenv("CCDB_CHANNEL_IDS", "").split(",") if x.strip().isdigit()
    }
    if not channel_ids:
        raise ValueError("Machine command scope requires CCDB_CHANNEL_IDS")
    original = bot.tree.interaction_check

    async def machine_check(interaction: Any) -> bool:
        channel = interaction.channel
        root = getattr(channel, "parent_id", None)
        if getattr(channel, "id", None) not in channel_ids and root not in channel_ids:
            await interaction.response.send_message(
                "Use this computer's control-center or workers channel, or a thread inside them.",
                ephemeral=True,
            )
            return False
        return await original(interaction)

    bot.tree.interaction_check = machine_check
