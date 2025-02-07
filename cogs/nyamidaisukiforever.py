import asyncio
import json
from datetime import datetime

import discord
import dotenv
from discord.ext import commands, tasks

dotenv.load_dotenv()


class NymiDaisukiForeverCog(commands.Cog):
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

        if ("ニャミ" in message.content and "好き" in message.content) or (
            "#ニャミかわいいフォーエバー" in message.content
        ):
            self.bot.cogs["AICog"].allowedUsers.append(message.author.id)
            self.bot.cogs["AICog"].allowedUsers = list(
                set(self.bot.cogs["AICog"].allowedUsers)
            )
            with open("ai-allowed.json", "r+") as f:
                f.write(json.dumps(self.bot.cogs["AICog"].allowedUsers))
            await message.add_reaction("❤️")
        if ("ニャミ" in message.content and "嫌い" in message.content) or (
            "#ニャミカスフォーエバー" in message.content
        ):
            self.bot.cogs["AICog"].allowedUsers.remove(message.author.id)
            self.bot.cogs["AICog"].allowedUsers = list(
                set(self.bot.cogs["AICog"].allowedUsers)
            )
            with open("ai-allowed.json", "r+") as f:
                f.write(json.dumps(self.bot.cogs["AICog"].allowedUsers))
            await message.add_reaction("😡")


async def setup(bot: commands.Bot):
    await bot.add_cog(NymiDaisukiForeverCog(bot))
