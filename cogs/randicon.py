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
    @commands.cooldown(5)
    async def randomProfileCommand(self, ctx: commands.Context):
        number = random.randint(0, 1)
        if number == 0:
            with open("nyami.png", "rb") as f:
                await self.bot.user.edit(global_name="ニャミ", avatar=f.read())
        else:
            with open("usanuko.png", "rb") as f:
                await self.bot.user.edit(global_name="＊うさぬこ＊", avatar=f.read())
        await ctx.message.add_reaction("👍")

    @commands.command("rm")
    @commands.cooldown(10)
    async def randomMentionCommand(self, ctx: commands.Context, count: int = 1):
        members = random.sample(ctx.guild.members, count)
        await ctx.reply(f"{" ".join([member.mention for member in members])}")


async def setup(bot: commands.Bot):
    await bot.add_cog(RandomProfileCog(bot))
