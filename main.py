import os

import discord
import dotenv
from discord.ext import commands

dotenv.load_dotenv()

bot = commands.Bot(["nyami#", "n#"])


@bot.event
async def setup_hook():
    await bot.load_extension("cogs.admin")
    await bot.load_extension("cogs.ai")
    await bot.load_extension("cogs.sniper")
    await bot.load_extension("cogs.reply")
    await bot.load_extension("cogs.boomerang")
    await bot.load_extension("cogs.music")
    await bot.load_extension("cogs.ytdl")
    await bot.load_extension("cogs.nyamidaisukiforever")
    await bot.load_extension("cogs.randicon")
    await bot.load_extension("cogs.joinlog")


if __name__ == "__main__":
    bot.run(os.getenv("discord"))
