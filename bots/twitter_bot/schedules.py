import asyncio
import logging

from twitter_bot.api import post_tweet, get_client_v1, get_client_v2
from twitter_bot.reports import (
    extracted_amount_report,
    profit_amount_report,
    swaps_report,
    victims_report,
)
from lib.task_rotation import get_current_task

REPORTS_LIST = [
    swaps_report,
    extracted_amount_report,
    profit_amount_report,
    victims_report,
]


async def weekly_report():
    logging.info("Weekly report starting")
    report = get_current_task(REPORTS_LIST)
    message = await report()
    client_v1 = get_client_v1()
    client_v2 = get_client_v2()
    post_tweet(client_v2, client_v1, message)


SCHEDULE = [
    ["wednesday", "13:00", weekly_report, asyncio.create_task],
]
