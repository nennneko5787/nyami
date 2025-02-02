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
        text = ""
        for message in messages:
            if isinstance(message, list):
                before: discord.Message = message[0]
                after: discord.Message = message[1]
                if ctx.channel.id == before.channel.id:
                    text += f"@{before.author.name} > {before.clean_content.split("\n", " ")} -> {after.clean_content.split("\n", " ")}\n"
                    self.messages.remove(message)
            else:
                if ctx.channel.id == message.channel.id:
                    files = ""
                    if message.attachments:
                        for attachment in message.attachments:
                            files += f"{attachment.url} "
                    text += f"@{message.author.name} > {message.clean_content.split("\n", " ")} {files}\n"
                    self.messages.remove(message)

        file = discord.File(io.BytesIO(text.encode()), "log.txt")
        await ctx.reply(
            "-# このチャンネルで削除・編集されたメッセージのみ表示しています", file=file
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        self.messages.append([before, after])

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        self.messages.append(message)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages: List[discord.Message]):
        for message in messages:
            self.messages.append(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(SniperCog(bot))
