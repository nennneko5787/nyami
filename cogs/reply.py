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
        self.cooldown = {}
        self.queue = asyncio.Queue()
        self.process_queue.start()

    @tasks.loop(seconds=5)
    async def process_queue(self):
        """キュー内のメッセージを順番に処理する"""
        message = await self.queue.get()
        try:
            await self.process_message(message)
        except Exception as e:
            raise e

    async def process_message(self, message: discord.Message):
        if "かいさい" in message.content:
            await message.reply("かいさいって誰のこと？", mention_author=True)
        if "ニャミ" in message.content and "好き" in message.content:
            await message.reply(
                "ニャミのことを好きでいてありがとう！", mention_author=True
            )
            self.bot.cogs["AICog"].allowedUsers.append(message.author.id)
            self.bot.cogs["AICog"].allowedUsers = list(
                set(self.bot.cogs["AICog"].allowedUsers)
            )
            with open("ai-allowed.json", "r+") as f:
                f.write(json.dumps(self.bot.cogs["AICog"].allowedUsers))
        if "ニャミ" in message.content and "嫌い" in message.content:
            self.bot.cogs["AICog"].allowedUsers.remove(message.author.id)
            self.bot.cogs["AICog"].allowedUsers = list(
                set(self.bot.cogs["AICog"].allowedUsers)
            )
            with open("ai-allowed.json", "r+") as f:
                f.write(json.dumps(self.bot.cogs["AICog"].allowedUsers))
        if "死ね" in message.content:
            await message.reply("暴言は良くないよ...", mention_author=True)
        if "雑魚" in message.content:
            await message.reply(":boomerang:", mention_author=True)
        if "障害" in message.content:
            await message.reply(":boomerang:", mention_author=True)
        if "しょうがい" in message.content:
            await message.reply(":boomerang:", mention_author=True)

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
        if self.cooldown.get(message.author.id, 0) + 4 >= datetime.now().timestamp():
            return

        self.cooldown[message.author.id] = datetime.now().timestamp()
        await self.queue.put(message)  # キューに追加


async def setup(bot: commands.Bot):
    await bot.add_cog(ReplyCog(bot))
