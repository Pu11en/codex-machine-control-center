"""One specifically authorized account, one verified Administrator grant."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .api import DiscordError, save_receipt, snowflake


async def grant_once(api: Any, guild_id: str, user_id: str, state: Path) -> str:
    snowflake(guild_id)
    snowflake(user_id)
    receipt = (
        json.loads(state.read_text())
        if state.exists()
        else {
            "guild_id": guild_id,
            "user_id": user_id,
            "status": "pending",
        }
    )
    if receipt["guild_id"] != guild_id or receipt["user_id"] != user_id:
        raise ValueError("Receipt identity differs from authorized target")
    if receipt["status"] == "complete":
        return "complete"
    me = await api.request("GET", "/users/@me")
    bot = await api.request("GET", f"/guilds/{guild_id}/members/{me['id']}")
    roles = await api.request("GET", f"/guilds/{guild_id}/roles")
    bot_roles = [r for r in roles if r["id"] in [guild_id, *bot["roles"]]]
    permissions = 0
    for role in bot_roles:
        permissions |= int(role["permissions"])
    if not permissions & 8:
        raise ValueError("Administrator is required to provision this Administrator role")
    candidates = (
        [r for r in roles if r["id"] == receipt.get("role_id")]
        if receipt.get("role_id")
        else [r for r in roles if r["name"] == "Server Admin"]
    )
    if len(candidates) > 1:
        raise ValueError("Multiple Server Admin roles; select the intended role in the receipt")
    if receipt.get("role_id") and not candidates:
        raise ValueError("The recorded admin role was removed; review before granting again")
    if candidates:
        role = candidates[0]
    else:
        role = await api.request(
            "POST",
            f"/guilds/{guild_id}/roles",
            {
                "name": "Server Admin",
                "permissions": "8",
                "hoist": True,
                "mentionable": False,
            },
        )
        # Discord may have shifted positions when it inserted the new role.
        roles = await api.request("GET", f"/guilds/{guild_id}/roles")
        bot_roles = [r for r in roles if r["id"] in bot["roles"]]
    if role.get("managed") or not int(role["permissions"]) & 8:
        raise ValueError("Selected role must be an unmanaged Administrator role")
    if not any(
        r["position"] > role["position"]
        or (r["position"] == role["position"] and int(r["id"]) < int(role["id"]))
        for r in bot_roles
        if r["id"] != guild_id
    ):
        raise ValueError("Move the bot role above Server Admin before assigning it")
    receipt["role_id"] = role["id"]
    save_receipt(state, receipt)
    try:
        member = await api.request("GET", f"/guilds/{guild_id}/members/{user_id}")
    except DiscordError as error:
        if error.status == 404 and error.code == 10007:
            return "waiting"
        raise
    if member["user"]["id"] != user_id:
        raise ValueError("Member response does not match authorized identity")
    if role["id"] not in member["roles"]:
        await api.request("PUT", f"/guilds/{guild_id}/members/{user_id}/roles/{role['id']}")
    verified = await api.request("GET", f"/guilds/{guild_id}/members/{user_id}")
    if role["id"] not in verified["roles"]:
        raise RuntimeError("Administrator assignment was not verified")
    receipt["status"] = "complete"
    save_receipt(state, receipt)
    return "granted"
