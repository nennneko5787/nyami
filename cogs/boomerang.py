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

        with open("boomerang.json", "r+") as f:
            self.allowedUsers = json.loads(f.read())

    @commands.command("abl")
    async def addAIWhiteList(self, ctx: commands.Context, user: discord.User):
        if ctx.author.id != 1048448686914551879:
            return
        self.allowedUsers.append(user.id)
        self.allowedUsers = list(set(self.allowedUsers))
        with open("ai-allowed.json", "r+") as f:
            f.write(json.dumps(self.allowedUsers))
        await ctx.reply("ホワイトリストに追加されました。")

    @commands.command("rbl")
    async def removeAIWhiteList(self, ctx: commands.Context, user: discord.User):
        if ctx.author.id != 1048448686914551879:
            return
        self.allowedUsers.remove(user.id)
        self.allowedUsers = list(set(self.allowedUsers))
        with open("ai-allowed.json", "r+") as f:
            f.write(json.dumps(self.allowedUsers))
        await ctx.reply("ホワイトリストから削除されました。")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.author.id in self.allowedUsers:
            return
        await message.reply(":boomerang:", mention_author=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(BoomerangCog(bot))
