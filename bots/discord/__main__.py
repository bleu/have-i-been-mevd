import asyncio
from dataclasses import asdict
import functools
import os
import logging
import schedule


from bots.discord.commands import bot as bot_client
from lib.schedule import schedule_module
from lib.templates import WeekOverviewTemplate
from lib.transformers.zero_mev import (
    filter_mev_transactions_with_user_loss,
    get_overview_data_from_mev_transactions,
)
from lib.zero_mev_api.api import get_all_mev_transactions_on_last_week

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


def send_to_channel(func, channel_id: int = int(os.getenv(f"DISCORD_CHANNEL_ID"))):
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


@send_to_channel()
async def week_overview_report():
    logging.info("Overview week report starting")
    txs = await get_all_mev_transactions_on_last_week()
    filtered_txs = filter_mev_transactions_with_user_loss(txs)
    overview_data = get_overview_data_from_mev_transactions(filtered_txs)
    embed = WeekOverviewTemplate.create_discord_embed(asdict(overview_data))
    return dict(embed=embed)


async def start_discord_bot():
    await bot_client.start(os.getenv(f"DISCORD_BOT_TOKEN"))


async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def main():
    schedule_module("discord")
    await asyncio.gather(run_schedule(), start_discord_bot())


# Run the main function
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
