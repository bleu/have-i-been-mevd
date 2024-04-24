import logging
import asyncio

import schedule

from lib.schedule import schedule_module

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def main():
    schedule_module("twitter_bot")
    await run_schedule()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
