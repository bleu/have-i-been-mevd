import asyncio
import logging
import httpx
import pandas as pd
from retry_async import retry
from lib.latest_eth_block import get_latest_eth_block
from lib.zero_mev.transformers import preprocess


API_BASE_URL = "https://data.zeromev.org/v1"
MAX_CALLS_PER_SECOND = 5


async def get_all_mev_transactions_related_to_address(address: str) -> pd.DataFrame:
    logging.info(f"Getting all mev transactions related to {address}")
    params = {"address_from": address, "page": 1}
    all_data = []
    while True:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{API_BASE_URL}/mevTransactions", params=params)
        data = r.json()
        all_data.extend(data)
        if not data or len(data) < 1000:
            break
        params["page"] += 1
    return pd.DataFrame(data=all_data)


async def get_all_mev_transactions_on_last_week(**preprocess_kwargs) -> pd.DataFrame:
    logging.info(f"Getting all last week mev transactions")
    latest_eth_block_number = await get_latest_eth_block()
    eth_block_number_1_week_ago = (
        latest_eth_block_number - 46523
    )  # 1 week approx 46523 blocks

    tasks = []
    sem = asyncio.Semaphore(MAX_CALLS_PER_SECOND)

    async with httpx.AsyncClient() as client:
        for block in range(eth_block_number_1_week_ago, latest_eth_block_number, 100):
            task = asyncio.create_task(
                bounded_fetch_with_preprocess(
                    sem, client, block, 100, **preprocess_kwargs
                )
            )
            tasks.append(task)

            if len(tasks) >= MAX_CALLS_PER_SECOND:
                await asyncio.sleep(1)

        responses = [response for response in await asyncio.gather(*tasks)]
        return pd.concat(responses)


@retry(
    exceptions=(
        httpx.HTTPStatusError,
        httpx.ReadTimeout,
        httpx.ConnectTimeout,
        httpx.ReadError,
    ),
    is_async=True,
    tries=3,
    delay=1,
)
async def fetch_all_mev_from_block(
    client: httpx.AsyncClient, block_number: int, count: int = 100
):
    logging.info(
        f"Fetching all mev transaction from block {block_number} to {block_number+count}"
    )
    url = f"{API_BASE_URL}/mevBlock"
    params = {"block_number": block_number, "count": count}
    r = await client.get(url, params=params)
    return r.json()


async def bounded_fetch_with_preprocess(
    sem: asyncio.Semaphore,
    client: httpx.AsyncClient,
    block_number: int,
    count: int = 100,
    **preprocess_kwargs,
):
    async with sem:
        data = await fetch_all_mev_from_block(client, block_number, count)  # type: ignore
        return preprocess(pd.DataFrame(data=data), **preprocess_kwargs)
