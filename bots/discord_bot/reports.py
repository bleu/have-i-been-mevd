import logging
import pandas as pd


from lib.zero_mev.api import get_all_mev_transactions_on_last_week
from lib.zero_mev.transformers import preprocess
from lib.templates import (
    WeekOverviewNumberOfSwaps,
    WeekOverviewExtractedAmount,
    WeekOverviewProfitAmount,
    WeekOverviewVictims,
    WeekOverviewDex,
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
    mev_amount_per_protocol = (
        txs_processed.groupby("protocol")
        .user_loss_usd.sum()
        .sort_values(
            ascending=False,
        )
    )
    extracted_amount = txs_processed["user_loss_usd"].sum()
    return WeekOverviewExtractedAmount.create_discord_embed(
        {"mev_extracted_amount": extracted_amount},
        has_image=True,
        x_image=mev_amount_per_protocol.index.tolist(),
        y_image=mev_amount_per_protocol.values.tolist(),
    )


async def profit_amount_report():
    logging.info("Overview week profit amount report starting")
    txs = await get_all_mev_transactions_on_last_week()

    txs_processed = preprocess(txs)
    profit_amount = txs_processed["extractor_profit_usd"].sum()
    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    txs_processed["day"] = pd.to_datetime(
        txs_processed["arrival_time_eu"]
    ).dt.day_name()  # type: ignore
    mev_per_day = (
        txs_processed.groupby("day").extractor_profit_usd.sum().reindex(weekdays)
    )
    return WeekOverviewProfitAmount.create_discord_embed(
        {"mev_profit_amount": profit_amount},
        has_image=True,
        x_image=mev_per_day.index.tolist(),
        y_image=mev_per_day.values.tolist(),
    )


async def dex_report():
    logging.info("Overview week dex report starting")
    txs = await get_all_mev_transactions_on_last_week()
    txs_processed = preprocess(
        txs,
        protocols_filter=[
            "uniswap2",
            "uniswap3",
            "zerox",
            "curve",
            "balancer1",
            "bancor",
        ],
        type_filter=["sandwich"],
    )
    loss_amount = txs_processed["user_loss_usd"].sum()
    mev_per_dex = (
        txs_processed.groupby("protocol")
        .user_loss_usd.sum()
        .sort_values(ascending=False)
    )
    threshold = 0.01 * loss_amount
    small_groups = mev_per_dex[mev_per_dex < threshold]
    mev_per_dex.loc["others"] = small_groups.sum()
    mev_per_dex.drop(small_groups.index, inplace=True)
    return WeekOverviewDex.create_discord_embed(
        {"mev_dex_amount": loss_amount},
        has_image=True,
        x_image=mev_per_dex.index.tolist(),
        y_image=mev_per_dex.values.tolist(),
    )


async def victims_report():
    logging.info("Overview week victims report starting")
    txs = await get_all_mev_transactions_on_last_week()
    txs_processed = preprocess(txs, type_filter=["sandwich"])
    victims_number = txs_processed["address_from"].unique().size
    return WeekOverviewVictims.create_discord_embed(
        {"mev_victims_number": victims_number}
    )
