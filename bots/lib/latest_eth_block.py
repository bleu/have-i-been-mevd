import logging
import httpx


async def get_latest_eth_block() -> int:
    logging.info(f"Fetching latest eth block")
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.blockcypher.com/v1/eth/main")
        return r.json()["height"]
