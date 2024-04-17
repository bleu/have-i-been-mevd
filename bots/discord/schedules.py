import asyncio

from bots.discord.__main__ import (
    swaps_report,
    extracted_amount_report,
    profit_amount_report,
    victims_report,
)


SCHEDULE = [
    ["wednesday", "14:45", swaps_report, asyncio.create_task],
    ["wednesday", "14:50", extracted_amount_report, asyncio.create_task],
    ["wednesday", "14:55", profit_amount_report, asyncio.create_task],
    ["wednesday", "15:00", victims_report, asyncio.create_task],
]
