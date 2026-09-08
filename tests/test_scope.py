from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from machine_scope import setup


@pytest.mark.asyncio
async def test_slash_scope_preserves_original_check(monkeypatch):
    monkeypatch.setenv("CCDB_CHANNEL_IDS", "111,222")
    original = AsyncMock(return_value=True)
    bot = SimpleNamespace(tree=SimpleNamespace(interaction_check=original))
    await setup(bot, None, None)
    response = SimpleNamespace(send_message=AsyncMock())
    outside = SimpleNamespace(channel=SimpleNamespace(id=333, parent_id=None), response=response)
    assert not await bot.tree.interaction_check(outside)
    original.assert_not_awaited()
    inside = SimpleNamespace(channel=SimpleNamespace(id=444, parent_id=111), response=response)
    assert await bot.tree.interaction_check(inside)
    original.assert_awaited_once_with(inside)
    original.return_value = False
    assert not await bot.tree.interaction_check(inside)


@pytest.mark.asyncio
async def test_scope_fails_closed_without_config(monkeypatch):
    monkeypatch.delenv("CCDB_CHANNEL_IDS", raising=False)
    bot = SimpleNamespace(tree=SimpleNamespace(interaction_check=AsyncMock()))
    with pytest.raises(ValueError):
        await setup(bot, None, None)
