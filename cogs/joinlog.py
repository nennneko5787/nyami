import discord
from discord.ext import commands

class JoinLogCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id != 1135775339377860648:
            return
        await self.bot.get_channel(1252406721943703683).send(f"{member.display_name} (ID: {member.name}) がやって来ました。", silent=True)

    @commands.Cog.listener()
    async def on_raw_member_remove(self, payload: discord.RawMemberRemoveEvent):
        if payload.guild_id != 1135775339377860648:
            return
        await self.bot.get_channel(1252406721943703683).send(f"{payload.user.display_name} (ID: {payload.user.name}) が退出しました。", silent=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(JoinLogCog(bot))