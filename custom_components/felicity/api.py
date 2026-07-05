"""Felicity Solar API."""

from __future__ import annotations

import base64

import httpx
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

BASE_URL = "https://open-api.felicitysolar.com"

PUBLIC_KEY = b"""-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAK0GDivaRzIKeTmQnAxAYh2LChuHWDp0
yHZ0zIvm+Eoi7J+rx7phqR7EtkBDO3HWqAXVkNDeeQaU32P5w1Q4FVUCAwEAAQ==
-----END PUBLIC KEY-----"""


class FelicityApi:

    def __init__(self, username: str, password: str, device_sn: str):
        self.username = username
        self.password = password
        self.device_sn = device_sn
        self.token = None

    def encrypt_password(self) -> str:

        key = load_pem_public_key(PUBLIC_KEY)

        encrypted = key.encrypt(
            self.password.encode("utf-8"),
            padding.PKCS1v15(),
        )

        return base64.b64encode(encrypted).decode()

    async def login(self):

        payload = {
            "userName": self.username,
            "password": self.encrypt_password(),
        }

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.post(
                f"{BASE_URL}/openApi/sec/login",
                json=payload,
            )

        response.raise_for_status()

        data = response.json()

        if data["code"] != 200:
            raise Exception(data)

        self.token = data["data"]["token"]

    async def get_latest(self):

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
                f"{BASE_URL}/openApi/data/devicesDataHistory",
                headers=headers,
                params=params,
            )

        response.raise_for_status()

        return response.json()

    async def get_basic(self):

        headers = {
            "Authorization": self.token,
            "Lang": "en_US",
        }

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.get(
                f"{BASE_URL}/openApi/data/deviceDataBasic/{self.device_sn}",
                headers=headers,
            )

        response.raise_for_status()

        return response.json()

    async def get_energy_today(self):

        headers = {
            "Authorization": self.token,
            "Lang": "en_US",
        }

        params = {
            "deviceSn": self.device_sn,
            "timeDimension": "day",
            "pageNum": 1,
            "pageSize": 1,
        }

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.get(
                f"{BASE_URL}/openApi/data/deviceDataEnergy",
                headers=headers,
                params=params,
            )

        response.raise_for_status()

        return response.json()