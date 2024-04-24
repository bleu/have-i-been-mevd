import logging
from lib.zero_mev.api import get_all_mev_transactions_on_last_week
from lib.zero_mev.transformers import preprocess
from lib.templates import (
    WeekOverviewNumberOfSwaps,
    WeekOverviewExtractedAmount,
    WeekOverviewProfitAmount,
    WeekOverviewVictims,
)


async def swaps_report():
    logging.info("Overview week swaps report starting")
    txs = await get_all_mev_transactions_on_last_week()
    txs_processed = preprocess(txs)
    mev_swaps_number = len(txs_processed)
    mev_swaps_per_type = (
        txs_processed.groupby("mev_type")
        .tx_index.count()
        .sort_values(
            ascending=False,
        )
    )

    return WeekOverviewNumberOfSwaps.create_discord_embed(
        {
            "mev_swaps_number": mev_swaps_number,
        },
        has_image=True,
        x_image=mev_swaps_per_type.index.tolist(),
        y_image=mev_swaps_per_type.values.tolist(),
    )


async def extracted_amount_report():
    logging.info("Overview week extracted amount report starting")
    txs = await get_all_mev_transactions_on_last_week()
    txs_processed = preprocess(txs)
    extracted_amount = txs_processed["user_loss_usd"].sum()
    return WeekOverviewExtractedAmount.create_discord_embed(
        {"mev_extracted_amount": extracted_amount}
    )


async def profit_amount_report():
    logging.info("Overview week profit amount report starting")
    txs = await get_all_mev_transactions_on_last_week()
    txs_processed = preprocess(txs)
    profit_amount = txs_processed["extractor_profit_usd"].sum()
    return WeekOverviewProfitAmount.create_discord_embed(
        {"mev_profit_amount": profit_amount}
    )


async def victims_report():
    logging.info("Overview week victims report starting")
    txs = await get_all_mev_transactions_on_last_week()
    txs_processed = preprocess(txs)
    victims_number = txs_processed["address_from"].unique().size
    return WeekOverviewVictims.create_discord_embed(
        {"mev_victims_number": victims_number}
    )
