from dataclasses import asdict
import discord
from discord import app_commands
from discord.ext.commands import Bot
from lib.templates import AddressScanTemplate
from lib.transformers.zero_mev import (
    filter_mev_transactions_with_user_loss,
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
@app_commands.describe(address="The address to be scanned")
async def scan_address(interaction: discord.Interaction, address: str):
    await interaction.response.defer(ephemeral=True)
    if not get_web3_provider().is_address(address):
        await interaction.followup.send(
            "Invalid address provided, please provide a valid Ethereum address.",
            ephemeral=True,
        )
        return

    mev_txs = await get_all_mev_transactions_related_to_address(address)
    mev_txs_with_user_loss = filter_mev_transactions_with_user_loss(mev_txs)
    if not len(mev_txs_with_user_loss):
        await interaction.followup.send(
            "No MEV transactions found for the provided address.",
            ephemeral=True,
        )
        return
    scan_data = get_scan_address_data_from_mev_transactions(
        mev_txs_with_user_loss, address
    )
    embed = AddressScanTemplate.create_discord_embed(asdict(scan_data))
    await interaction.followup.send(embed=embed, ephemeral=True)
