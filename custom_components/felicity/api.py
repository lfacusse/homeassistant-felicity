"""Felicity Solar API."""

from __future__ import annotations

import base64

import httpx
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

from .const import API_URL

PUBLIC_KEY = b"""-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAK0GDivaRzIKeTmQnAxAYh2LChuHWDp0
yHZ0zIvm+Eoi7J+rx7phqR7EtkBDO3HWqAXVkNDeeQaU32P5w1Q4FVUCAwEAAQ==
-----END PUBLIC KEY-----"""


class FelicityApi:
    """Felicity Solar cloud API."""

    def __init__(self, username: str, password: str, device_sn: str):
        self.username = username
        self.password = password
        self.device_sn = device_sn
        self.token: str | None = None

    def _encrypt_password(self) -> str:
        """Encrypt password using Felicity public key."""
        key = load_pem_public_key(PUBLIC_KEY)

        encrypted = key.encrypt(
            self.password.encode("utf-8"),
            padding.PKCS1v15(),
        )

        return base64.b64encode(encrypted).decode()

    async def login(self) -> None:
        """Authenticate with Felicity cloud."""

        payload = {
            "userName": self.username,
            "password": self._encrypt_password(),
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{API_URL}/openApi/sec/login",
                json=payload,
            )

        response.raise_for_status()

        data = response.json()

        if data["code"] != 200:
            raise RuntimeError(data["message"])

        self.token = data["data"]["token"]

    async def get_latest(self) -> dict:
        """Return latest inverter data."""

        if self.token is None:
            await self.login()

        headers = {
            "Authorization": self.token,
            "Lang": "en_US",
        }

        params = {
            "deviceSnList": self.device_sn,
            "queryType": 0,
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_URL}/openApi/data/devicesDataHistory",
                headers=headers,
                params=params,
            )

        response.raise_for_status()

        data = response.json()

        if data["code"] != 200:
            raise RuntimeError(data["message"])

        return data