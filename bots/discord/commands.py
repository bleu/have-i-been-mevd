import discord
from discord import app_commands
from discord.ext.commands import Bot
from lib.templates import AddressScanTemplate
from lib.w3 import get_web3_provider


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
    if get_web3_provider().is_checksum_address(address):
        embed = AddressScanTemplate.create_discord_embed(
            {
                "address": address,
                "totalAmountUsd": 1000,
                "mevTxsLength": 10,
                "mostMevContractName": "UniswapV3",
                "mostMevUsdAmount": 500,
            }
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        return
    await interaction.followup.send(
        "Invalid address provided, please provide a valid Ethereum address.",
        ephemeral=True,
    )
