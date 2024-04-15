import asyncio

from bots.discord.__main__ import week_overview_report


SCHEDULE = [
    ["monday", "13:00", week_overview_report, asyncio.create_task],
]
