import discord
from discord.ext import commands
import google.generativeai as genai
import os

# Lấy biến môi trường từ Railway dashboard
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# Cấu hình Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Cấu hình bot Discord
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot đã sẵn sàng: {bot.user}")

@bot.command(name="ask")
async def ask_gemini(ctx, *, prompt: str):
    await ctx.send("💬 Đang suy nghĩ...")
    try:
        response = model.generate_content(prompt)
        await ctx.send(f"🤖 **Gemini:** {response.text}")
    except Exception as e:
        await ctx.send(f"❌ Lỗi: {str(e)}")

bot.run(DISCORD_TOKEN)
