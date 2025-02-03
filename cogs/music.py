import asyncio
from concurrent.futures import ThreadPoolExecutor

import discord
from discord.ext import commands
from yt_dlp import YoutubeDL


class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ydl = YoutubeDL(
            {
                "quiet": True,
                "format": "bestaudio/best",
                "noplaylist": True,
                "cookiefile": "./cookies.txt",
            }
        )

    def fetchVideo(self, url: str):
        return self.ydl.sanitize_info(self.ydl.extract_info(url, download=False))

    async def playAudio(self, url: str, ctx: commands.Context, volume: float):
        await ctx.author.voice.channel.connect()

        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            info = await loop.run_in_executor(executor, self.fetchVideo, url)

        options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn -bufsize 64k -analyzeduration 2147483647 -probesize 2147483647",
        }
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(info.get("url"), **options), volume
        )

        def after():
            asyncio.run_coroutine_threadsafe(voiceClient.disconnect(), loop)

        voiceClient: discord.VoiceClient = ctx.guild.voice_client
        voiceClient.play(source, after=after)

    @commands.command("play")
    @commands.cooldown(1, 5)
    async def playCommand(self, ctx: commands.Context, url: str, volume: float = 0.5):
        if ctx.author.voice is None:
            await ctx.reply("ボイスチャンネルに接続してください")
            return
        if ctx.guild.voice_client is not None:
            await ctx.reply("現在再生中です。キュー機能は現在実装していません")
            return

        await self.playAudio(url, ctx, volume)


async def setup(bot: commands.Bot):
    await bot.add_cog(MusicCog(bot))
