from __future__ import annotations

from types import SimpleNamespace

import pytest
from shared_access import setup


@pytest.mark.asyncio
async def test_additional_users_join_existing_relay_authorization(monkeypatch):
    monkeypatch.setenv("CCDB_ADDITIONAL_USER_IDS", "100000000000000004,100000000000000005")
    allowed = {100000000000000003}
    chat = SimpleNamespace(_allowed_user_ids=allowed)
    skill = SimpleNamespace(_allowed_user_ids=allowed)
    bot = SimpleNamespace(
        get_cog=lambda name: {"ClaudeChatCog": chat, "SkillCommandCog": skill}.get(name)
    )
    await setup(bot, None, None)
    assert chat._allowed_user_ids == {100000000000000003, 100000000000000004, 100000000000000005}
    assert skill._allowed_user_ids is chat._allowed_user_ids


@pytest.mark.asyncio
async def test_additional_user_ids_fail_closed_on_invalid_value(monkeypatch):
    monkeypatch.setenv("CCDB_ADDITIONAL_USER_IDS", "friend-name")
    bot = SimpleNamespace(get_cog=lambda name: SimpleNamespace(_allowed_user_ids={1}))
    with pytest.raises(ValueError, match="numeric Discord IDs"):
        await setup(bot, None, None)
