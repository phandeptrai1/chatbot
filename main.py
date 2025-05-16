import os
import json
import discord
from discord.ext import commands
from google import genai
from google.genai import types

# Lấy biến môi trường
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# Cấu hình Gemini
client = genai.Client(api_key=GEMINI_API_KEY)
model = "gemini-2.0-flash"

# Cấu hình Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Đường dẫn file lưu lịch sử
HISTORY_FILE = "history/thuy.json"

# Hàm đọc lịch sử từ file
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []  # Nếu file rỗng
            raw = json.loads(content)
            return [types.Content(**msg) for msg in raw]
    except Exception as e:
        print(f"📛 Lỗi khi load history: {e}")
        return []

# Hàm ghi lịch sử vào file
def save_history(history):
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        raw = [msg.model_dump() for msg in history]
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"📛 Lỗi khi lưu history: {e}")

@bot.event
async def on_ready():
    print(f"🐰 Tú đã online dưới tên: {bot.user}")

@bot.command(name="ask")
async def ask_tu(ctx, *, prompt: str):
    await ctx.send("💭 Đợi xíu Thúy ơi...")

    try:
        # Load lịch sử từ file
        history = load_history()[-6:]

        # Prompt vai trò ban đầu
        messages = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=(
                    "Bạn tên là Tú, AI dễ thương nói chuyện thân mật với Thúy 🐰. "
                    "Gọi Thúy bằng tên, dùng nhiều icon dễ thương như 🥺💖🌸."
                ))]
            )
        ]
        messages.extend(history)

        # Câu mới của Thúy
        new_user_msg = types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
        messages.append(new_user_msg)

        # Gửi tới Gemini
        config = types.GenerateContentConfig(response_mime_type="text/plain")
        reply = ""

        for chunk in client.models.generate_content_stream(
            model=model,
            contents=messages,
            config=config,
        ):
            if chunk.text:
                reply += chunk.text

        await ctx.send(f"🌸 **Tú:** {reply}")

        # Lưu lại lịch sử
        history.append(new_user_msg)
        history.append(types.Content(role="model", parts=[types.Part.from_text(text=reply)]))
        save_history(history)

    except Exception as e:
        await ctx.send(f"❌ Tú lỗi rùi Thúy ơi: `{str(e)}`")

bot.run(DISCORD_TOKEN)
