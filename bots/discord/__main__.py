import asyncio
import os
import logging

from bots.discord.commands import bot as bot_client

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


@bot_client.event
async def on_ready():
    logging.info(f"We have logged in as {bot_client.user}")
    synced = await bot_client.tree.sync()
    logging.info(f"Synced {len(synced)} commands")


async def start_discord_bot():
    await bot_client.start(os.getenv(f"DISCORD_BOT_TOKEN"))


async def main():
    await start_discord_bot()


# Run the main function
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
