from __future__ import annotations

import json
import plistlib

import pytest

from machine_control.admin import grant_once
from machine_control.api import DiscordError
from machine_control.provision import provision
from machine_control.runtime import environment_text, launch_agent

GUILD = "100000000000000001"
BOT = "100000000000000002"
OWNER = "100000000000000003"
USER = "100000000000000004"


class FakeDiscord:
    def __init__(self):
        self.channels = []
        self.roles = [
            {"id": GUILD, "name": "@everyone", "position": 0, "permissions": "0"},
            {"id": "botrole", "name": "Bot", "position": 3, "permissions": "8"},
        ]
        self.member = None
        self.calls = []

    async def request(self, method, route, payload=None):
        self.calls.append((method, route, payload))
        if route == "/users/@me":
            return {"id": BOT}
        if route == f"/guilds/{GUILD}/members/{BOT}":
            return {"user": {"id": BOT}, "roles": ["botrole"]}
        if route == f"/guilds/{GUILD}/members/{USER}":
            if self.member is None:
                raise DiscordError(404, 10007)
            return self.member
        if route == f"/guilds/{GUILD}/roles":
            if method == "GET":
                return self.roles
            role = dict(payload, id="adminrole", position=1, managed=False)
            self.roles.append(role)
            return role
        if route == f"/guilds/{GUILD}/channels":
            if method == "GET":
                return self.channels
            channel = dict(payload, id=str(200000000000000000 + len(self.channels)))
            self.channels.append(channel)
            return channel
        if method == "PUT" and route.endswith("/roles/adminrole"):
            self.member["roles"].append("adminrole")
            return None
        raise AssertionError((method, route, payload))


@pytest.mark.asyncio
async def test_admin_waits_for_exact_account_then_grants_once(tmp_path):
    api = FakeDiscord()
    state = tmp_path / "grant.json"
    assert await grant_once(api, GUILD, USER, state) == "waiting"
    assert not any(c[0] == "PUT" for c in api.calls)
    api.member = {"user": {"id": USER}, "roles": []}
    assert await grant_once(api, GUILD, USER, state) == "granted"
    assert api.member["roles"] == ["adminrole"]
    api.member["roles"] = []  # A later manual removal must be respected.
    assert await grant_once(api, GUILD, USER, state) == "complete"
    assert api.member["roles"] == []
    receipt = json.loads(state.read_text())
    assert receipt["user_id"] == USER
    assert receipt["status"] == "complete"


@pytest.mark.asyncio
async def test_admin_rejects_reused_receipt_for_different_identity(tmp_path):
    state = tmp_path / "grant.json"
    state.write_text(json.dumps({"guild_id": "different", "user_id": USER, "status": "complete"}))
    with pytest.raises(ValueError, match="identity"):
        await grant_once(FakeDiscord(), GUILD, USER, state)


@pytest.mark.asyncio
async def test_admin_rejects_role_above_bot(tmp_path):
    api = FakeDiscord()
    api.roles.append(
        {
            "id": "adminrole",
            "name": "Server Admin",
            "position": 5,
            "permissions": "8",
            "managed": False,
        }
    )
    with pytest.raises(ValueError, match="above"):
        await grant_once(api, GUILD, USER, tmp_path / "state.json")
    assert not any(c[0] == "PUT" for c in api.calls)


@pytest.mark.asyncio
async def test_admin_role_position_tie_uses_discord_id_order(tmp_path):
    api = FakeDiscord()
    api.roles[1]["id"] = "100000000000000010"
    api.roles[1]["position"] = 1
    api.roles.append(
        {
            "id": "100000000000000020",
            "name": "Server Admin",
            "position": 1,
            "permissions": "8",
            "managed": False,
        }
    )
    original = api.request

    async def request(method, route, payload=None):
        if route.endswith("/members/" + BOT):
            return {"user": {"id": BOT}, "roles": ["100000000000000010"]}
        return await original(method, route, payload)

    api.request = request
    assert await grant_once(api, GUILD, USER, tmp_path / "state.json") == "waiting"


@pytest.mark.asyncio
async def test_admin_only_treats_unknown_member_as_waiting(tmp_path):
    api = FakeDiscord()
    original = api.request

    async def request(method, route, payload=None):
        if route.endswith("/members/" + USER):
            raise DiscordError(403, 50013)
        return await original(method, route, payload)

    api.request = request
    with pytest.raises(DiscordError):
        await grant_once(api, GUILD, USER, tmp_path / "state.json")


@pytest.mark.asyncio
async def test_provision_is_idempotent_and_does_not_touch_lenovo(tmp_path):
    api = FakeDiscord()
    original = {"id": "lenovo", "name": "CODEX CONTROL CENTER", "type": 4}
    api.channels.append(original.copy())
    state = tmp_path / "setup.json"
    receipt = await provision(api, GUILD, BOT, OWNER, "IMAC CODEX CONTROL CENTER", state)
    assert len(api.channels) == 7  # Old category + new category + five channels.
    assert api.channels[0] == original
    assert set(receipt["channels"]) == {
        "control-center",
        "workers",
        "cheat-sheet",
        "🎙️ Auto Transcripts",
        "voice-transcripts",
    }
    assert await provision(api, GUILD, BOT, OWNER, "IMAC CODEX CONTROL CENTER", state) == receipt
    assert len(api.channels) == 7
    assert not any(method in ("PATCH", "DELETE") for method, _, _ in api.calls)


@pytest.mark.asyncio
async def test_provision_refuses_wrong_bot_before_writes(tmp_path):
    api = FakeDiscord()
    with pytest.raises(ValueError, match="bot"):
        await provision(api, GUILD, OWNER, OWNER, "IMAC", tmp_path / "receipt.json")
    assert all(c[0] == "GET" for c in api.calls)


@pytest.mark.asyncio
async def test_existing_category_without_receipt_is_not_adopted(tmp_path):
    api = FakeDiscord()
    api.channels.append({"id": "existing", "name": "IMAC", "type": 4})
    with pytest.raises(ValueError, match="receipt"):
        await provision(api, GUILD, BOT, OWNER, "IMAC", tmp_path / "receipt.json")


def test_codex_runtime_uses_mac_paths_and_scoped_channels(tmp_path):
    receipt = {
        "bot_id": BOT,
        "guild_id": GUILD,
        "category_id": "category",
        "channels": {"control-center": "111", "workers": "222"},
    }
    env = environment_text(
        "test-token",
        OWNER,
        receipt,
        tmp_path / "My Projects",
        tmp_path / "data",
        tmp_path / "source",
        "codex",
        "/opt/homebrew/bin/codex",
    )
    assert "CCDB_MENTION_ANYWHERE='false'" in env
    assert "CCDB_CHANNEL_IDS='111,222'" in env
    assert "CCDB_BACKEND='codex'" in env
    assert "/home/drewp" not in env
    from io import StringIO

    from dotenv import dotenv_values

    parsed = dotenv_values(stream=StringIO(env), interpolate=False)
    assert parsed["CCDB_WORKING_DIR"] == str(tmp_path / "My Projects")
    assert parsed["DISCORD_BOT_TOKEN"] == "test-token"
    assert parsed["CCDB_CODEX_COMMAND"] == "/opt/homebrew/bin/codex"


def test_claude_runtime_uses_friends_subscription_and_not_codex(tmp_path):
    receipt = {"category_id": "category", "channels": {"control-center": "111", "workers": "222"}}
    env = environment_text(
        "friend-token",
        USER,
        receipt,
        tmp_path / "Projects",
        tmp_path / "data",
        tmp_path / "source",
        "claude",
        "/Users/friend/.local/bin/claude",
    )
    from io import StringIO

    from dotenv import dotenv_values

    parsed = dotenv_values(stream=StringIO(env), interpolate=False)
    assert parsed["CCDB_BACKEND"] == "claude"
    assert parsed["CCDB_CLAUDE_COMMAND"] == "/Users/friend/.local/bin/claude"
    assert "CCDB_CODEX_COMMAND" not in parsed
    assert parsed["DISCORD_OWNER_ID"] == USER
    assert parsed["CCDB_PERMISSION_MODE"] == "acceptEdits"


def test_launch_agent_preserves_spaces_and_keeps_credentials_out(tmp_path):
    raw = launch_agent(tmp_path / "My Repo", tmp_path / "private bot.env", tmp_path / "logs")
    plist = plistlib.loads(raw)
    assert plist["ProgramArguments"][-1] == str(tmp_path / "private bot.env")
    assert plist["WorkingDirectory"] == str(tmp_path / "My Repo")
    assert plist["RunAtLoad"] and plist["KeepAlive"]
    assert plist["Label"] == "com.ai.machine-control-center"
    assert "DISCORD_BOT_TOKEN" not in plist.get("EnvironmentVariables", {})
