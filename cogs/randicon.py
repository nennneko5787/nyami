import asyncio
from datetime import datetime
import random

import discord
import dotenv
from discord.ext import commands, tasks

dotenv.load_dotenv()


class RandomProfileCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("rp")
    @commands.cooldown(5, 1)
    async def randomProfileCommand(self, ctx: commands.Context):
        number = random.randint(0, 1)
        if number == 0:
            with open("nyami.png", "rb") as f:
                await self.bot.user.edit(global_name="ニャミ", avatar=f.read())
        else:
            with open("usanuko.png", "rb") as f:
                await self.bot.user.edit(global_name="＊うさぬこ＊", avatar=f.read())
        await ctx.message.add_reaction("👍")

    @commands.command("ra")
    @commands.cooldown(5, 1)
    async def randomAvatarCommand(self, ctx: commands.Context):
        number = random.randint(0, 1)
        if number == 0:
            file = discord.File("nyami.png")
        else:
            file = discord.File("usanuko.png")
        await ctx.reply(file=file)

    @commands.command("rm")
    @commands.cooldown(10, 1)
    async def nennneko5787MentionCommand(self, ctx: commands.Context, count: int = 1):
        await ctx.reply("<@1048448686914551879>")


async def setup(bot: commands.Bot):
    await bot.add_cog(RandomProfileCog(bot))
