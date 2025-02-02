import io
from typing import List

import discord
from discord.ext import commands


class SniperCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.messages: list[discord.Message] = []

    @commands.command("s", aliases=["sniper"])
    @commands.cooldown(1, 5)
    async def snipeCommand(self, ctx: commands.Context):
        messages = self.messages
        messages.reverse()
        text = ""
        for message in messages:
            if ctx.channel.id == message.channel.id:
                text += f"@{message.author.name} > {message.clean_content}\n"
                self.messages.remove(message)

        file = discord.File(io.BytesIO(text.encode()), "log.txt")
        await ctx.reply(
            "-# このチャンネルで削除・編集されたメッセージのみ表示しています", file=file
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        self.messages.append(before)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        self.messages.append(message)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages: List[discord.Message]):
        for message in messages:
            self.messages.append(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(SniperCog(bot))
