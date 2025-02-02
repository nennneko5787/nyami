import discord
from discord.ext import commands


class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("sm")
    async def sendMessageCommand(
        self, ctx: commands.Context, channelId: int, *, message: str
    ):
        if ctx.author.id != 1048448686914551879:
            return
        await self.bot.get_channel(channelId).send(message)

    @commands.command("st")
    async def sendMessageCommand(self, ctx: commands.Context, *, message: str):
        if ctx.author.id != 1048448686914551879:
            return
        await ctx.message.channel.send(message)

    @commands.command("dl")
    async def deleteCommand(self, ctx: commands.Context):
        if ctx.author.id != 1048448686914551879:
            return
        await ctx.message.reference.resolved.delete()

    @commands.command("reply")
    async def replyCommand(self, ctx: commands.Context, *, message: str):
        if ctx.author.id != 1048448686914551879:
            return
        await ctx.message.reference.resolved.reply(message, mention_author=True)

    @commands.command("ar")
    @commands.cooldown(1, 5)
    async def addreactionCommand(self, ctx: commands.Context, emoji: str):
        await ctx.message.reference.resolved.add_reaction(emoji)

    @commands.command("rr")
    @commands.cooldown(1, 5)
    async def removereactionCommand(self, ctx: commands.Context, emoji: str):
        await ctx.message.reference.resolved.remove_reaction(emoji)

    @commands.Cog.listen()
    async def on_guild_channel_create(self, channel: discord.TextChannel):
        if channel.name == "1day-chat":
            await channel.send("a")

async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCog(bot))
