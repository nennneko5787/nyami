import discord
from disord.ext import commands

class JoinLogCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
async def setup(bot: commands.Bot):
    await bot.add_cog(JoinLog(bot))