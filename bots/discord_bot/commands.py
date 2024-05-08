from dataclasses import asdict
import logging
import discord
from discord import app_commands
from discord.ext.commands import Bot
from lib.templates import AddressScanTemplate
from lib.zero_mev.transformers import (
    preprocess,
    get_scan_address_data_from_mev_transactions,
)
from lib.w3 import get_address
from lib.zero_mev.api import get_all_mev_transactions_related_to_address


intents = discord.Intents.all()
intents.typing = False
intents.presences = False

bot = Bot(command_prefix="/", intents=intents)


@bot.tree.command(
    name="scan_address",
    description="Check if how much funds an address lost on MEV.",
)
@app_commands.describe(
    address="The address or ENS name to be scanned.",
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
    address_bytes = get_address(address)
    if not address_bytes:
        await interaction.followup.send(
            "Invalid address provided, please provide a valid Ethereum address.",
            ephemeral=ephemeral,
        )
        return

    mev_txs = await get_all_mev_transactions_related_to_address(address_bytes)
    mev_txs_with_user_loss = preprocess(
        mev_txs, type_filter=["sandwich"], dropna_columns=[]
    )
    if mev_txs_with_user_loss.empty:
        await interaction.followup.send(
            "No MEV transactions found for the provided address.",
            ephemeral=ephemeral,
        )
        return
    scan_data = get_scan_address_data_from_mev_transactions(
        mev_txs_with_user_loss, address
    )
    output = AddressScanTemplate.create_discord_embed(asdict(scan_data))
    await interaction.followup.send(
        embed=output["embed"],
        ephemeral=ephemeral,
    )
