import logging
from lib.zero_mev_api.api import get_all_mev_transactions_on_last_week
from lib.transformers.zero_mev import preporcess
from lib.templates import (
    WeekOverviewNumberOfSwaps,
    WeekOverviewExtractedAmount,
    WeekOverviewProfitAmount,
    WeekOverviewVictims,
)


async def swaps_report():
    logging.info("Overview week swaps report starting")
    txs = await get_all_mev_transactions_on_last_week()
    txs_processed = preporcess(txs)
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


async def extracted_amount_report():
    logging.info("Overview week extracted amount report starting")
    txs = await get_all_mev_transactions_on_last_week()
    txs_processed = preporcess(txs)
    extracted_amount = txs_processed["user_loss_usd"].sum()
    embed = WeekOverviewExtractedAmount.create_discord_embed(
        {"mev_extracted_amount": extracted_amount}
    )
    return dict(embed=embed)


async def profit_amount_report():
    logging.info("Overview week profit amount report starting")
    txs = await get_all_mev_transactions_on_last_week()
    txs_processed = preporcess(txs)
    profit_amount = txs_processed["extractor_profit_usd"].sum()
    embed = WeekOverviewProfitAmount.create_discord_embed(
        {"mev_profit_amount": profit_amount}
    )
    return dict(embed=embed)


async def victims_report():
    logging.info("Overview week victims report starting")
    txs = await get_all_mev_transactions_on_last_week()
    txs_processed = preporcess(txs)
    victims_number = txs_processed["address_from"].unique().size
    embed = WeekOverviewVictims.create_discord_embed(
        {"mev_victims_number": victims_number}
    )
    return dict(embed=embed)
