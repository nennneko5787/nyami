import discord
from discord.ext import commands


class MusicACog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("musica")
    async def musicaPlay(
        self, ctx: commands.Context, mode: str, url: str
    ):
        if ctx.author.id != 1048448686914551879:
            return
        match mode:
            case "join":
                await ctx.author.voice.connect()
            case "play":
                for i in range(1, 15):
                    await ctx.send(f"moyai{i}.music play {url}")
                await ctx.send(f"lolz2.music play {url}")
                await ctx.send(f"lolz5.music play {url}")
                await ctx.send(f"lolz10.music play {url}")
                await ctx.send(f"lolz11.music play {url}")
                await ctx.send(f"lolz12.music play {url}")
                await ctx.send(f"lolz13.music play {url}")
                await ctx.send(f"rat.music play {url}")
                await ctx.send(f";music play {url}")

async def setup(bot: commands.Bot):
    await bot.add_cog(MusicACog(bot))