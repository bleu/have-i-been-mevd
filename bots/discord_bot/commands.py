from dataclasses import asdict
import logging
import discord
from discord import app_commands
from discord.ext.commands import Bot
from lib.templates import AddressScanTemplate
from lib.transformers.zero_mev import (
    preprocess,
    get_scan_address_data_from_mev_transactions,
)
from lib.w3 import get_web3_provider
from lib.zero_mev_api.api import get_all_mev_transactions_related_to_address


intents = discord.Intents.all()
intents.typing = False
intents.presences = False

bot = Bot(command_prefix="/", intents=intents)


@bot.tree.command(
    name="scan_address",
    description="Check if how much funds an address lost on MEV.",
)
@app_commands.describe(
    address="The address to be scanned",
    privacy_preserving="If the bot reply should be private or not. Default is not private.",
)
@app_commands.choices(
    privacy_preserving=[
        app_commands.Choice(name="True", value=1),
        app_commands.Choice(name="False", value=0),
    ],
)
async def scan_address(
    interaction: discord.Interaction,
    address: str,
    privacy_preserving: app_commands.Choice[int] = None,
):
    logging.info(f"Scanning {address} address")
    if privacy_preserving is None:
        privacy_preserving = app_commands.Choice(name="False", value=0)
    ephemeral = bool(privacy_preserving.value)
    await interaction.response.defer(
        ephemeral=ephemeral,
    )
    if not get_web3_provider().is_address(address):
        await interaction.followup.send(
            "Invalid address provided, please provide a valid Ethereum address.",
            ephemeral=ephemeral,
        )
        return

    mev_txs = await get_all_mev_transactions_related_to_address(address)
    mev_txs_with_user_loss = preprocess(mev_txs)
    if mev_txs_with_user_loss.empty:
        await interaction.followup.send(
            "No MEV transactions found for the provided address.",
            ephemeral=ephemeral,
        )
        return
    scan_data = get_scan_address_data_from_mev_transactions(
        mev_txs_with_user_loss, address
    )
    embed = AddressScanTemplate.create_discord_embed(asdict(scan_data))
    await interaction.followup.send(
        embed=embed,
        ephemeral=ephemeral,
    )
