import os

import discord
import dotenv
from discord.ext import commands

dotenv.load_dotenv()

bot = commands.Bot("nyami#")


@bot.event
async def setup_hook():
    await bot.load_extension("cogs.admin")
    await bot.load_extension("cogs.ai")


bot.run(os.getenv("discord"))
