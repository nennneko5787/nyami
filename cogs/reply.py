import asyncio
import json
from datetime import datetime

import discord
import dotenv
from discord.ext import commands, tasks

dotenv.load_dotenv()


class ReplyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """メッセージを受け取ったらキューに追加"""
        if message.content.startswith("nyami#") or message.content.startswith("n#"):
            return
        if message.guild.me.id == message.author.id:
            return
        if message.author.bot:
            return
        if message.guild.me in message.mentions:
            return

        if "かいさい" in message.content:
            await message.reply("かいさいって誰のこと？", mention_author=True)
        if "死ね" in message.content:
            await message.reply("暴言は良くないよ...", mention_author=True)
        if "雑魚" in message.content:
            await message.reply(":boomerang:", mention_author=True)
        if "障害" in message.content:
            await message.reply(":boomerang:", mention_author=True)
        if "しょうがい" in message.content:
            await message.reply(":boomerang:", mention_author=True)
        if "音猫はゲイですか" in message.content:
            await message.reply("はい、そうです", mention_author=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(ReplyCog(bot))
