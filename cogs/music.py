import discord
from discord.ext import commands

class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

async def setup(bot: commands.Bot):
    bot.add_cog(MusicCog(bot))