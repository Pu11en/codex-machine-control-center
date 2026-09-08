from __future__ import annotations

import asyncio
import json
import os
import re
from pathlib import Path
from typing import Any

import aiohttp


class DiscordError(RuntimeError):
    def __init__(self, status: int, code: int | None = None) -> None:
        self.status = status
        self.code = code
        super().__init__(f"Discord HTTP {status}, code {code}")


def snowflake(value: str) -> str:
    if not re.fullmatch(r"[0-9]{17,20}", value):
        raise ValueError("Expected a permanent numeric Discord ID")
    return value


def private_write(path: Path, content: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temp = path.with_name(path.name + ".tmp")
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(content.encode() if isinstance(content, str) else content)
    temp.chmod(0o600)
    temp.replace(path)


def save_receipt(path: Path, receipt: dict[str, Any]) -> None:
    private_write(path, json.dumps(receipt, indent=2) + "\n")


class DiscordAPI:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session = session

    async def request(self, method: str, route: str, payload: Any = None) -> Any:
        for _ in range(4):
            async with self.session.request(
                method,
                "https://discord.com/api/v10" + route,
                json=payload,
                allow_redirects=False,
            ) as response:
                if response.status == 204:
                    return None
                try:
                    data = await response.json()
                except (ValueError, aiohttp.ContentTypeError):
                    raise DiscordError(response.status) from None
                if response.status == 429:
                    await asyncio.sleep(min(float(data.get("retry_after", 1)), 30))
                    continue
                if not 200 <= response.status < 300:
                    raise DiscordError(response.status, data.get("code"))
                return data
        raise DiscordError(429)


def session(token: str) -> aiohttp.ClientSession:
    return aiohttp.ClientSession(
        headers={
            "Authorization": "Bot " + token,
            "User-Agent": (
                "DiscordBot (https://github.com/Pu11en/codex-machine-control-center, 0.1)"
            ),
        },
        timeout=aiohttp.ClientTimeout(total=30),
    )
