import asyncio
from typing import List
import httpx
from lib.zero_mev_api.models import MevTransaction


API_BASE_URL = "https://data.zeromev.org/v1"


async def get_all_mev_transactions_related_to_address(address: str):
    address_from_transaction, address_to_transaction = await asyncio.gather(
        get_paginated_mev_transactions_by_address_and_key(address, "address_from"),
        get_paginated_mev_transactions_by_address_and_key(address, "address_to"),
    )
    return [*address_from_transaction, *address_to_transaction]


async def get_paginated_mev_transactions_by_address_and_key(
    address: str, params_address_key: str
) -> List[MevTransaction]:
    params = {params_address_key: address, "page": 1}
    all_data = []
    while True:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{API_BASE_URL}/mevTransactions", params=params)
        data = r.json()
        all_data.extend(data)
        if not data or len(data) < 1000:
            break
        params["page"] += 1
    return [MevTransaction(**d) for d in all_data]
