import asyncio
from concurrent.futures import ThreadPoolExecutor

import discord
from discord.ext import commands
from yt_dlp import YoutubeDL


class YTDLCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ydl = YoutubeDL(
            {
                "quiet": True,
                "format": "best",
                "noplaylist": True,
                "cookiefile": "./cookies.txt",
            }
        )

    def fetchVideo(self, url: str):
        return self.ydl.sanitize_info(self.ydl.extract_info(url, download=False))

    @commands.command("ytdl")
    @commands.cooldown(1, 5)
    async def playCommand(self, ctx: commands.Context, url: str):
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            info = await loop.run_in_executor(executor, self.fetchVideo, url)
        await ctx.reply(f"ダウンロードリンク → {info.get('url')}")


async def setup(bot: commands.Bot):
    await bot.add_cog(YTDLCog(bot))
