import logging
import time

import schedule

from lib.schedule import schedule_module

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


def run():
    schedule_module("twitter")
    logging.info("Twitter bot started")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run()
