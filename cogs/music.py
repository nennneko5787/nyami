import asyncio
import random
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
        self.queue = asyncio.Queue()

    def _isPlayList(self, url: str, locale: str = "ja") -> list[dict] | bool:
        try:
            if locale in ["en-US", "en-GB"]:
                lang = "en"
            elif locale == "es-ES":
                lang = "es"
            elif locale == "sv-SE":
                lang = "sv"
            else:
                lang = locale

            ydlOpts = {
                "quiet": True,
                "extract_flat": True,
                "cookiefile": "./cookies.txt",
                "extractor_args": {"youtube": {"lang": [lang]}},
            }
            with YoutubeDL(ydlOpts) as ydl:
                info = ydl.sanitize_info(ydl.extract_info(url, download=False))
            if "entries" in info and len(info["entries"]) > 1:
                entries = [entry for entry in info["entries"]]
                return entries
            else:
                return [info]
        except Exception as e:
            raise e

    async def isPlayList(self, url: str) -> list[str] | bool:
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            return await loop.run_in_executor(executor, self._isPlayList, url)

    def fetchVideo(self, url: str):
        return self.ydl.sanitize_info(self.ydl.extract_info(url, download=False))

    async def playAudio(self, guild: discord.Guild):
        if self.queue.qsize() <= 0:
            if guild.voice_client is not None:
                await guild.voice_client.disconnect()
            return

        url, ctx, volume = await self.queue.get()

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

        voiceClient: discord.VoiceClient = ctx.guild.voice_client

        def after(e: Exception):
            if voiceClient.is_playing():
                voiceClient.stop()
            if voiceClient.is_connected():
                asyncio.run_coroutine_threadsafe(self.playAudio(guild), loop=loop)

        voiceClient.play(source, after=after)

    @commands.command("play")
    async def playCommand(self, ctx: commands.Context, url: str, volume: float = 0.5):
        if ctx.author.voice is None:
            await ctx.message.add_reaction("❌")
            return
        for info in await self.isPlayList(url):
            print(info)
            await self.queue.put(
                (
                    info["webpage_url"],
                    ctx,
                    volume,
                )
            )
        if ctx.guild.voice_client is not None:
            await ctx.message.add_reaction("👍")
            return

        await ctx.author.voice.channel.connect()
        await self.playAudio(ctx.guild)

    @commands.command("splay")
    async def splayCommand(self, ctx: commands.Context, url: str, volume: float = 0.5):
        if ctx.author.voice is None:
            await ctx.message.add_reaction("❌")
            return
        shuffledData = await self.isPlayList(url)
        random.shuffle(shuffledData)
        for info in shuffledData:
            print(info)
            await self.queue.put(
                (
                    info["webpage_url"],
                    ctx,
                    volume,
                )
            )
        if ctx.guild.voice_client is not None:
            await ctx.message.add_reaction("👍")
            return

        await ctx.author.voice.channel.connect()
        await self.playAudio(ctx.guild)

    @commands.command("skip")
    async def skipCommand(self, ctx: commands.Context):
        voiceClient: discord.VoiceClient = ctx.guild.voice_client
        await voiceClient.stop()
        await ctx.message.add_reaction("👍")

    @commands.command("stop")
    async def stopCommand(self, ctx: commands.Context):
        voiceClient: discord.VoiceClient = ctx.guild.voice_client
        await voiceClient.disconnect()
        await ctx.message.add_reaction("👍")

    @commands.command("pause")
    async def pauseCommand(self, ctx: commands.Context):
        voiceClient: discord.VoiceClient = ctx.guild.voice_client
        voiceClient.pause()
        await ctx.message.add_reaction("👍")

    @commands.command("resume")
    async def resumeCommand(self, ctx: commands.Context):
        voiceClient: discord.VoiceClient = ctx.guild.voice_client
        voiceClient.resume()
        await ctx.message.add_reaction("👍")


async def setup(bot: commands.Bot):
    await bot.add_cog(MusicCog(bot))
