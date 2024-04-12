import httpx


async def get_latest_eth_block() -> int:
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.blockcypher.com/v1/eth/main")
        return r.json()["height"]
