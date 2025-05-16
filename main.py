import os
import discord
from discord.ext import commands
from google import genai
from google.genai import types

# Lấy API Key từ biến môi trường (Railway)
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# Tạo Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)
model = "gemini-2.0-flash"  # Model bạn yêu cầu

# Cấu hình bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot đã sẵn sàng: {bot.user}")

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
        if "503" in str(e) or "overloaded" in str(e).lower():
            await ctx.send("⚠️ Model hiện đang quá tải. Vui lòng thử lại sau vài phút.")
        else:
            await ctx.send(f"❌ Lỗi: {str(e)}")

bot.run(DISCORD_TOKEN)
