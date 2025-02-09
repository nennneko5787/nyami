import asyncio
import io
import json
import os
import re
from datetime import datetime

import discord
import dotenv
import google.generativeai as genai
import PIL.Image
from discord.ext import commands, tasks

dotenv.load_dotenv()

genai.configure(api_key=os.getenv("gemini"))
model = genai.GenerativeModel("gemini-1.5-flash")

KANJI_NUM_MAP = {
    "零": 0,
    "〇": 0,
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
    "百": 100,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
}

safetySettings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]


class AICog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.allowedUsers = []
        self.cooldown = {}
        self.chats: dict[int, genai.ChatSession] = {}
        self.queue = asyncio.Queue()
        self.process_queue.start()

        with open("ai-allowed.json", "r+") as f:
            self.allowedUsers = json.loads(f.read())

    def maskNumber(self, text: str):
        for kanji, digit in KANJI_NUM_MAP.items():
            text = text.replace(kanji, str(digit))
        return re.sub(r"\b(0?[0-9]|1[0-2])\b", "*", text)

    @commands.command("aawl")
    async def addAIWhiteList(self, ctx: commands.Context, user: discord.User):
        if ctx.author.id != 1048448686914551879:
            return
        self.allowedUsers.append(user.id)
        self.allowedUsers = list(set(self.allowedUsers))
        with open("ai-allowed.json", "r+") as f:
            f.write(json.dumps(self.allowedUsers))
        await ctx.message.add_reaction("⭕")

    @commands.command("rawl")
    async def removeAIWhiteList(self, ctx: commands.Context, user: discord.User):
        if ctx.author.id != 1048448686914551879:
            return
        self.allowedUsers.remove(user.id)
        self.allowedUsers = list(set(self.allowedUsers))
        with open("ai-allowed.json", "r+") as f:
            f.write(json.dumps(self.allowedUsers))
        await ctx.message.add_reaction("⭕")

    @commands.command("clear")
    @commands.cooldown(1, 5.0)
    async def clearAIHistory(self, ctx: commands.Context):
        del self.chats[ctx.author.id]
        await ctx.message.add_reaction("⭕")

    @tasks.loop(seconds=5)
    async def process_queue(self):
        """キュー内のメッセージを順番に処理する"""
        message = await self.queue.get()
        try:
            await self.process_message(message)
        except Exception as e:
            raise e

    async def process_message(self, message: discord.Message):
        """AIのメッセージ処理"""
        async with message.channel.typing():
            if message.author.id not in self.chats:
                self.chats[message.author.id] = await asyncio.to_thread(
                    model.start_chat
                )

            parts = [message.clean_content.replace("@ニャミ", "")]
            if message.attachments:
                for file in message.attachments:
                    rawData = await file.read()
                    parts.append(PIL.Image.open(io.BytesIO(rawData)))

            response = await asyncio.to_thread(
                self.chats[message.author.id].send_message,
                parts,
                safety_settings=safetySettings,
            )

            text = re.sub(
                r"(歳|さい|ans|years old|y/o|yo|jahre alt|años|лет|anni|anos|साल|tuổi|yaşında|ปี|שנים|ετών|岁|歲|살)",
                "**",
                response.text,
            )

            text = re.sub(
                r"(loli|ロリ|ろり|лоли|लोलीता|לוליטה|λολίτα|萝莉|蘿莉|로리)",
                "**",
                text,
            )

            text = re.sub(
                r"(?<!-)#\s",
                "",
                text,
            )

            await message.reply(
                discord.utils.escape_mentions(self.maskNumber(text)),
                allowed_mentions=discord.AllowedMentions.none(),
            )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """メッセージを受け取ったらキューに追加"""
        if message.content.startswith("nyami#") or message.content.startswith("n#"):
            return
        if message.guild.me.id == message.author.id:
            return
        if message.author.bot:
            return
        if not message.guild.me in message.mentions:
            return
        if not message.author.id in self.allowedUsers:
            return
        if self.cooldown.get(message.author.id, 0) + 8 >= datetime.now().timestamp():
            return

        self.cooldown[message.author.id] = datetime.now().timestamp()
        await self.queue.put(message)  # キューに追加


async def setup(bot: commands.Bot):
    await bot.add_cog(AICog(bot))
