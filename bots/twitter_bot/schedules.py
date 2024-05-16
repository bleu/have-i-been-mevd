import asyncio
import logging

from twitter_bot.api import TwitterAPI
from twitter_bot.reports import (
    dex_report,
    extracted_amount_report,
    profit_amount_report,
    swaps_report,
    victims_report,
)
from twitter_bot.replies import reply_on_mentions
from lib.task_rotation import get_current_task

REPORTS_LIST = [
    swaps_report,
    extracted_amount_report,
    profit_amount_report,
    victims_report,
    dex_report,
]


async def weekly_report():
    logging.info("Weekly report starting")
    report = get_current_task(REPORTS_LIST)
    message = await report()
    twitter_api = TwitterAPI()
    twitter_api.post_tweet(message)


SCHEDULE = [
    ["monday", "14:00", weekly_report, asyncio.create_task],
    ["minutes", ":02", reply_on_mentions, asyncio.create_task],
]
