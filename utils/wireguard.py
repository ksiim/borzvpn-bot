import httpx
from typing import Optional, List
from config import WIREGUARD_BASE_URL, WIREGUARD_PASSWORD


class WireGuard:
    def __init__(self):
        self.base_url = WIREGUARD_BASE_URL.rstrip("/")
        self.password = WIREGUARD_PASSWORD
        self.client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self.client = httpx.AsyncClient(base_url=self.base_url, headers={"Content-Type": "application/json"})
        await self.create_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.delete_session()
        await self.close()

    async def create_session(self):
        resp = await self.client.post("/session", json={"password": self.password})
        resp.raise_for_status()
        return resp.json()

    async def delete_session(self):
        resp = await self.client.delete("/session")
        resp.raise_for_status()
        return True

    async def get_clients(self) -> List[dict]:
        resp = await self.client.get("/wireguard/client")
        resp.raise_for_status()
        return resp.json()

    async def create_client(self, name: str) -> dict:
        resp = await self.client.post("/wireguard/client", json={"name": str(name)})
        resp.raise_for_status()
        return resp.json()

    async def delete_client(self, client_id: str):
        resp = await self.client.delete(f"/wireguard/client/{client_id}")
        resp.raise_for_status()
        return True

    async def enable_client(self, client_id: str):
        resp = await self.client.post(f"/wireguard/client/{client_id}/enable")
        resp.raise_for_status()
        return True

    async def disable_client(self, client_id: str):
        resp = await self.client.post(f"/wireguard/client/{client_id}/disable")
        resp.raise_for_status()
        return True

    async def update_client_name(self, client_id: str, name: str):
        resp = await self.client.put(f"/wireguard/client/{client_id}/name/", json={"name": str(name)})
        resp.raise_for_status()
        return resp.json()

    async def update_client_address(self, client_id: str, address: str):
        resp = await self.client.put(f"/wireguard/client/{client_id}/address/", json={"address": address})
        resp.raise_for_status()
        return resp.json()

    async def get_qrcode(self, client_id: str) -> bytes:
        resp = await self.client.get(f"/wireguard/client/{client_id}/qrcode.svg")
        resp.raise_for_status()
        return resp.content

    async def get_configuration_file(self, client_id: str) -> bytes:
        resp = await self.client.get(f"/wireguard/client/{client_id}/configuration")
        resp.raise_for_status()
        return resp.content

    async def close(self):
        if self.client:
            await self.client.aclose()
