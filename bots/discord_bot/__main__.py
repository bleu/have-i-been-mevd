import asyncio
import functools
import os
import logging
import schedule

from discord_bot.commands import bot as bot_client
from discord_bot.reports import (
    extracted_amount_report,
    profit_amount_report,
    swaps_report,
    victims_report,
)
from lib.schedule import schedule_module
from lib.task_rotation import get_current_task

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

REPORTS_LIST = [
    swaps_report,
    extracted_amount_report,
    profit_amount_report,
    victims_report,
]


def send_to_channel(func, channel_id: int = int(os.getenv(f"DISCORD_CHANNEL_ID"))):  # type: ignore
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        channel = await bot_client.fetch_channel(channel_id)
        message = await func(*args, **kwargs)

        if message:
            return await channel.send(**message)

    return wrapper


@bot_client.event
async def on_ready():
    logging.info(f"We have logged in as {bot_client.user}")
    synced = await bot_client.tree.sync()
    logging.info(f"Synced {len(synced)} commands")


@send_to_channel
async def weekly_report():
    logging.info("Weekly report starting")
    report = get_current_task(REPORTS_LIST)
    return await report()


async def start_discord_bot():
    await bot_client.start(os.getenv(f"DISCORD_BOT_TOKEN"))  # type: ignore


async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def main():
    schedule_module("discord_bot")
    await asyncio.gather(run_schedule(), start_discord_bot())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
