import os
import discord
from discord.ext import commands
from google import genai
from google.genai import types

# Biến môi trường Railway
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# Tạo client Gemini
client = genai.Client(api_key=GEMINI_API_KEY)
model = "gemini-2.0-flash-lite"

# Cấu hình Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập: {bot.user}")

@bot.command(name="ask")
async def ask_gemini(ctx, *, prompt: str):
    await ctx.send("💭 Đang suy nghĩ...")

    try:
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt),
                ],
            ),
        ]
        config = types.GenerateContentConfig(response_mime_type="text/plain")

        reply = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=config,
        ):
            if chunk.text:
                reply += chunk.text

        await ctx.send(f"🤖 **Gemini:** {reply}")
    except Exception as e:
        await ctx.send(f"❌ Lỗi: {str(e)}")

bot.run(DISCORD_TOKEN)
