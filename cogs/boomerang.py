import asyncio
import json
from datetime import datetime

import discord
import dotenv
from discord.ext import commands, tasks

dotenv.load_dotenv()


class BoomerangCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.allowedUsers = []
        self.queue = asyncio.Queue()

        with open("boomerang.json", "r+") as f:
            self.allowedUsers = json.loads(f.read())
        self.process_queue.start()

    @tasks.loop(seconds=12)
    async def process_queue(self):
        """キュー内のメッセージを順番に処理する"""
        message = await self.queue.get()
        try:
            await self.process_message(message)
        except Exception as e:
            raise e

    @commands.command("abl")
    async def addAIWhiteList(self, ctx: commands.Context, user: discord.User):
        if ctx.author.id != 1048448686914551879:
            return
        self.allowedUsers.append(user.id)
        self.allowedUsers = list(set(self.allowedUsers))
        with open("boomerang.json", "r+") as f:
            f.write(json.dumps(self.allowedUsers))
        await ctx.reply("リストに追加されました。")

    @commands.command("rbl")
    async def removeAIWhiteList(self, ctx: commands.Context, user: discord.User):
        if ctx.author.id != 1048448686914551879:
            return
        self.allowedUsers.remove(user.id)
        self.allowedUsers = list(set(self.allowedUsers))
        with open("boomerang.json", "r+") as f:
            f.write(json.dumps(self.allowedUsers))
        await ctx.reply("リストから削除されました。")

    async def process_message(self, message: discord.Message):
        await message.reply(":boomerang:", mention_author=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.author.id in self.allowedUsers:
            return
        await self.queue.put(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(BoomerangCog(bot))
