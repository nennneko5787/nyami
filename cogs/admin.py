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

    @commands.command("reply")
    async def replyCommand(self, ctx: commands.Context, *, message: str):
        if ctx.author.id != 1048448686914551879:
            return
        await ctx.message.reference.resolved.reply(message, mention_author=True)

    @commands.command("ar")
    async def addreactionCommand(self, ctx: commands.Context, emoji: str):
        if ctx.author.id != 1048448686914551879:
            return
        await ctx.message.reference.resolved.add_reaction(emoji)

    @commands.command("rr")
    async def removereactionCommand(self, ctx: commands.Context, emoji: str):
        if ctx.author.id != 1048448686914551879:
            return
        await ctx.message.reference.resolved.remove_reaction(emoji)


async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCog(bot))
