import asyncio

from discord_bot.__main__ import weekly_report


SCHEDULE = [
    ["monday", "13:00", weekly_report, asyncio.create_task],
]
