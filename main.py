import os
import discord
from discord.ext import commands
from google import genai
from google.genai import types

# Lấy API Key từ môi trường Railway
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# Tạo Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)
model = "gemini-2.0-flash"

# Cấu hình bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🐰 Bot Tú đã online dưới tên: {bot.user}")

@bot.command(name="ask")
async def ask_tu(ctx, *, prompt: str):
    await ctx.send("💭 Đợi xíu Thúy ơi...")

    try:
        role_prompt = (
            "Bạn tên là Tú, là một AI đáng yêu và dễ thương nhất quả đất 🌸.\n"
            "Bạn nói chuyện thân thiện, dùng nhiều icon cute như 🥺✨💖🐰🌸.\n"
            "Bạn đang trò chuyện với Thúy - bạn thân nhất của bạn 💖. Hãy luôn gọi người đó là 'Thúy' và thể hiện sự thân mật, vui vẻ nhaaa 🐾."
        )

        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=role_prompt)],
            ),
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
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

        await ctx.send(f"🌸 **Tú:** {reply}")
    
    except Exception as e:
        if "503" in str(e) or "overloaded" in str(e).lower():
            await ctx.send("⚠️ Tú đang hơi mệt á Thúy ơi 🥺. Đợi Tú một xíu rồi hỏi lại nhaaaa 💖")
        else:
            await ctx.send(f"❌ Oops Thúy ơi, bị lỗi rồi nè: `{str(e)}`")

bot.run(DISCORD_TOKEN)
