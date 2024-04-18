import asyncio
import functools
import os
import logging
import schedule


from bots.discord.commands import bot as bot_client
from lib.schedule import schedule_module
from lib.templates import (
    WeekOverviewExtractedAmount,
    WeekOverviewNumberOfSwaps,
    WeekOverviewVictims,
    WeekOverviewProfitAmount,
)

from lib.transformers.zero_mev import minimal_preporcessing
from lib.zero_mev_api.api import get_all_mev_transactions_on_last_week

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


def send_to_channel(func, channel_id: int = int(os.getenv(f"DISCORD_CHANNEL_ID", 0))):
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
async def swaps_report():
    logging.info("Overview week swaps report starting")
    txs = await get_all_mev_transactions_on_last_week()
    txs_processed = minimal_preporcessing(txs)
    mev_swaps_number = len(txs_processed)
    mev_swaps_per_type = (
        txs_processed.groupby("mev_type")
        .tx_index.count()
        .sort_values(
            ascending=False,
        )
    )

    return WeekOverviewNumberOfSwaps.create_discord_embed_with_image(
        {
            "mev_swaps_number": mev_swaps_number,
        },
        mev_swaps_per_type.index.tolist(),
        mev_swaps_per_type.values.tolist(),
    )


@send_to_channel
async def extracted_amount_report():
    logging.info("Overview week extracted amount report starting")
    txs = await get_all_mev_transactions_on_last_week()
    txs_processed = minimal_preporcessing(txs)
    extracted_amount = txs_processed["user_loss_usd"].sum()
    embed = WeekOverviewExtractedAmount.create_discord_embed(
        {"mev_extracted_amount": extracted_amount}
    )
    return dict(embed=embed)


@send_to_channel
async def profit_amount_report():
    logging.info("Overview week profit amount report starting")
    txs = await get_all_mev_transactions_on_last_week()
    txs_processed = minimal_preporcessing(txs)
    profit_amount = txs_processed["extractor_profit_usd"].sum()
    embed = WeekOverviewProfitAmount.create_discord_embed(
        {"mev_profit_amount": profit_amount}
    )
    return dict(embed=embed)


@send_to_channel
async def victims_report():
    logging.info("Overview week victims report starting")
    txs = await get_all_mev_transactions_on_last_week()
    txs_processed = minimal_preporcessing(txs)
    victims_number = txs_processed["address_from"].unique().size
    embed = WeekOverviewVictims.create_discord_embed(
        {"mev_victims_number": victims_number}
    )
    return dict(embed=embed)


async def start_discord_bot():
    await bot_client.start(os.getenv(f"DISCORD_BOT_TOKEN", ""))


async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def main():
    schedule_module("discord")
    await asyncio.gather(run_schedule(), start_discord_bot())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
