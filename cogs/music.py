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
        self.queue = asyncio.Queue()

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
            await ctx.message.add_reaction(discord.PartialEmoji.from_str(":x:"))
            return
        await self.queue.put(
            (
                url,
                ctx,
                volume,
            )
        )
        if ctx.guild.voice_client is not None:
            await ctx.message.add_reaction(discord.PartialEmoji.from_str(":thumbs_up:"))
            return

        await ctx.author.voice.channel.connect()
        await self.playAudio(ctx.guild)

    @commands.command("skip")
    async def skipCommand(self, ctx: commands.Context):
        voiceClient: discord.VoiceClient = ctx.guild.voice_client
        await voiceClient.stop()

    @commands.command("stop")
    async def stopCommand(self, ctx: commands.Context):
        voiceClient: discord.VoiceClient = ctx.guild.voice_client
        await voiceClient.disconnect()


async def setup(bot: commands.Bot):
    await bot.add_cog(MusicCog(bot))
